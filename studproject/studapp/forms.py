import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note, Subject, Branch, Comment


# --------------- Shared helpers ---------------

def validate_strict_email(email):
    # Reject emails with suspicious multi-part TLDs like user@gmail.com.in.gov
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$'
    if not re.match(pattern, email):
        raise forms.ValidationError('Enter a valid email address (e.g. name@example.com).')
    # Reject domains with more than 3 parts (e.g. gmail.com.in.gov has 4)
    domain = email.split('@')[1]
    parts = domain.split('.')
    if len(parts) > 3:
        raise forms.ValidationError('This email domain is invalid. Please check and try again.')


def validate_name(value, field_label):
    # Names must contain only letters, spaces, and hyphens.
    cleaned = value.strip()
    if not cleaned:
        raise forms.ValidationError(f'{field_label} cannot be blank.')
    if not re.match(r'^[a-zA-Z\s\-]+$', cleaned):
        raise forms.ValidationError(f'{field_label} can only contain letters, spaces, and hyphens.')
    return cleaned


# --------------- Forms ---------------

class UserUpdateForm(forms.ModelForm):
    # Form for updating user name and email.
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        validate_strict_email(email)
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('This email is already in use by another account.')
        return email


class SignUpForm(UserCreationForm):
    # Registration form with email and name fields.
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email', 'id': 'signup-email'})
    )
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name', 'id': 'signup-first-name'})
    )
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name', 'id': 'signup-last-name'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Choose a username', 'id': 'signup-username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Create a password', 'id': 'signup-password1'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm password', 'id': 'signup-password2'})

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        validate_strict_email(email)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise forms.ValidationError('Username can only contain letters, numbers, underscores, and hyphens.')
        return username

    def clean_first_name(self):
        return validate_name(self.cleaned_data.get('first_name', ''), 'First name')

    def clean_last_name(self):
        return validate_name(self.cleaned_data.get('last_name', ''), 'Last name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class NoteUploadForm(forms.ModelForm):
    """Form for uploading a note."""
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(), required=True,
        widget=forms.Select(attrs={'class': 'form-input', 'id': 'note-branch'}),
        empty_label='-- Select Branch --',
    )

    class Meta:
        model = Note
        fields = ('title', 'description', 'subject', 'file')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Give your notes a title', 'id': 'note-title'}),
            'description': forms.Textarea(attrs={'class': 'form-input form-textarea', 'placeholder': 'What do these notes cover?', 'rows': 4, 'id': 'note-description'}),
            'subject': forms.Select(attrs={'class': 'form-input', 'id': 'note-subject'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-file-input', 'id': 'note-file', 'accept': '.pdf,.doc,.docx,.ppt,.pptx,.txt,.jpg,.jpeg,.png'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.select_related('branch').all()
        self.fields['subject'].empty_label = '-- Select Subject --'

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_file(self):
        """Reject files larger than 100 MB."""
        f = self.cleaned_data.get('file')
        if f:
            from django.conf import settings
            max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 100 * 1024 * 1024)
            if f.size > max_size:
                raise forms.ValidationError(f'File too large! Max size is {max_size // (1024 * 1024)} MB.')
        return f


class CommentForm(forms.ModelForm):
    """Form for adding a comment to a note."""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-input comment-input',
                'placeholder': 'Write a comment...',
                'rows': 2,
                'maxlength': 500,
                'id': 'comment-text',
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        if not text:
            raise forms.ValidationError('Comment cannot be empty.')
        if len(text) > 500:
            raise forms.ValidationError('Comment must be 500 characters or less.')
        return text

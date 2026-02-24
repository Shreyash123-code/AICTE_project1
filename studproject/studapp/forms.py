from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note, Subject, Branch


class UserUpdateForm(forms.ModelForm):
    """Form for updating user name and email."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class SignUpForm(UserCreationForm):
    """Registration form with email and name fields."""
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

    def clean_file(self):
        """Reject files larger than 10 MB."""
        f = self.cleaned_data.get('file')
        if f:
            from django.conf import settings
            max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
            if f.size > max_size:
                raise forms.ValidationError(f'File too large! Max size is {max_size // (1024 * 1024)} MB.')
        return f

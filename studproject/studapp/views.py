from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.db.models import Q, Count
from .models import Note, Subject, Branch, Bookmark, Download
from .forms import SignUpForm, NoteUploadForm, UserUpdateForm, ProfileUpdateForm


def home(request):
    """Landing page with hero, features, and recent notes."""
    recent_notes = Note.objects.select_related('subject', 'subject__branch', 'uploaded_by')[:6]
    branches = Branch.objects.prefetch_related('subjects').annotate(note_count=Count('subjects__notes'))
    total_notes = Note.objects.count()
    total_branches = Branch.objects.count()
    context = {
        'recent_notes': recent_notes,
        'branches': branches,
        'total_notes': total_notes,
        'total_branches': total_branches,
    }
    return render(request, 'home.html', context)


def signup_view(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Stud Safe, {user.first_name}! 🎉')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if remember_me:
                request.session.set_expiry(2592000)  # 30 days in seconds
            else:
                request.session.set_expiry(0)  # Browser close
                
            messages.success(request, f'Welcome back, {user.first_name}! 👋')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    """Log out the user."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def browse_notes(request):
    """Browse and search notes, optionally filtered by branch and subject."""
    notes = Note.objects.select_related('subject', 'subject__branch', 'uploaded_by')
    branches = Branch.objects.prefetch_related('subjects').annotate(note_count=Count('subjects__notes'))
    subjects = Subject.objects.select_related('branch').annotate(note_count=Count('notes'))

    # Filter by branch
    branch_id = request.GET.get('branch')
    if branch_id:
        notes = notes.filter(subject__branch_id=branch_id)
        subjects = subjects.filter(branch_id=branch_id)

    # Filter by subject
    subject_id = request.GET.get('subject')
    if subject_id:
        notes = notes.filter(subject_id=subject_id)

    # Search
    query = request.GET.get('q', '')
    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(subject__branch__name__icontains=query)
        )

    # Get bookmarked note IDs for the current user
    bookmarked_ids = []
    if request.user.is_authenticated:
        bookmarked_ids = list(Bookmark.objects.filter(user=request.user).values_list('note_id', flat=True))

    context = {
        'notes': notes,
        'branches': branches,
        'subjects': subjects,
        'current_branch': branch_id,
        'current_subject': subject_id,
        'search_query': query,
        'bookmarked_ids': bookmarked_ids,
    }
    return render(request, 'browse.html', context)


@login_required(login_url='login')
def upload_note(request):
    """Upload a new note."""
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Your notes have been uploaded successfully! 📚')
            return redirect('dashboard')
    else:
        form = NoteUploadForm()
    return render(request, 'upload.html', {'form': form})


@login_required(login_url='login')
def download_note(request, note_id):
    """Download a note file and increment download count."""
    note = get_object_or_404(Note, id=note_id)
    
    if not note.file:
        messages.error(request, 'This note has no file attached.')
        return redirect('browse')
        
    try:
        response = FileResponse(note.file.open('rb'), as_attachment=True, filename=note.file.name.split('/')[-1])
        note.downloads += 1
        note.save(update_fields=['downloads'])
        # Record who downloaded it
        Download.objects.create(user=request.user, note=note)
        return response
    except FileNotFoundError:
        messages.error(request, 'The requested file could not be found on the server.')
        return redirect('browse')


@login_required(login_url='login')
def preview_note(request, note_id):
    """Preview a note file in the browser with an HTML wrapper for certain types."""
    note = get_object_or_404(Note, id=note_id)
    
    if not note.file:
        messages.error(request, 'This note has no file attached.')
        return redirect('browse')
        
    file_url = note.file.url
    extension = note.file.name.split('.')[-1].lower()
    
    # Handle images
    if extension in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ margin:0; display:flex; justify-content:center; align-items:center; background:#0f172a; height:100vh; overflow:hidden; user-select:none; -webkit-user-select:none; }}
                    img {{ max-width:100%; max-height:100%; object-fit:contain; pointer-events:none; -webkit-user-drag:none; }}
                </style>
            </head>
            <body oncontextmenu="return false;">
                <img src="{file_url}">
            </body>
        </html>
        """
        from django.http import HttpResponse
        return HttpResponse(html_content)
    
    # Handle text files
    if extension in ['txt', 'py', 'js', 'html', 'css']:
        try:
            content = note.file.read().decode('utf-8')
            html_content = f"""
            <html>
                <head>
                    <style>
                        body {{ margin:0; padding:20px; background:#0f172a; color:#f8fafc; font-family:monospace; line-height:1.5; user-select:none; -webkit-user-select:none; }}
                        pre {{ white-space:pre-wrap; word-break:break-all; pointer-events:none; }}
                    </style>
                </head>
                <body oncontextmenu="return false;">
                    <pre>{content}</pre>
                </body>
            </html>
            """
            from django.http import HttpResponse
            return HttpResponse(html_content)
        except:
            pass 
            
    # Handle PDFs
    if extension == 'pdf':
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ margin:0; padding:0; background:#0f172a; overflow:hidden; }}
                    .pdf-container {{
                        position: relative;
                        width: 100%;
                        height: 100vh;
                        background: #0f172a;
                    }}
                    /* Shift iframe up to hide browser PDF toolbar */
                    iframe {{
                        position: absolute;
                        top: -50px; 
                        left: 0;
                        width: 100%;
                        height: calc(100vh + 50px);
                        border: none;
                    }}
                    /* Transparent blocker only over the top hidden area to prevent interaction with the toolbar */
                    .top-blocker {{
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 60px;
                        background: transparent;
                        z-index: 10;
                    }}
                </style>
            </head>
            <body oncontextmenu="return false;">
                <div class="pdf-container">
                    <div class="top-blocker"></div>
                    <iframe src="{file_url}#toolbar=0&navpanes=0"></iframe>
                </div>
            </body>
        </html>
        """
        from django.http import HttpResponse
        return HttpResponse(html_content)
            
    try:
        # Fallback for other files
        return FileResponse(note.file.open('rb'), as_attachment=False)
    except FileNotFoundError:
        messages.error(request, 'The requested file could not be found on the server.')
        return redirect('browse')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard showing their profile, uploaded notes, and bookmarks."""
    user_notes = Note.objects.filter(uploaded_by=request.user).select_related('subject')
    user_bookmarks = Bookmark.objects.filter(user=request.user).select_related('note', 'note__subject', 'note__uploaded_by')
    
    # Track the user's own downloads (files they downloaded)
    user_downloads = Download.objects.filter(user=request.user).select_related('note', 'note__subject')
    total_downloads = user_downloads.count()
    
    if request.method == 'POST' and 'update_profile' in request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Ensure profile exists
        from .models import Profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated! ✨')
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # Ensure profile exists
        from .models import Profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_notes': user_notes,
        'user_bookmarks': user_bookmarks,
        'total_downloads': total_downloads,
        'user_downloads': user_downloads,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def toggle_bookmark(request, note_id):
    """Toggle bookmark on a note."""
    note = get_object_or_404(Note, id=note_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, note=note)
    if not created:
        bookmark.delete()
        messages.info(request, 'Bookmark removed.')
    else:
        messages.success(request, 'Note bookmarked! 🔖')
    return redirect(request.META.get('HTTP_REFERER', 'browse'))


@login_required(login_url='login')
def delete_note(request, note_id):
    """Delete a note — only the uploader can delete their own note."""
    note = get_object_or_404(Note, id=note_id)

    # Only the uploader can delete
    if note.uploaded_by != request.user:
        messages.error(request, 'You can only delete your own notes.')
        return redirect('dashboard')

    if request.method == 'POST':
        # Delete the file from storage
        if note.file:
            note.file.delete(save=False)
        note.delete()
        messages.success(request, 'Note deleted successfully! 🗑️')

    return redirect('dashboard')
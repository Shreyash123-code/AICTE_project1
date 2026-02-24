from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Note, Subject, Branch, Bookmark
from .forms import SignUpForm, NoteUploadForm, UserUpdateForm


def home(request):
    """Home page."""
    recent_notes = Note.objects.select_related('subject', 'subject__branch', 'uploaded_by')[:6]
    branches = Branch.objects.annotate(note_count=Count('subjects__notes'))

    # Get IDs for the four featured FE subjects
    featured_subjects = {}
    subject_map = {
        'math': 'Engineering Mathematics-I',
        'mechanics': 'Engineering Mechanics',
        'electrical': 'Basic Electrical Engineering',
        'chemistry': 'Engineering Chemistry',
    }
    for key, name in subject_map.items():
        subj = Subject.objects.filter(name=name).first()
        if subj:
            featured_subjects[key] = subj.id

    return render(request, 'home.html', {
        'recent_notes': recent_notes,
        'branches': branches,
        'total_notes': Note.objects.count(),
        'total_branches': Branch.objects.count(),
        'featured_subjects': featured_subjects,
    })


def signup_view(request):
    """Sign up a new user."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account is ready.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """Log in a user."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password.')
    return render(request, 'login.html')


def logout_view(request):
    """Log out."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def browse_notes(request):
    """Browse notes with optional filters and search."""
    notes = Note.objects.select_related('subject', 'subject__branch', 'uploaded_by')
    branches = Branch.objects.annotate(note_count=Count('subjects__notes'))
    subjects = Subject.objects.select_related('branch').annotate(note_count=Count('notes'))

    branch_id = request.GET.get('branch')
    subject_id = request.GET.get('subject')
    query = request.GET.get('q', '')

    if branch_id:
        notes = notes.filter(subject__branch_id=branch_id)
        subjects = subjects.filter(branch_id=branch_id)
    if subject_id:
        notes = notes.filter(subject_id=subject_id)
    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(description__icontains=query) |
            Q(subject__name__icontains=query) | Q(subject__branch__name__icontains=query)
        )

    # Pagination — 12 per page
    page_obj = Paginator(notes, 12).get_page(request.GET.get('page'))

    # Bookmarks for current user
    bookmarked_ids = []
    if request.user.is_authenticated:
        bookmarked_ids = list(Bookmark.objects.filter(user=request.user).values_list('note_id', flat=True))

    return render(request, 'browse.html', {
        'notes': page_obj,
        'page_obj': page_obj,
        'branches': branches,
        'subjects': subjects,
        'current_branch': branch_id,
        'current_subject': subject_id,
        'search_query': query,
        'bookmarked_ids': bookmarked_ids,
    })


def get_subjects(request, branch_id):
    """Return subjects for a branch (JSON, used by upload form)."""
    subjects = Subject.objects.filter(branch_id=branch_id).values('id', 'name', 'icon')
    return JsonResponse(list(subjects), safe=False)


@login_required(login_url='login')
def upload_note(request):
    """Upload a new note."""
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Note uploaded!')
            return redirect('browse')
    else:
        form = NoteUploadForm()
    return render(request, 'upload.html', {'form': form})


@login_required(login_url='login')
def download_note(request, note_id):
    """Download a note and count it."""
    note = get_object_or_404(Note, id=note_id)
    if not note.file:
        messages.error(request, 'No file attached to this note.')
        return redirect('browse')
    try:
        filename = note.file.name.split('/')[-1]
        response = FileResponse(note.file.open('rb'), as_attachment=True, filename=filename)
        note.downloads += 1
        note.save(update_fields=['downloads'])
        return response
    except FileNotFoundError:
        messages.error(request, 'File not found on server.')
        return redirect('browse')


@login_required(login_url='login')
def preview_note(request, note_id):
    """Preview a note file in the browser."""
    note = get_object_or_404(Note, id=note_id)
    if not note.file:
        messages.error(request, 'No file attached.')
        return redirect('browse')

    ext = note.file.name.rsplit('.', 1)[-1].lower()
    url = note.file.url

    # Images — show centered
    if ext in ('jpg', 'jpeg', 'png', 'gif', 'webp'):
        return HttpResponse(f'''
        <body style="margin:0;display:flex;justify-content:center;align-items:center;background:#0f172a;height:100vh" oncontextmenu="return false">
            <img src="{url}" style="max-width:100%;max-height:100%;object-fit:contain">
        </body>''')

    # Text files — show as preformatted text
    if ext in ('txt', 'py', 'js', 'html', 'css'):
        try:
            content = note.file.read().decode('utf-8')
            import html
            content = html.escape(content)
            return HttpResponse(f'''
            <body style="margin:0;padding:20px;background:#0f172a;color:#f8fafc;font-family:monospace" oncontextmenu="return false">
                <pre>{content}</pre>
            </body>''')
        except Exception:
            pass

    # PDFs — embed in iframe
    if ext == 'pdf':
        return HttpResponse(f'''
        <body style="margin:0;background:#0f172a;overflow:hidden" oncontextmenu="return false">
            <iframe src="{url}#toolbar=0&navpanes=0" style="width:100%;height:100vh;border:none"></iframe>
        </body>''')

    # Fallback — serve the raw file
    try:
        return FileResponse(note.file.open('rb'), as_attachment=False)
    except FileNotFoundError:
        messages.error(request, 'File not found.')
        return redirect('browse')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard."""
    user_notes = Note.objects.filter(uploaded_by=request.user).select_related('subject')
    user_bookmarks = Bookmark.objects.filter(user=request.user).select_related('note', 'note__subject')

    if request.method == 'POST' and 'update_profile' in request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'dashboard.html', {
        'user_notes': user_notes,
        'user_bookmarks': user_bookmarks,
        'u_form': u_form,
    })


@login_required(login_url='login')
def toggle_bookmark(request, note_id):
    """Add or remove a bookmark."""
    note = get_object_or_404(Note, id=note_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, note=note)
    if not created:
        bookmark.delete()
        messages.info(request, 'Bookmark removed.')
    else:
        messages.success(request, 'Note bookmarked!')
    return redirect(request.META.get('HTTP_REFERER', 'browse'))


@login_required(login_url='login')
def delete_note(request, note_id):
    """Delete a note (only the uploader can delete)."""
    note = get_object_or_404(Note, id=note_id)
    if note.uploaded_by != request.user:
        messages.error(request, "You can only delete your own notes.")
        return redirect('dashboard')
    if request.method == 'POST':
        if note.file:
            import os
            if os.path.isfile(note.file.path):
                os.remove(note.file.path)
        note.delete()
        messages.success(request, 'Note deleted.')
    return redirect('dashboard')
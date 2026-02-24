from django.db import models
from django.contrib.auth.models import User


class Branch(models.Model):
    """Engineering branch (CSE, ECE, etc.)."""
    name = models.CharField(max_length=150, unique=True)
    icon = models.CharField(max_length=50, default='🎓')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Branches'


class Subject(models.Model):
    """Subject within a branch."""
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    icon = models.CharField(max_length=50, default='📘')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.branch.name})" if self.branch else self.name

    class Meta:
        ordering = ['branch__name', 'name']


class Note(models.Model):
    """An uploaded note file."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='notes/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} — {self.subject.name}"

    class Meta:
        ordering = ['-created_at']


class Bookmark(models.Model):
    """A user's bookmarked note."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')

    def __str__(self):
        return f"{self.user.username} → {self.note.title}"


class Comment(models.Model):
    """A comment on a note."""
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.text[:40]}"

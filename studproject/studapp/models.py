from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)


class Branch(models.Model):
    name = models.CharField(max_length=150, unique=True)
    icon = models.CharField(max_length=50, default='🎓')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Branches'


class Subject(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    icon = models.CharField(max_length=50, default='📘')  # emoji icon
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.branch.name})" if self.branch else self.name

    class Meta:
        ordering = ['branch__name', 'name']


class Note(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')

    def __str__(self):
        return f"{self.user.username} → {self.note.title}"


class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='download_records')
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-downloaded_at']

    def __str__(self):
        return f"{self.user.username} ⬇ {self.note.title}"

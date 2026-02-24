from django.contrib import admin
from .models import Branch, Subject, Note, Bookmark


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'icon', 'created_at')
    list_filter = ('branch',)
    search_fields = ('name',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'downloads', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'created_at')
    list_filter = ('created_at',)

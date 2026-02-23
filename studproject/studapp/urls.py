from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('browse/', views.browse_notes, name='browse'),
    path('upload/', views.upload_note, name='upload'),
    path('download/<int:note_id>/', views.download_note, name='download'),
    path('preview/<int:note_id>/', views.preview_note, name='preview'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bookmark/<int:note_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
]

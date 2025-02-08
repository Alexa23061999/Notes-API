from django.urls import path
from .views import user_registration, user_login
from .views import create_note, get_note_by_id, get_user_notes, update_note, delete_note


urlpatterns = [
    path('register/', user_registration, name='register'),
    path('login/', user_login, name='login'),
    path('notes/create/', create_note, name='create_note'),
    path('notes/', get_user_notes, name='list_notes'),
    path('notes/<uuid:note_id>/', get_note_by_id, name='get-note-by-id'),
    path('update/notes/<uuid:note_id>/', update_note, name='update_note'),
    path('delete/notes/<uuid:note_id>/', delete_note, name='delete_note'),
]
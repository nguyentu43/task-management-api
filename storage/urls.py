from django.urls import path
from .views import get_files_view, upload_file_view, get_file_view, delete_file_view

urlpatterns = [
    path(r'<int:project_pk>/<int:task_pk>/', get_files_view),
    path(r'<int:project_pk>/<int:task_pk>/<str:filename>', get_file_view),
    path(r'<int:project_pk>/<int:task_pk>/<str:filename>/delete', delete_file_view),
    path(r'', upload_file_view)
]
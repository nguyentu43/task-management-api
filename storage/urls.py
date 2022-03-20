from django.urls import path
from .views import get_files_view, upload_file_view, manage_file

urlpatterns = [
    path(r'<int:project_pk>/<int:task_pk>/', get_files_view),
    path(r'<int:project_pk>/<int:task_pk>/<str:filename>', manage_file),
    path(r'', upload_file_view)
]
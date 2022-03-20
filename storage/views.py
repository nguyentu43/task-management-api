from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from storages.backends.ftp import FTPStorageException

from .forms import UploadFileForm
from rest_framework.response import Response
from rest_framework import status
from .utils import get_files, delete_file, get_file, exists_file, save_file
import mimetypes
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file_view(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.data
        file = request.FILES['file']
        filename = str(int(datetime.now().timestamp())) + '.' + file.name
        save_file(data['project_pk'], data['task_pk'], filename, file)
        return Response({'filename': filename }, status=status.HTTP_200_OK)
    return Response({"error": form.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_files_view(request, project_pk, task_pk):
    return Response(get_files(project_pk, task_pk))

@swagger_auto_schema(methods=['get', 'delete'], operation_id='storage_file_read_delete')
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_file(request, project_pk, task_pk, filename):
    if request.method == 'GET':
        file = get_file(project_pk, task_pk, filename)
        content_type = mimetypes.guess_type(file.name)[0]
        print(content_type)
        try:
            return HttpResponse(file.read(), content_type=content_type)
        except FTPStorageException:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        if exists_file(project_pk, task_pk, filename):
            delete_file(project_pk, task_pk, filename)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
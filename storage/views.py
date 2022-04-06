from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from storages.backends.ftp import FTPStorageException

from .forms import UploadFileForm
from rest_framework.response import Response
from rest_framework import status
from .utils import get_files, delete_file, get_file, exists_file, save_file
import mimetypes
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import FileSerializer
from rest_framework.parsers import MultiPartParser


@swagger_auto_schema(
    methods=['post'],
    manual_parameters=[
        openapi.Parameter('project_pk', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('task_pk', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True)
    ],
    responses={200: openapi.Response('storage response', FileSerializer)}
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def upload_file_view(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.data
        file = request.FILES['file']
        filename = str(int(datetime.now().timestamp())) + '.' + file.name
        save_file(data['project_pk'], data['task_pk'], filename, file)

        return Response(FileSerializer({'filename': filename, 'size': file.size }).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

@swagger_auto_schema(methods=['get'], responses={200: openapi.Response('get files', FileSerializer(many=True))})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_files_view(request, project_pk, task_pk):
    return Response(get_files(project_pk, task_pk))

@swagger_auto_schema(method='get', deprecated=True, operation_id='storage_file_read')
@api_view(['GET'])
@permission_classes([AllowAny])
def get_file_view(request, project_pk, task_pk, filename):
    file = get_file(project_pk, task_pk, filename)
    content_type = mimetypes.guess_type(file.name)[0]
    try:
        return HttpResponse(file.read(), content_type=content_type)
    except FTPStorageException:
        return Response(status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='delete', operation_id='storage_file_delete')
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file_view(request, project_pk, task_pk, filename):
        if exists_file(project_pk, task_pk, filename):
            delete_file(project_pk, task_pk, filename)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

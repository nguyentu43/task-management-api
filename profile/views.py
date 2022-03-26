from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from auth0.utils import get_userinfo
from profile.models import Profile
from profile.serializers import ProfileSerializer
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models.query import Q

from project.models import Project


@csrf_exempt
@swagger_auto_schema(methods=['post'], responses={ 200: openapi.Response('post profile', ProfileSerializer)})
@api_view(['POST'])
def add_profile(request):
    token = request.META['HTTP_AUTHORIZATION']
    userinfo = get_userinfo(token)
    data = {
        'email': userinfo['email'],
        'nickname': userinfo['nickname'],
        'name': userinfo['name'],
        'picture': userinfo['picture'],
        'id': request.user.username
    }

    try:
        profile = Profile.objects.get(email=data['email'])
        if profile.id != data['id']:
            provider = profile.id.split('.')[0]
            return Response('This account has been register with provider ' + provider, 
            status=status.HTTP_406_NOT_ACCEPTABLE)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(**data)

    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['get'], responses={ 200: openapi.Response('get profile', ProfileSerializer)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    try:
        me = Profile.objects.get(pk=request.user.username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ProfileSerializer(me).data)

@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('nickname', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
    openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
    openapi.Parameter('project', openapi.IN_QUERY, type=openapi.TYPE_STRING)
], responses={ 200: openapi.Response('get profiles', ProfileSerializer(many=True))})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_profile(request):
    support_fields = ['nickname', 'email', 'project']

    query_string = {}
    for field in request.META['QUERY_STRING'].split('&'):
        name, value = field.split('=')
        if name not in support_fields:
            continue
        query_string[name] = unquote(value)

    try:
        project_pk = query_string['project']
        project = Project.objects.get(pk=project_pk)
        profiles = {project.owner, *project.participants.all()}
        serializer = ProfileSerializer(profiles, many=True)
    except KeyError:
        profiles = Profile.objects.filter(
            Q(nickname__icontains=query_string['nickname']) | 
            Q(email=query_string['email'])
        )
        serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

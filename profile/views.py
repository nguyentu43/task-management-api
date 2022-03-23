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


@csrf_exempt
@swagger_auto_schema(methods=['post'], responses={ 200: openapi.Response('post profile', ProfileSerializer)})
@api_view(['POST'])
def add_profile(request):
    token = request.META['HTTP_AUTHORIZATION']
    userinfo = get_userinfo(token)
    profile, _ = Profile.objects.get_or_create(
        id=request.user.username,
        defaults={
            'email': userinfo['email'],
            'nickname': userinfo['nickname'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
    )
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
    openapi.Parameter('nickname', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING)
], responses={ 200: openapi.Response('get profiles', ProfileSerializer(many=True))})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_profile(request):
    icontains_fields = ['nickname']

    query_string = {}
    for field in request.META['QUERY_STRING'].split('&'):
        try:
            name, value = field.split('=')
            if name in icontains_fields:
                name = name + '__icontains'
            query_string[name] = unquote(value)
        except IndexError:
            continue

    filters = Q()
    for key, value in query_string.items():
        filters = filters | Q(**{key:value})

    profiles = Profile.objects.filter(filters)
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

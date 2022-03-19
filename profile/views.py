from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from auth0.utils import get_userinfo
from profile.models import Profile
from profile.serializers import ProfileSerializer
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote


@csrf_exempt
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


@api_view(['GET'])
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

    profiles = Profile.objects.filter(**query_string)
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

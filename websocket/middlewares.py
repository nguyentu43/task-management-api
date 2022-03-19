from channels.db import database_sync_to_async
from auth0.utils import get_userinfo
from profile.models import Profile


@database_sync_to_async
def get_user(token):
    userinfo = get_userinfo('Bearer ' + token)
    try:
        return Profile.objects.get(pk=userinfo['sub'].replace('|', '.'))
    except Profile.DoesNotExist:
        return None


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        scope['user'] = await get_user(scope["query_string"][6:].decode('UTF-8'))
        return await self.app(scope, receive, send)

from rest_framework.permissions import IsAuthenticated
from profile.models import Profile


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner.id == request.user.username


class IsParticipantProject(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        p = Profile.objects.get(id=request.user.username)
        return (p in obj.project.participants.all()) or (obj.project.owner == p)


class IsParticipantTask(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        p = Profile.objects.get(id=request.user.username)
        return (p in obj.task.participants.all()) or (obj.task.owner == p)

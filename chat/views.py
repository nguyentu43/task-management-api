from taskmanagement.base.views import ModelViewSetWithPermission
from profile.models import Profile
from .serializers import MessageSerializer
from project.models import Project
from taskmanagement.utils.permissions import IsParticipantProject, IsOwner


class MessageViewSet(ModelViewSetWithPermission):
    permission_classes = [IsParticipantProject]

    permission_classes_by_action = {
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner]
    }

    serializer_class = MessageSerializer

    def get_queryset(self):
        try:
            p = Project.objects.get(pk=self.kwargs['project_pk'])
            return p.message_set.all()
        except Project.DoesNotExist:
            return []

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.username, project_id=self.kwargs['project_pk'])

    def perform_update(self, serializer):
        serializer.save(owner_id=self.request.user.username, project_id=self.kwargs['project_pk'])

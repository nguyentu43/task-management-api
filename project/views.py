from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profile.models import Profile
from .models import Project, Section, Tag
from .serializers import ProjectSerializer, SectionSerializer, TagSerializer
from taskmanagement.base.views import ModelViewSetWithPermission
from taskmanagement.utils.permissions import IsOwner, IsParticipantProject
from django.db.models import Q


class ProjectViewSet(ModelViewSetWithPermission):
    serializer_class = ProjectSerializer

    permission_classes_by_action = {
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner]
    }

    def get_queryset(self):
        user_id = self.request.user.username
        try:
            p = Profile.objects.get(id=user_id)
            return Project.objects.filter(Q(owner_id=p) | Q(participants__in=[p]))
        except Profile.DoesNotExist:
            return []

    def perform_create(self, serializer):
        serializer.save(**self.request.data, owner_id=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(**self.request.data, owner_id=self.request.user.username)


class SectionViewSet(ModelViewSetWithPermission):
    serializer_class = SectionSerializer

    permission_classes = [IsParticipantProject]

    def get_queryset(self):
        print(self.request.data)
        try:
            p = Project.objects.get(pk=self.kwargs['project_pk'])
            return p.section_set.all()
        except Project.DoesNotExist:
            return []

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'])

    def perform_update(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'])


class TagViewSet(ModelViewSetWithPermission):
    serializer_class = TagSerializer

    permission_classes = [IsParticipantProject]

    def get_queryset(self):
        print(self.request.data)
        try:
            p = Project.objects.get(pk=self.kwargs['project_pk'])
            return p.tag_set.all()
        except Project.DoesNotExist:
            return []

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'])

    def perform_update(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'])

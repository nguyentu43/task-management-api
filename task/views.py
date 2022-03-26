from taskmanagement.base.views import ModelViewSetWithPermission
from .serializers import TaskSerializer, TodoItemSerializer, CommentSerializer, ActivitySerializer
from .models import Task, TodoItem, Comment, Activity
from taskmanagement.utils.permissions import IsOwner, IsParticipantTask
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from profile.models import Profile
from django.db.models.query import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TaskViewSet(ModelViewSetWithPermission):
    serializer_class = TaskSerializer

    permission_classes_by_action = {
        'update': [IsOwner],
        'destroy': [IsOwner],
        'partial_update': [IsOwner]
    }

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        serializer.save(**self.request.data, project_id=self.kwargs['project_pk'],
                        owner_id=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(**self.request.data, project_id=self.kwargs['project_pk'],
                        owner_id=self.request.user.username)

    @swagger_auto_schema(methods=['get'], 
        responses={200: openapi.Response('get activities', ActivitySerializer(many=True))}
    )
    @action(detail=True, methods=["GET"], url_path="activities")
    def get_activities(self, request, project_pk=None, pk=None):
        activities = Task.objects.get(pk=pk).activity_set.order_by('-created_at').all()
        return Response(ActivitySerializer(activities, many=True).data, status=status.HTTP_200_OK)

class TodoItemViewSet(ModelViewSetWithPermission):
    serializer_class = TodoItemSerializer
    permission_classes = [IsParticipantTask]

    def get_queryset(self):
        return TodoItem.objects.filter(task_id=self.kwargs['task_pk'])

    def perform_create(self, serializer):
        serializer.save(**self.request.data, owner_id=self.request.user.username, task_id=self.kwargs['task_pk'])

    def perform_update(self, serializer):
        serializer.save(**self.request.data, owner_id=self.request.user.username, task_id=self.kwargs['task_pk'])


class CommentViewSet(ModelViewSetWithPermission):
    serializer_class = CommentSerializer
    permission_classes = [IsParticipantTask]

    permission_classes_by_action = {
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner]
    }

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_pk'])

    def perform_create(self, serializer):
        serializer.save(**self.request.data, owner_id=self.request.user.username, task_id=self.kwargs['task_pk'])

    def perform_update(self, serializer):
        serializer.save(**self.request.data, owner_id=self.request.user.username, task_id=self.kwargs['task_pk'])

class TaskByProfileViewSet(ModelViewSetWithPermission):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        try:
            p = Profile.objects.get(id=self.request.user.username)
            return Task.objects.filter(Q(project__owner=p) | Q(project__participants__in=[p])).distinct()
        except Profile.DoesNotExist:
            return []

class TodoItemByProfileViewSet(ModelViewSetWithPermission):
    serializer_class = TodoItemSerializer
    
    def get_queryset(self):
        try:
            p = Profile.objects.get(id=self.request.user.username)
            return TodoItem.objects.filter(Q(owner=p) | Q(participants__in=[p])).distinct()
        except Profile.DoesNotExist:
            return []


class ActivitiesByProfileViewSet(ModelViewSetWithPermission):
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        try:
            p = Profile.objects.get(id=self.request.user.username)
            return Activity.objects.filter(Q(task__project__owner=p) | Q(task__project__participants__in=[p])).order_by('-created_at').distinct().all()[:15]
        except Profile.DoesNotExist:
            return []

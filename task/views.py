from config.base.views import ModelViewSetWithPermission
from .serializers import TaskSerializer, TodoItemSerializer, CommentSerializer, ActivitySerializer, ReactionSerializer
from .models import Task, TodoItem, Comment, Activity
from config.utils.permissions import IsOwner, IsParticipantTask
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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

    @action(detail=True, methods=["GET"], url_path="activities")
    def get_activities(self, request, project_pk=None, pk=None):
        activities = Task.objects.get(pk=pk).activity_set.all()
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


class ReactionViewSet(ModelViewSetWithPermission):
    serializer_class = ReactionSerializer

    permission_classes_by_action = {
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner]
    }

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs['comment_pk']).reactions.all()
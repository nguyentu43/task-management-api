from rest_framework.serializers import ModelSerializer
from .models import Activity, Reaction, Task, Comment, TodoItem
from project.serializers import SectionSerializer, TagSerializer, ProjectSerializer
from profile.serializers import ProfileSerializer


class ReactionSerializer(ModelSerializer):
    owner = ProfileSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    section = SectionSerializer(read_only=True)
    owner = ProfileSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TodoItemSerializer(ModelSerializer):
    participants = ProfileSerializer(many=True, read_only=True)
    owner = ProfileSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TodoItem
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    owner = ProfileSerializer(read_only=True)
    reactions = ReactionSerializer(many=True, read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ActivitySerializer(ModelSerializer):
    reactions = ReactionSerializer(many=True, read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'

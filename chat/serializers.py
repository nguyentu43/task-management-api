from rest_framework.serializers import ModelSerializer
from .models import Message
from profile.serializers import ProfileSerializer
from project.serializers import ProjectSerializer


class MessageSerializer(ModelSerializer):
    owner = ProfileSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

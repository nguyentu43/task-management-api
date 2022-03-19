from .models import Project, Section, Tag
from rest_framework.serializers import ModelSerializer
from profile.serializers import ProfileSerializer


class ProjectSerializer(ModelSerializer):
    owner = ProfileSerializer(many=False, read_only=True)
    participants = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class SectionSerializer(ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Section
        fields = '__all__'


class TagSerializer(ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'

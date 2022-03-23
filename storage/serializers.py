from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    size = serializers.IntegerField()
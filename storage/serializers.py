from rest_framework import serializers

class FileSerializer(serializers):
    name = serializers.CharField(max_length=255)
    url = serializers.URLField()
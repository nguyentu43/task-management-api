from django.db import models
from profile.models import Profile
from project.models import Project

# Create your models here.
class Message(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=255,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
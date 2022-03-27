from django.db import models
from profile.models import Profile
from django.db.models.signals import pre_save
from taskmanagement.db.receivers import set_updated_at_pre_save


class Project(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='project_owner')
    participants = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    color = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    color = models.CharField(max_length=25)

    def __str__(self):
        return self.name


pre_save.connect(set_updated_at_pre_save, sender=Project)

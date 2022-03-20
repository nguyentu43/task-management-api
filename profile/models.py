from django.db import models
from django.db.models.signals import pre_save
from taskmanagement.db.receivers import set_updated_at_pre_save


class Profile(models.Model):
    email = models.EmailField(unique=True, blank=False, null=False)
    id = models.CharField(max_length=100, blank=False, null=False, primary_key=True)
    nickname = models.CharField(max_length=255, blank=False, null=False)
    picture = models.URLField()
    name = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname


pre_save.connect(set_updated_at_pre_save, sender=Profile)

# pre_save new profile
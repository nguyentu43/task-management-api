from django.db import models
from django.db.models.signals import pre_save, post_save
from django.forms import model_to_dict

from taskmanagement.db.receivers import set_updated_at_pre_save
from profile.models import Profile
from project.models import Tag, Section, Project

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class TaskStatus(models.TextChoices):
    Complete = 'Complete'
    UnComplete = 'UnComplete'
    Draft = 'Draft'


class Task(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False, null=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    due_datetime = models.DateTimeField(blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices=TaskStatus.choices, default=TaskStatus.UnComplete, null=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    due_datetime = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(Profile, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    is_done = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Activity(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile, blank=True, related_name='like_comments')

    def __str__(self):
        return self.content

pre_save.connect(set_updated_at_pre_save, sender=Task)
pre_save.connect(set_updated_at_pre_save, sender=TodoItem)
pre_save.connect(set_updated_at_pre_save, sender=Comment)


def create_activity(sender, instance, *args, **kwargs):
    created = kwargs['created']
    action_text = 'Update'

    if created:
        action_text = 'New'

    title = '{} {}'.format(action_text, sender.__name__)
    type = sender.__name__

    if type == 'Task' and created:
        Activity.objects.create(
            title=title,
            type=type,
            content='{} has created a task "{}"'.format(instance.owner.nickname, instance.title),
            task_id=instance.id
        )

    if type == 'Comment' and created:
        Activity.objects.create(
            title=title,
            type=type,
            content='{} has comment "{}"'.format(instance.owner.nickname, instance.content),
            task_id=instance.task_id
        )

    if type == 'TodoItem':
        if not instance.is_done and created:
            Activity.objects.create(
                title=title,
                type=type,
                task_id=instance.task_id,
                content='{} has created a todo "{}"'.format(instance.owner, instance.title)
            )
        if instance.is_done:
            Activity.objects.create(
                title=title,
                type=type,
                task_id=instance.task_id,
                content='{} has checked done todo "{}"'.format(instance.owner, instance.title)
            )


post_save.connect(create_activity, sender=TodoItem)
post_save.connect(create_activity, sender=Comment)
post_save.connect(create_activity, sender=Task)


def send_activity_ws(sender, instance, *args, **kwargs):
    user_set = set(instance.task.project.participants.values_list('id', flat=True))
    user_set.add(instance.task.project.owner.id)

    text_data = json.dumps(model_to_dict(instance));

    try:
        for user_id in user_set:
            room_group_name = 'activity_{}'.format(user_id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {'type': 'send_activity', 'activity': text_data}
            )
    except ConnectionRefusedError:
        print('Redis connect failed')

post_save.connect(send_activity_ws, sender=Activity)

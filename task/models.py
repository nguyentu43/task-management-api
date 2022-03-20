from django.db import models
from django.db.models.signals import pre_save, post_save

from taskmanagement.db.receivers import set_updated_at_pre_save
from profile.models import Profile
from project.models import Tag, Section, Project

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Create your models here.

class ReactionType(models.TextChoices):
    Love = 'Love'
    Like = 'Like'
    Smile = 'Smile'


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
    due_datetime = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices=TaskStatus.choices, default=TaskStatus.UnComplete, null=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # attachments

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order = models.IntegerField(null=False, blank=False)
    due_datetime = models.DateTimeField(auto_now_add=True)
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

    def __str__(self):
        return self.content

class Reaction(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=25, choices=ReactionType.choices, default=ReactionType.Like)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.type

pre_save.connect(set_updated_at_pre_save, sender=Task)
pre_save.connect(set_updated_at_pre_save, sender=TodoItem)
pre_save.connect(set_updated_at_pre_save, sender=Comment)
pre_save.connect(set_updated_at_pre_save, sender=Reaction)


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

    if type == 'Comment':
        Activity.objects.create(
            title=title,
            type=type,
            content='{} has comment "{}"'.format(instance.owner.nickname, instance.content),
            task_id=instance.task_id
        )

    if type == 'TodoItem':
        if instance.is_done:
            Activity.objects.create(
                title=title,
                type=type,
                content='{} has been done'.format(instance.title),
                task_id=instance.task_id
            )
        if not instance.is_done and created:
            Activity.objects.create(
                title=title,
                type=type,
                task_id=instance.task_id,
                content='{} has created a todo "{}"'.format(instance.owner, instance.title)
            )


post_save.connect(create_activity, sender=TodoItem)
post_save.connect(create_activity, sender=Comment)
post_save.connect(create_activity, sender=Task)


def send_activity_ws(sender, instance, *args, **kwargs):
    user_set = set(instance.task.project.participants.values_list('id', flat=True))
    user_set.add(instance.task.project.owner.id)

    for user_id in user_set:
        room_group_name = 'activity_{}'.format(user_id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            instance
        )


post_save.connect(send_activity_ws, sender=Activity)

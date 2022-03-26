from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from task.models import Activity
from .serializers import ActivitySerializer


def send_activity_ws(sender, instance, *args, **kwargs):
    user_set = set(instance.task.project.participants.values_list('id', flat=True))
    user_set.add(instance.task.project.owner.id)

    try:
        for user_id in user_set:
            room_group_name = 'activity_{}'.format(user_id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {'type': 'send_activity', 'activity': ActivitySerializer(instance).data}
            )
    except ConnectionRefusedError:
        print('Redis connect failed')

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
        if not instance.is_done and created:
            Activity.objects.create(
                title=title,
                type=type,
                task_id=instance.task_id,
                content='{} has created a todo "{}"'.format(instance.owner, instance.title)
            )
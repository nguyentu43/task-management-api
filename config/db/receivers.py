from django.utils import timezone


def set_updated_at_pre_save(sender, instance, *args, **kwargs):
    instance.updated_at = timezone.now()



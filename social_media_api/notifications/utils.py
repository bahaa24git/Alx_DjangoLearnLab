from django.contrib.contenttypes.models import ContentType


def notify(*, actor, recipient, verb: str, target=None):
    """
    Create a notification. Usage:
        notify(actor=request.user, recipient=post.author, verb="liked your post", target=post)
    """
    from .models import Notification

    payload = {"actor": actor, "recipient": recipient, "verb": verb}
    if target is not None:
        payload["target_ct"] = ContentType.objects.get_for_model(target)
        payload["target_id"] = target.pk
    return Notification.objects.create(**payload)

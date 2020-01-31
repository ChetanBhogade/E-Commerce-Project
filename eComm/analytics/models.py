from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .signals import object_viewed_signal

# Create your models here.

User = settings.AUTH_USER_MODEL

class ObjectViewedManager(models.Manager):
    pass

class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address      = models.CharField(max_length=220, null=True, blank=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return f"{self.content_object}"[:20]#" : - Viewed on {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


def object_viewed_signal_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    user = None
    if request.user.is_authenticated:
        user = request.user
    new_object_view_object = ObjectViewed.objects.create(
        user = user,
        ip_address = request.META.get('REMOTE_ADDR', None),
        content_type = c_type,
        object_id = instance.id,
    )

object_viewed_signal.connect(object_viewed_signal_receiver)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address   = models.CharField(max_length=220, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_object} : - Viewed on {self.timestamp}"


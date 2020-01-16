from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Address(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1   = models.CharField(max_length=120)
    address_line2   = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    state           = models.CharField(max_length=120)
    country         = models.CharField(max_length=120)
    pincode         = models.CharField(max_length=120)

    def __str__(self):
        return self.user



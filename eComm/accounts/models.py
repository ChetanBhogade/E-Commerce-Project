from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.

User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        obj = None 
        created = False
        user = request.user
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        return obj, created

class BillingProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    email       = models.EmailField()
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

def post_save_email_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(post_save_email_receiver, sender=User)

###########################################################################################################

class AddressManager(models.Manager):
    pass

class Address(models.Model):
    billing_profile  = models.ForeignKey(BillingProfile, null=True, on_delete=models.CASCADE)
    address_line1   = models.CharField(max_length=120)
    address_line2   = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    state           = models.CharField(max_length=120)
    country         = models.CharField(max_length=120)
    pincode         = models.CharField(max_length=120)

    objects = AddressManager()

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return f"{self.address_line1} {self.address_line2}, {self.city}, {self.state}, {self.country}, {self.pincode}"


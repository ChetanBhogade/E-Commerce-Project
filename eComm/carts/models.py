from django.db import models
from django.conf import settings
from django.db.models.signals import m2m_changed

from products.models import Product
# Create your models here.

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    pass

class Cart(models.Model):
    id          = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    products    = models.ManyToManyField(Product, blank=True)
    total       = models.IntegerField(default=0)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for i in products:
            total += i.price
        if instance.total != total:
            instance.total = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


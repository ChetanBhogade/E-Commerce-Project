from django.db import models
from django.db.models.signals import pre_save, post_save

from carts.models import Cart
from eComm.utils import unique_order_id_generator
# Create your models here.

class OrderManager(models.Manager):
    def new_or_get(self, cart_obj):
        created = False
        obj = None
        qs = Order.objects.filter(cart=cart_obj)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = Order.objects.create(cart=cart_obj)
            created = True
        return obj, created

class Order(models.Model):
    order_id        = models.CharField(max_length=50, primary_key=True)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping_cost   = models.IntegerField(default=10)
    total           = models.IntegerField(default=0)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_cost = self.shipping_cost
        new_total = cart_total + shipping_cost
        self.total = new_total
        self.save()
        return new_total



def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance=instance)

pre_save.connect(pre_save_order_id_receiver, sender=Order)


def post_save_cart_total_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        qs = Order.objects.filter(cart__id=cart_obj.id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total_receiver, sender=Cart)


def post_save_order_total_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print("Updating.....")
        instance.update_total()

post_save.connect(post_save_order_total_receiver, sender=Order)
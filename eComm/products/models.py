import random
import os
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from eComm.utils import unique_slug_generator

# Create your models here.

def get_file_extension(filepath):
    basename = os.path.basename(filepath)
    name, ext = basename.split('.')
    return name, ext

def upload_file_path(instance, filename):
    new_filename = random.randint(1, 464654165)
    name, ext = get_file_extension(filename)
    final_filename = f'{new_filename}.{ext}'
    return f'products/{new_filename}/{final_filename}'


class ProductManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

CATEGORY_CHOICES = (
    ('Mobiles', 'mobiles'),
    ('Accessories', 'accessories'),
    ('Watches', 'watches'),
    ('Shirts', 'shirts'),
    ('Shoes', 'shoes'),
    ('Others', 'others'),

)
class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    category    = models.CharField(max_length=120, choices=CATEGORY_CHOICES)
    price       = models.IntegerField(default=39)
    image       = models.ImageField(upload_to=upload_file_path, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return f'/products/{self.slug}/'
        return reverse("products:product-detail", kwargs={"slug":self.slug})


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)
    
pre_save.connect(product_pre_save_receiver, sender=Product)



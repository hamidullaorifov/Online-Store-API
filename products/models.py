from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)


User = get_user_model()
class ProductItem(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)


class Product(models.Model):
    product = models.OneToOneField(ProductItem,on_delete=models.CASCADE,related_name='product')
    quantity = models.PositiveIntegerField(default=0)

@receiver(post_save,sender=ProductItem)
def prod_item_receiver(sender, instance, **kwargs):
    product = Product.objects.get_or_create(product=instance)


class Review(models.Model):
    product = models.ForeignKey(ProductItem,on_delete=models.CASCADE,related_name='reviews')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.TextField(blank=True,null=True)
    created = created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-updated',)


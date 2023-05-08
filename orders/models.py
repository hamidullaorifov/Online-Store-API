from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductItem
User = get_user_model()
# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=(
        ('P','Pending'),
        ('D','Delivered')
    ))
    class Meta:
        ordering = ('-updated',)

    @property
    def total_price(self):
        return sum([order_item.totel for order_item in self.order_items.all()])

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(ProductItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.quantity*(self.product.price-self.product.discount)

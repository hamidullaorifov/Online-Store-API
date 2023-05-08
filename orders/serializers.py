from rest_framework import serializers
from rest_framework.response import Response
from .models import Order, OrderItem
from products.models import ProductItem
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id', 'customer', 'created', 'updated', 'status', 'total_price', 'order_items')
    def get_total_price(self, obj):
        total_price = 0
        for item in obj.order_items.all():
            total_price += item.quantity * (item.product.price-item.product.discount)
        return total_price
class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'order')
        extra_kwargs = {'order':{'required':False}}

class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'quantity')

class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'total_price', 'order_items')
        extra_kwargs = {'total_price':{'read_only':True}}
    def get_total_price(self, obj):
        total_price = 0
        for item in obj.order_items.all():
            total_price += item.quantity * (item.product.price-item.product.discount)
        return total_price

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status')
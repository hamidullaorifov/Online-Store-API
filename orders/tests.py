from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Order
from products.models import Product,ProductItem
from django.contrib.auth import get_user_model
from .serializers import *
User = get_user_model()
class OrderTests(TestCase):
    def setUp(self):
        self.product = ProductItem.objects.create(
            brand='Lenovo',
            name = 'Laptop',
            price = 799.99
        )
        self.client = APIClient()
        self.customer = User.objects.create(username='testuser',password='testpass',email='test@example.com')
        self.order = Order.objects.create(
            customer = self.customer,
            status='P',
            total_price=100.0,
        )
        self.valid_payload = {
            "customer":self.customer.pk,
            "status":"P",
            "total_price":255,
            "order_items":[
                {
                    "product":self.customer.pk,
                    "quantity":2
                }
            ]
        }
        self.invalid_payload_create_order = {
            'customer': '',
            'status': 'P',
            'total_amount': 200.0,
            "order_items":[
                {
                    "product":5,
                    "quantity":2
                },
                {
                    "product":6,
                    "quantity":3
                }
            ]
        }
        self.valid_data_update_order = {
            'id':self.order.pk,
            'status':'D'
        }
        self.invalid_data_update_order = {
            'id':self.order.pk,
            'status':'Invalid status'
        }

    def test_get_orders(self):
        response = self.client.get(reverse('order-list'))
        orders = Order.objects.all()
        serializer_data = OrderSerializer(orders, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_order(self):
        response = self.client.post(
            reverse('order-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_order(self):
        response = self.client.post(
            reverse('order-list'),
            data=self.invalid_payload_create_order,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_order(self):
        response = self.client.put(
            reverse('order-detail', kwargs={'pk': self.order.pk}),
            data=self.valid_data_update_order,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['status'],self.valid_data_update_order['status'])

    def test_update_invalid_order(self):
        response = self.client.put(
            reverse('order-detail', kwargs={'pk': self.order.pk}),
            data=self.invalid_data_update_order,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_order(self):
        response = self.client.delete(
            reverse('order-detail', kwargs={'pk': self.order.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

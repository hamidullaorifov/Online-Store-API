from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Order, OrderItem
from products.models import ProductItem
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAdminUser
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
                        OrderSerializer, 
                        OrderItemSerializer, 
                        OrderCreateSerializer, 
                        OrderUpdateSerializer,
                        OrderItemCreateSerializer, 
                        OrderItemUpdateSerializer
                        )




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        queryset = Order.objects.all()
        user_id = query_params.get('user')
        status = query_params.get('status','').upper()
        ordering = query_params.get('ordering')
        if user_id:
            queryset = queryset.filter(customer=user_id)
        if status:
            queryset = queryset.filter(status=status)
        if ordering:
            queryset = queryset.order_by(f'-{ordering}')

        serializer = OrderSerializer(queryset,many=True)
        return Response(serializer.data)
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return OrderSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return OrderUpdateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        order_items = data.pop('order_items')
        for item in order_items:
            product_item = ProductItem.objects.filter(pk=item['product']).first()
            if product_item:
                product = product_item.product
                if product.quantity < item['quantity']:
                    response_data = {
                        "message":"There is not enough product",
                        'product':product_item.name,
                        'available':product_item.product.quantity
                    }
                    return Response(data=response_data,status=400)
                product.quantity = product.quantity-item['quantity']
                product.save()
            else:
                return Response({'message':"Product not found"},status=404)
        order = None
        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid(raise_exception=True):
            order = order_serializer.save()
        for item_data in order_items:
            item_data['order'] = order.pk
            order_item_serializer = OrderItemCreateSerializer(data=item_data)
            if order_item_serializer.is_valid(raise_exception=True):
                order_item = order_item_serializer.save()
        return Response(OrderCreateSerializer(order).data,status=201)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderItemCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return OrderItemUpdateSerializer
        else:
            return OrderItemSerializer

class UserOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Order.objects.filter(customer=user_id)
        return queryset


order_user_parameter= openapi.Parameter('user',openapi.IN_QUERY,type=openapi.TYPE_STRING)
order_status_parameter= openapi.Parameter('status',openapi.IN_QUERY,type=openapi.TYPE_STRING)

@method_decorator(name='get',decorator=swagger_auto_schema(manual_parameters=[order_user_parameter,order_status_parameter]))
class OrderFilterView(ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        queryset = Order.objects.all()
        query_params = self.request.query_params or {}
        user_id = query_params.get('user')
        status = query_params.get('status')
        if user_id:
            queryset = queryset.filter(customer=user_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
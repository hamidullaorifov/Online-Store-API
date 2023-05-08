from .models import Product,ProductItem,Review,Category
from .permissions import ReviewIsOwnerOrReadOnly
from rest_framework import viewsets,views
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,UpdateAPIView
from .permissions import IsAdminOrReadOnly
from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (  ProductUpdateSerializer,
                            ProductItemSerializer,
                            ReviewSerializer,
                            ReviewUpdateSerializer,
                            CategorySerializer,
                            AddProductSerializer)


search_parameter= openapi.Parameter('search',openapi.IN_QUERY,type=openapi.TYPE_STRING)
price_from_parameter= openapi.Parameter('price_from',openapi.IN_QUERY,type=openapi.TYPE_NUMBER)
price_to_parameter= openapi.Parameter('price_to',openapi.IN_QUERY,type=openapi.TYPE_NUMBER)
category_parameter= openapi.Parameter('category',openapi.IN_QUERY,type=openapi.TYPE_STRING)



# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    class Meta:
        model = ProductItem
    queryset = ProductItem.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return ProductUpdateSerializer
        return ProductItemSerializer
    


@method_decorator(name='get',decorator=swagger_auto_schema(manual_parameters=[search_parameter,price_from_parameter,price_to_parameter,category_parameter]))
class ProductSearchView(ListAPIView):
    serializer_class = ProductItemSerializer
    def get_queryset(self):
        queryset = ProductItem.objects.all()
        query_params = self.request.query_params
        query = query_params.get('search')
        price_from = query_params.get('price_from')
        price_to = query_params.get('price_to')
        category = query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(brand__icontains=query))
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        return queryset





class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [ReviewIsOwnerOrReadOnly]
    class Meta:
        model = Review
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return ReviewUpdateSerializer
        return ReviewSerializer
        

class ProductReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['product_id']
        queryset = Review.objects.filter(product=pk)
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by('-'+ordering)
        return queryset
class UserReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['user_id']
        queryset = Review.objects.filter(owner=pk)
        return queryset

class AddProductView(views.APIView):
    serializer_class = AddProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    @swagger_auto_schema(request_body=AddProductSerializer)
    def post(self,request,*args,**kwargs):
        product_id = kwargs.get('product_id')
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            product_item = ProductItem.objects.get(pk=product_id)
            quantity = data['quantity']
            product = product_item.product
            product.quantity = product.quantity+quantity
            product.save()
            return Response(data=ProductItemSerializer(product_item).data,status=200)


class CategoryViewSet(viewsets.ModelViewSet):
    class Meta:
        model = Category
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
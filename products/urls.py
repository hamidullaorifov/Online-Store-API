from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,ProductSearchView,CategoryViewSet,AddProductView
router = DefaultRouter()

router.register('category',CategoryViewSet,basename='category')
router.register('',ProductViewSet,basename='product')
urlpatterns = [
    path('search/',ProductSearchView.as_view(),name='search'),
    path('add/<int:product_id>',AddProductView.as_view(),name='add_product'),
    path('',include(router.urls)),
    ]

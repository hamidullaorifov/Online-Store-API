
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter
from products.views import ReviewViewSet
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

credentials = {
'username' : 'staffuser',
'password' : 'staffuser'
}
schema_view = get_schema_view(
   openapi.Info(
      title="Online Store API",
      default_version='v1',
      description=f"This is Online Store API that sells products.\nSome endpoints can be used only by staff users. \nTo test this endpoints use this data and get access token: {credentials}",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="orifovhamidulla@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   authentication_classes=[JWTAuthentication]
)
review_router = DefaultRouter()
review_router.register('',ReviewViewSet,basename='reviews')

urlpatterns = [

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),


    path('api/users/',include('users.urls')),
    path('api/products/',include('products.urls')),

    path('api/reviews/',include('products.review_urls')),

    path('api/orders/',include('orders.urls')),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
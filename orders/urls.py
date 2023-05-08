from .views import OrderViewSet,OrderFilterView
from rest_framework.routers import DefaultRouter
from django.urls import path,include

router = DefaultRouter()
router.register('',OrderViewSet,basename='order')
urlpatterns = [
    path('filter/',OrderFilterView.as_view()),
    path('',include(router.urls))
]

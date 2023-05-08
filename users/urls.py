from django.urls import path,include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register('',views.UserApiViewSet,basename='users')

urlpatterns = [
    path('search/',views.UserSearchView.as_view(),name='user_search'),
    path('',include(router.urls)),
]
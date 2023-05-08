from django.urls import path,include
from rest_framework.routers import DefaultRouter
from products.views import ReviewViewSet,ProductReviewsView,UserReviewsView

review_router = DefaultRouter()
review_router.register('',ReviewViewSet,basename='reviews')

urlpatterns = [
    path('product/<int:product_id>',ProductReviewsView.as_view()),
    path('user/<int:user_id>',UserReviewsView.as_view()),
    path('',include(review_router.urls)),
]
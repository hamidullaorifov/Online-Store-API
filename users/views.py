from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
User = get_user_model()


# Create your views here.


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    class Meta:
        model = User

query = openapi.Parameter('query',openapi.IN_QUERY,type=openapi.TYPE_STRING)
@method_decorator(name='get',decorator=swagger_auto_schema(manual_parameters=[query]))
class UserSearchView(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        query = self.request.query_params.get('query',None)
        if query:
            queryset = queryset.filter(Q(username__icontains=query) | Q(email__icontains=query))
        return queryset
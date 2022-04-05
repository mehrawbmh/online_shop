from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import BasicAuthentication, CSRFCheck
from rest_framework.serializers import HyperlinkedRelatedField
from rest_framework.generics import RetrieveAPIView
from core.models import User
from .models import Customer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'is_staff']


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    user = HyperlinkedRelatedField(view_name='user-detail', read_only=True)


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    queryset = User.objects.all()


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser, ]
    authentication_classes = [BasicAuthentication]

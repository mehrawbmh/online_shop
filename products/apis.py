from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'price', 'category']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


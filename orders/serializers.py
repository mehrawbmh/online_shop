from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'count', 'product', 'related_product', 'related_cart']
    product = serializers.PrimaryKeyRelatedField(
        required=True,
        write_only=True,
        queryset=Product.objects.all()
    )
    related_product = serializers.StringRelatedField(
        source='product',
    )
    related_cart = serializers.StringRelatedField(
        source='cart'
    )



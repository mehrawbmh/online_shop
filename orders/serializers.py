from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='customer.user.first_name')

    class Meta:
        model = Cart
        fields = '__all__'


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
    related_cart = serializers.HyperlinkedRelatedField(
        view_name='cart-detail',
        source='cart',
        read_only=True
    )

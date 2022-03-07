import rest_framework.permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils import CsrfExemptSessionAuthentication
from .models import CartItem, Cart
from .serializers import CartItemSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class CartItemAPIView(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        last_cart = self.request.user.customer.cart_set.last()
        former_products = last_cart.items.values_list('product_id', flat=True)
        prod = serializer.validated_data['product']
        if prod.id in former_products:
            return Response({'400': 'This product is already in your cart items. update it!'}, status=400)
        if last_cart and last_cart.status == 'unfinished':
            serializer.save(cart=last_cart)
        else:
            cart = Cart.objects.create(
                customer=self.request.user.customer,
                address=self.request.user.customer.address_set.last()
            )
            serializer.save(cart=cart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user)

    def post(self, request, *args, **kwargs):
        user_items = self.get_queryset().order_by('-id')
        product_id = self.request.POST.get('product', None)
        product_id = int(product_id)
        if product_id:
            for cart_item in user_items:
                if cart_item.product.id == product_id:
                    return Response({'cart_item_id': cart_item.id}, status=200)
            return Response({'404', 'cart item for user with this product not found'}, status=404)
        else:
            return Response({'404': 'No such product with this id found'}, status=404)

    def delete(self, request, *args, **kwargs):
        print(kwargs)
        return super().delete(request, *args, **kwargs)

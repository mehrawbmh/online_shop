from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem, Cart
from .serializers import CartItemSerializer
from rest_framework.generics import ListCreateAPIView


class CartItemAPIView(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        last_cart = self.request.user.customer.cart_set.last()
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


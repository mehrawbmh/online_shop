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

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print('data:',request.data)
        serializer = self.get_serializer(data=request.data)
        print('former:',serializer)

        print('now:', serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        print('args:',args)
        print('kw:', kwargs)
        last_cart = self.request.user.customer.cart_set.last()
        if last_cart and last_cart.status == 'unfinished':
            kwargs['data']['cart'] = last_cart
        else:
            cart = Cart.objects.create(
                customer=self.request.user.customer,
                address=self.request.user.customer.address_set.last()
            )
            kwargs['data']['cart'] = cart
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

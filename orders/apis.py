import rest_framework.permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils import CsrfExemptSessionAuthentication
from products.models import Product
from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, RetrieveAPIView
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
        former_products = last_cart.items.values_list('product_id', flat=True) if last_cart else []
        prod = serializer.validated_data['product']
        if prod.id in former_products:
            last_cart: Cart
            cart_item = last_cart.items.get(product=prod)
            cart_item.count += 1
            cart_item.save()
        elif last_cart and last_cart.status == 'unfinished':
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
        if product_id:
            product_id = int(product_id)
            product = get_object_or_404(Product.objects.filter(is_active=True).all(), id=product_id)
            for cart_item in user_items:
                if cart_item.product.id == product.id:
                    return Response({'cart_item_id': cart_item.id}, status=200)
            return Response({'404', 'cart item for user with this product not found'}, status=404)
        else:
            return Response({'404': 'You have to send product id with key "product"'}, status=404)

    def delete(self, request, *args, **kwargs):
        print(kwargs)
        return super().delete(request, *args, **kwargs)


class SetCookieForCartItem(APIView):

    def post(self, request, *args, **kwargs):
        prod_id = request.POST.get('product', None)
        if prod_id:
            prod = get_object_or_404(Product.objects.filter(is_active=True).all(), id=prod_id)
            cookie_exist = self.check_cookie_exist(prod.id)
            if cookie_exist:
                resp = Response(status=201)
                resp.set_cookie(f'prod{prod_id}', str(int(cookie_exist) + 1))
                return resp
            else:
                resp = Response(status=201)
                resp.set_cookie(f'prod{prod_id}', '1')
                return resp
        else:
            return Response(status=404, data={'404': {'You have to pass "product" key in your request body'}})

    def check_cookie_exist(self, product_id):
        print(self.request.COOKIES.get(f'prod{product_id}'))
        return self.request.COOKIES.get(f'prod{product_id}', None)

    def delete(self, *args, **kwargs):
        product_id = kwargs.get('pk')
        cookie = self.request.COOKIES.get(f'prod{product_id}')
        resp = Response(status=status.HTTP_204_NO_CONTENT)
        if cookie:
            resp.delete_cookie(f'prod{product_id}')
        return resp


class CartDetailAPIView(RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

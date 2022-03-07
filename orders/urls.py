from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .apis import CartItemAPIView

urlpatterns = [
    path('basket_item', csrf_exempt(CartItemAPIView.as_view()), name='cart_api')
]

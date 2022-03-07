from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .apis import CartItemAPIView, CartItemDetailAPIView

urlpatterns = [
    path('basket_items/', csrf_exempt(CartItemAPIView.as_view()), name='cart_item_api'),
    path('basket_item_detail/<int:pk>/', csrf_exempt(CartItemDetailAPIView.as_view()), name='cart_item_detail_api')
]

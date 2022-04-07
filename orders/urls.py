from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .apis import CartItemAPIView, CartItemDetailAPIView, SetCookieForCartItem, CartDetailAPIView, CartItemCountChange
from .views import CartView


urlpatterns = [
    path('basket_items/', CartItemAPIView.as_view(), name='cart_item_api'),
    path('basket_item_detail/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart_item_detail_api'),
    path('set_cart_cookie/', SetCookieForCartItem.as_view(), name='set_cookie_for_cart_item'),
    path('delete_cart_cookie/<int:pk>/', SetCookieForCartItem.as_view(), name='delete_cookie_for_cart_item'),
    path('basket/', CartView.as_view(), name='basket_detail'),
    path('basket-detail/<int:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('basket-quantity', CartItemCountChange.as_view(), name='cartitem_change_count')
]

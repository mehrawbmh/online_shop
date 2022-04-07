from django.urls import path
from django.views.generic.base import RedirectView

from .views import ProductListView, CategoryDetailView, ProductDetailView, CheckOffCodeView
from .apis import ProductViewSet

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('index/', RedirectView.as_view(url='/'), name='index-redirect'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('check_customer_offcode/', CheckOffCodeView.as_view(), name='check_off_code'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products_api/', ProductViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }))
]

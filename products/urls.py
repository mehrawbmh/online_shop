from django.urls import path
from .views import ProductListView, CategoryDetailView, ProductDetailView
from .apis import ProductViewSet

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('index/', ProductListView.as_view(), name='index'),  # TODO redirect view!
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products_api/', ProductViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }))
]

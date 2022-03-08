from django.urls import path
from .views import ProductListView, CategoryDetailView, ProductDetailView
urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('index/', ProductListView.as_view(), name='index'), #TODO redirect view!
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]


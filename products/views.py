from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product


class ProductListView(ListView):
    template_name = 'products/index.html'
    model = Product
    queryset = Product.objects.filter(is_active=True).all()
    context_object_name = 'products'

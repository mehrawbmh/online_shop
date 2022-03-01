from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.models import Product, Category


class ProductListView(ListView):
    template_name = 'products/index.html'
    model = Product
    queryset = Product.objects.filter(is_active=True).all()
    context_object_name = 'products'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs, object_list=object_list)
        context['categories'] = Category.objects.filter(is_active=True).all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'products/category_detail.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

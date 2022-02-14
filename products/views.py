from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class ProductListView(TemplateView):
    template_name = 'products/index.html'

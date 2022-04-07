from audioop import reverse

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView

from orders.models import Cart
from products.models import Product, Category, OffCode


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


class CheckOffCodeView(View):
    def post(self, req):
        offcode = self.request.POST.get('offcode')
        if offcode:
            try:
                obj = OffCode.objects.get(unique_token=offcode)
            except OffCode.DoesNotExist:
                obj = None
            cart = self.request.user.customer.cart_set.last()
            cart.off_code = obj
            cart.save()
            data = {
                'valid': 2,
                'cart': cart,
                'items': cart.items.all(),
                'totalprize': cart.final_prize_calc(),
                'profit': cart.order_discount
            }
            try:
                cart = cart if cart.status == 'unfinished' else None
                if cart and obj and obj.is_valid(offcode):
                    return render(req, 'orders/basket.html', data)
                else:
                    raise ValidationError('this code does not exist')
            except ValidationError:
                data['valid'] = 0
                data['items'] = []
                data['totalprize'] = 0
                data['profit'] = 0
                return render(req, 'orders/basket.html', context=data)
        return HttpResponse(status=404)

    def get(self, req):
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, id=self.request.GET.get('cartid'))
            if cart in self.request.user.customer.cart_set.all():
                cart.status = 'unpaid'
                cart.save()
                return redirect(reverse_lazy('index'))
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=403)

from django.shortcuts import render
from django.views import View
from .models import CartItem, Cart


class CartView(View):

    def get(self, request):
        data = dict() #context!
        if request.user.is_authenticated:
            cart = self.request.user.customer.cart_set.last()
            data = {'cart': cart}
            if cart:
                data['items'] = CartItem.objects.filter(cart=cart)
            else:
                data['items'] = None
        else:
            data['cart'] = None
            print(request.COOKIES)

        return render(request, 'orders/basket.html', data)

# TODO replace it with api

from django.shortcuts import render
from django.views import View

from products.models import Product
from .models import CartItem, Cart


class CartView(View):

    def get(self, request):
        data = dict()  # context!
        if request.user.is_authenticated:
            cart = self.request.user.customer.cart_set.last()
            cart: Cart
            data = {'cart': cart}
            if cart:
                data['items'] = CartItem.objects.filter(cart=cart)
                data['totalprize'] = cart.final_prize_calc()
            else:
                data['items'] = None
        else:
            data['cart'] = None
            items = list()
            sum = 0
            for key, value in self.request.COOKIES.items():
                key: str
                if key.startswith('prod'):
                    prod_id = int(key[4:])
                    product = Product.objects.get(id=prod_id)
                    items.append((product, value))
                    sum += int(product.final_price) * int(value)
            data['items'] = items
            data['totalprize'] = str(sum)

        return render(request, 'orders/basket.html', data)

# TODO replace it with api

from django.db import models
from core.models import BaseModel
from customers.models import Address, Customer
from products.models import Product, _, OffCode
from datetime import timedelta

class CartItem(BaseModel):
    class Meta:
        verbose_name = _("Basket item")

    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        verbose_name=_("Product")
    )
    count = models.SmallIntegerField(
        verbose_name=_("Number of product"),
        default=1
    )  # TODO: check available number
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        verbose_name=_("Basket"),
        related_name='items'
    )

    @property
    def final_price(self):
        return self.product.final_price * int(self.count)

    def __repr__(self):
        return f"for {self.cart} => {self.count} of {self.product}"


class Cart(BaseModel):
    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    off_code = models.ForeignKey(
        OffCode,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("OffCode")
    )
    status = models.CharField(
        max_length=20,
        choices=[('unfinished', "Unfinished"), ('unpaid', 'Unpaid'), ('paid', 'Paid')],
        verbose_name=_("Basket Status"),
        default='unfinished'
    )
    address = models.ForeignKey(
        to=Address,
        on_delete=models.RESTRICT
    )
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.DO_NOTHING
    )

    # TODO: create a receipt when status of cart is paid

    def __repr__(self):
        try:
            return f"Cart {self.id}({self.status})"
        except:
            return f"Temporary Cart"

# class Receipt(BaseModel):
#     class Meta:
#         verbose_name = _("Receipt")
#
#     unique_id = models.IntegerField(unique=True, primary_key=True, verbose_name=_("Unique id"))
#     # TODO: implement a random id generator function for default of this field
#     delivery_time = models.DurationField(null=True, default=timedelta(days=1), blank=True,
#                                          verbose_name=_("Will delivery at"))
#
#     @property
#     def product_list(self):
#         cart = self.cart
#         cart: Cart
#         return cart.items.values_list('product', flat=True)
#
#     @property
#     def total_price(self):
#         prices = [x.final_price for x in self.cart.items.all()]
#         return sum(prices)
#
#     #  Test it with aggregation function
#
#     @property
#     def order_discount(self):
#         return self.cart.off_code.profit(self.total_price)
#
#     @property
#     def final_price(self):
#         return self.total_price - self.order_discount
#
#     def __repr__(self):
#         return f"Receipt {self.unique_id}"

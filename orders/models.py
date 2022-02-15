from django.db import models
from datetime import timedelta
from core.models import BaseModel
from products.models import Product, _, OffCode


class CartItem(BaseModel):
    class Meta:
        verbose_name = _("Cart item")

    product = models.ForeignKey(Product, on_delete=models.RESTRICT, verbose_name=_("Product"))
    count = models.SmallIntegerField(verbose_name=_("Number of product"))  # TODO: check available number
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name=_("Basket"), related_name='items')


class Cart(BaseModel):
    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    off_code = models.ForeignKey(OffCode, default=None, null=True, on_delete=models.SET_NULL, verbose_name=_("OffCode"))
    status = models.CharField(max_length=20,
                              choices=[('unfinished', "Unfinished"), ('unpaid', 'Unpaid'), ('paid', 'Paid')],
                              verbose_name=_("Basket Status"))
    receipt = models.OneToOneField('Receipt', on_delete=models.SET_NULL, null=True, default=None,
                                   verbose_name=_("Receipt"))
    # TODO: create a receipt when status of cart is paid


class Receipt(BaseModel):
    class Meta:
        verbose_name = _("Receipt")

    unique_id = models.IntegerField(unique=True, primary_key=True, verbose_name=_("Unique id"))
    # TODO: implement a random id generator function for default of this field
    delivery_time = models.DurationField(null=True, default=timedelta(days=1), verbose_name=_("Will delivery at"))

    @property
    def product_list(self):
        cart = self.cart
        cart: Cart
        return cart.items.values_list('product', flat=True)

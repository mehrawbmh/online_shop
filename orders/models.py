from django.db import models
from core.models import BaseModel
from customers.models import Address, Customer
from products.models import Product, _, OffCode
from datetime import timedelta
from .validators import check_positive_not_zero


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
        default=1,
        validators=[check_positive_not_zero]
    )
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        verbose_name=_("Basket"),
        related_name='items'
    )
    total_price = models.IntegerField(
        null=True,
        blank=True,
        validators=[check_positive_not_zero]
    )

    @property
    def final_price(self):
        return self.calc_final_price()

    def calc_final_price(self):
        self.total_price = self.product.final_price * int(self.count)
        return self.total_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.calc_final_price()
        self.cart.save()
        return super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        self.cart.save()

    def __repr__(self):
        return f"for {self.cart} => {self.count} of {self.product}"


class Cart(BaseModel):
    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    #     unique_id = models.IntegerField(unique=True, primary_key=True, verbose_name=_("Unique id"))
    #     delivery_time = models.DurationField(null=True, default=timedelta(days=1), blank=True,verbose_name=_("Will delivery at"))
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
        on_delete=models.RESTRICT,
        null=True,
    )
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.DO_NOTHING
    )
    extra_info = models.TextField(
        null=True,
        blank=True,
        help_text="more information about your order and how it would be sent"
    )
    raw_price = models.IntegerField(
        blank=True,
        null=True
    )
    order_discount = models.IntegerField(
        blank=True,
        null=True
    )
    final_prize = models.IntegerField(
        blank=True,
        null=True
    )

    @property
    def product_list(self):
        return list(self.items.values_list('product__name', flat=True))

    def raw_price_calc(self):
        prices = [x.final_price for x in self.items.all()]
        self.raw_price = sum(prices)
        return self.raw_price

    def order_discount_calc(self):
        if self.off_code:
            self.order_discount = self.off_code.profit(self.raw_price)
            return self.order_discount
        return 0

    def final_prize_calc(self):
        final_prize = self.raw_price_calc() - self.order_discount_calc()
        self.final_prize = final_prize
        return self.final_prize

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.final_prize_calc()
        return super().save(force_insert, force_update, using, update_fields)

    def __repr__(self):
        try:
            return f"Cart {self.id}({self.status}) for {self.customer}"
        except AttributeError:
            return f"Temporary Cart for {self.customer}"

    def clean(self):
        # IS it necessary?
        self.final_prize_calc()
        return super().clean()

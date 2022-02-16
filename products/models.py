from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import datetime

from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Category")
        ordering = ("parent",)

    name = models.CharField(max_length=50, unique=True, verbose_name=_("Category Name"), db_index=True)
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, default=None,
                               verbose_name=_("Category parent"))


class Brand(BaseModel):
    class Meta:
        verbose_name = _("Brand")
        ordering = ("name",)

    name = models.CharField(max_length=50, unique=True, verbose_name=_("Brand name"), db_index=True)
    satisfaction_rate = models.PositiveIntegerField(verbose_name=_("Satisfaction rating"), null=True, blank=True)
    bio = models.TextField(null=True, blank=True, verbose_name=_("Brand description"))


class Discount(BaseModel):
    class Meta:
        verbose_name = _("Discount")

    type = models.CharField(max_length=10, choices=[("percent", 'Percent'), ("amount", 'Amount')],
                            verbose_name="Discount type")
    value = models.IntegerField(verbose_name=_("Discount value"))
    max_price = models.IntegerField(null=True, blank=True, verbose_name=_("Maximum Price"))  # TODO : add validator
    expire_date = models.DateField(null=True, blank=True, verbose_name=_("Expire time"))

    @property
    def _max_price(self):
        return self.max_price

    @_max_price.setter
    def _max_price(self, value):
        if self.type != 'percent':
            raise ValueError("Max price only defines for discounts with type of percent")
        else:
            self.max_price = value

    def profit(self, price):
        if self.type == 'percent':
            raw = int(self.value * price / 100)
            return min(self.max_price, raw) if self.max_price else raw
        elif self.type == 'amount':
            return self.value if price - self.value > 0 else price
        else:
            raise AttributeError("discount type is not defined!")

    def is_valid(self, code=None):
        if datetime.today().date() > self.expire_date:
            self.is_active = False
            raise ValidationError("The discount has expired!")
        self.is_active = True
        return True


class OffCode(Discount):
    class Meta:
        verbose_name = _("Off Code")

    unique_token = models.CharField(max_length=50, verbose_name=_("Unique token"), unique=True)
    # TODO: a function in utils that makes unique code
    title = models.CharField(max_length=127, default="Season OFF!", verbose_name=_("Title"))
    min_buy_price = models.IntegerField(default=25000, verbose_name=_("Minimum buy amount"))

    def is_valid(self, code=None):  ### super?
        if self.unique_token == code:
            if datetime.today().date() > self.expire_date:
                self.is_active = False
                raise ValidationError("The token has expired!")
            self.is_active = True
            return True
        return False

    def profit(self, price):
        return super().profit(price) if self.min_buy_price < price else 0


class Product(BaseModel):
    class Meta:
        verbose_name = _("Product")
        unique_together = ['name', 'brand']
        ordering = ("name", "-price")

    name = models.CharField(max_length=127, verbose_name=_("Product name"), db_index=True)
    price = models.IntegerField(verbose_name=_("Product price"))  # TODO: validator!
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=_("Category"))
    discount = models.ForeignKey(Discount, null=True, default=None, on_delete=models.SET_NULL,
                                 verbose_name=_("Discount"))
    available_count = models.IntegerField(verbose_name=_("Available number in store"), default=10)
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    # properties = models.JSONField(verbose_name=_("Product Properties"), null=True, default=None) (test writing)

    @property
    def final_price(self):
        return self.price - self.discount.profit(self.price) if self.discount else self.price

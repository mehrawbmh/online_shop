from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import datetime
from core.models import BaseModel, BaseDiscount
from django.utils.translation import gettext_lazy as _
from .validators import is_positive, check_percent_range


class Category(BaseModel):
    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Category")
        ordering = ('name',)

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Category Name"),
        db_index=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        default=None,
        blank=True,
        verbose_name=_("Category parent")
    )

    @property
    def cat_order(self):
        count = 0
        while self.parent:
            count += 1
            self = self.parent
        return count

    @property
    def full_set(self):
        cat_list = []
        for prod in Product.objects.all():
            if prod.has_cat(self):
                cat_list.append(prod)
        return cat_list

    @classmethod
    def get_max_order(cls):
        degree_list = [x.cat_order for x in cls.objects.all()]
        return max(degree_list)

    def __repr__(self):
        if self.parent:
            return f'Sub Category => {self.name}'
        return f'Base Category => {self.name}'


class Brand(BaseModel):
    class Meta:
        verbose_name = _("Brand")
        ordering = ("name",)

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Brand name"),
        db_index=True
    )
    satisfaction_rate = models.PositiveIntegerField(
        verbose_name=_("Satisfaction rating"),
        null=True,
        blank=True,
        validators=[check_percent_range]
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Brand description")
    )

    def __repr__(self):
        return f'Brand {self.name}'


class Discount(BaseDiscount):
    class Meta:
        verbose_name = _("Discount")

    @property
    def _max_price(self):
        return self.max_price

    @_max_price.setter
    def _max_price(self, value):
        if self.type != 'percent':
            raise ValueError("Max price only defines for discounts with type of percent")
        else:
            self.max_price = value

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        for prod in self.product_set.all():
            prod.discount = None
            prod.save()

    def __repr__(self):
        return f"{self.type} Discount => {self.value}"

    def __str__(self):
        if self.type == 'percent':
            text = f"{self.value} percent Discount"
        else:
            text = f"{self.value} Tooman Discount"
        if self.expire_date:
            text += f'- expires at {self.expire_date}'
        return text


class OffCode(BaseDiscount):
    class Meta:
        verbose_name = _("Off Code")

    unique_token = models.CharField(
        max_length=50,
        verbose_name=_("Unique token"),
        unique=True,
    )
    # TODO: a function in utils that makes unique code
    title = models.CharField(
        max_length=127,
        default="Season OFF!",
        verbose_name=_("Title")
    )
    min_buy_price = models.IntegerField(
        default=25000,
        verbose_name=_("Minimum buy amount")
    )

    def is_valid(self, code=None):  ### super?
        if self.unique_token == code:
            if self.expire_date:
                if datetime.today().date() > self.expire_date:
                    self.is_active = False
                    raise ValidationError("The token has expired!")
                self.is_active = True
            return True
        return False

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        for cart in self.cart_set.all():
            cart.off_code = None
            cart.save()

    def profit(self, price):
        return super().profit(price) if self.min_buy_price < price else 0

    def __repr__(self):
        if self.type == 'percent':
            string = f'{self.value}% OFF code'
            if self.max_price:
                string += f" - up to {self.max_price} Tooman"
        else:
            string = f'{self.value} Tooman OFF code'
        if self.expire_date:
            string += f' (expires at {self.expire_date})'
        return string


class Product(BaseModel):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        unique_together = ['name', 'brand']
        ordering = ("name", "-price")

    name = models.CharField(
        max_length=127,
        verbose_name=_("Product name"),
        db_index=True
    )
    price = models.IntegerField(
        verbose_name=_("Product price"),
        validators=[is_positive]
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        verbose_name=_("Category")
    )
    discount = models.ForeignKey(
        Discount,
        null=True,
        default=None,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Discount")
    )
    available_count = models.IntegerField(
        verbose_name=_("Available number in store"),
        default=10,
        validators=[is_positive],
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description")
    )
    properties = models.JSONField(
        verbose_name=_("Product Properties"),
        null=True,
        default=None,
        blank=True
    )
    image = models.ImageField(
        verbose_name=_("Product image"),
        blank=True,
        null=True,
    )

    @property
    def final_price(self):
        return self.price - self.discount.profit(self.price) if self.discount else self.price

    def has_cat(self, cat: Category):
        for i in range(self.category.cat_order):
            if self.category == cat:
                return True
            self.category = self.category.parent
        return False

    def __repr__(self):
        return f"{self.name} from brand {self.brand.name}"

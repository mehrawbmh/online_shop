from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import datetime
from core.managers import BaseManager, UsersManager
from django.utils.translation import gettext_lazy as _
from .validators import is_all_digit, is_11_characters, startswith_09


class BaseModel(models.Model):
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        db_column='deleted?',
        editable=False,
        verbose_name=_('Delete_status')
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        db_column='active?',
        verbose_name=_('Active_status'),
        help_text="Use it when you want to temporarily not show some model to end user"
    )
    create_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Create time')
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last update")
    )

    objects = BaseManager()

    class Meta:
        abstract = True
        get_latest_by = "create_timestamp"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(using=using)

    def restore(self):
        self.is_deleted = False
        self.save()
        # TODO: log when some object restored

    def deactivate(self):
        self.is_active = False
        self.save()
        # TODO: use it when you want to finish a basket(card) of customer after payment

    def activate(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return str(vars(self))


class User(AbstractUser):
    class Meta:
        verbose_name = _("User")
    objects = UsersManager()
    USERNAME_FIELD = 'phone'
    phone = models.CharField(
        max_length=16,
        unique=True,
        validators=[is_all_digit, startswith_09, is_11_characters]
    )

    def __repr__(self):
        return f'{self.username}'


class BaseDiscount(BaseModel):
    class Meta:
        abstract = True

    type = models.CharField(
        max_length=10,
        choices=[("percent", 'Percent'), ("amount", 'Amount')],
        verbose_name="Discount type"
    )
    value = models.IntegerField(
        verbose_name=_("Discount value")
    )
    max_price = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Maximum Price")
    )  # TODO : add validator
    expire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Expire time"),
    )

    def profit(self, price):
        if self.type == 'percent':
            raw = int(self.value * price / 100)
            return min(self.max_price, raw) if self.max_price else raw
        elif self.type == 'amount':
            return self.value if price - self.value > 0 else price
        else:
            raise AttributeError("discount type is not defined!")

    def is_valid(self, code=None):
        if self.expire_date:
            if datetime.today().date() > self.expire_date:
                self.is_active = False
                raise ValidationError("The discount has expired!")
            self.is_active = True
        return True

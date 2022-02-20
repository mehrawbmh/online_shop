from django.db import models
from core.models import User, BaseModel, _


class Customer(models.Model):
    class Meta:
        verbose_name = _("Customer")

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )


class Address(BaseModel):
    class Meta:
        verbose_name = _("Address")

    province = models.CharField(
        max_length=30
    )
    city = models.CharField(
        max_length=30
    )
    region = models.IntegerField(
        blank=True,
        null=True
    )
    main_street = models.CharField(
        max_length=40
    )
    minor_street = models.CharField(
        max_length=40
    )
    alley = models.CharField(
        max_length=40
    )
    number = models.IntegerField(
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.DO_NOTHING
    )

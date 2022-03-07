from django.db import models
from core.models import User, BaseModel, _


class Customer(models.Model):
    class Meta:
        verbose_name = _("Customer")
    birthday = models.DateField(
        blank=True,
        null=True
    )
    national_code = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        unique=True
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )

    @property
    def address_list(self):
        return Address.objects.filter(customer=self).all()

    def __repr__(self):
        return f"Customer {self.user.username}"

    def __str__(self):
        return str(self.user)


class Address(BaseModel):
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    province = models.CharField(
        max_length=30
    )
    city = models.CharField(
        max_length=30
    )
    region = models.PositiveSmallIntegerField(
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
    number = models.PositiveSmallIntegerField(
    )
    house_floor = models.PositiveSmallIntegerField(
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

    def __repr__(self):
        return f'Address {self.id} for {self.customer}'

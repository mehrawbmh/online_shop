from django.contrib.auth.models import UserManager
from django.db import models
from .utils import phone_normalize


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_deleted=True)

    def get_deleted(self):
        return super().get_queryset().exclude(is_deleted=False)

    def full_archive(self):
        return super().get_queryset()

    def get_active(self):
        return self.get_queryset().filter(is_active=True)


class UsersManager(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields['phone'] = phone_normalize(extra_fields['phone'])
        phone = extra_fields['phone']
        username = phone
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields['phone'] = phone_normalize(extra_fields['phone'])
        phone = extra_fields['phone']
        username = phone
        return super().create_superuser(username, email, password, **extra_fields)

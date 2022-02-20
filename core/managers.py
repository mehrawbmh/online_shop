from django.contrib.auth.models import UserManager
from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_deleted=True)

    def get_deleted(self):
        return super().get_queryset().exclude(is_deleted=False)

    def full_archive(self):
        return super().get_queryset()

    def get_active(self):  # TODO : just show active products on site not all!
        return self.get_queryset().filter(is_active=True)


class UsersManager(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_superuser(username, email, password, **extra_fields)




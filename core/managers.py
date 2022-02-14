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

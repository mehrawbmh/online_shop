from django.db import models

from core.managers import BaseManager
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True, db_column='deleted?', editable=False,
                                     verbose_name=_('Delete_status'))
    is_active = models.BooleanField(default=True, db_index=True, db_column='active?', verbose_name=_('Active_status'),
                                    help_text="Use it when you want to temporarily not show some model to end user")
    create_timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Create time'))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_("Last update"))

    objects = BaseManager()

    class Meta:
        abstract = True

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

    def activate(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return repr(self)



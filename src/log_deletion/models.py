# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete

registry = []
ONCOMMIT = getattr(settings, 'LOG_DELETION_ONCOMMIT', False)
if ONCOMMIT:
    from django.db.transaction import on_commit


class DeletionQuerySet(models.QuerySet):
    def filter_model(self, model):
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content_type=content_type)

    def create_for_model(self, model, **kwargs):
        content_type = ContentType.objects.get_for_model(model)
        kwargs['content_type'] = content_type
        kwargs['table_name'] = model._meta.db_table.lower()
        return self.create(**kwargs)


class AbstractDeletion(models.Model):
    when = models.DateTimeField(auto_now_add=True, db_index=True)
    content_type = models.ForeignKey(ContentType,
                                     blank=True, null=True,
                                     on_delete=models.SET_NULL)
    table_name = models.CharField(max_length=100, db_index=True)
    object_id = models.CharField(max_length=100)

    objects = DeletionQuerySet.as_manager()

    class Meta:
        abstract = True
        app_label = 'log_deletion'


class Deletion(AbstractDeletion):
    pass


def log_instance_deletion(sender, instance, using, **kwargs):
    pk = instance.pk

    def ond():
        Deletion.objects.create_for_model(instance, object_id=pk)

    if sender in registry:
        if ONCOMMIT:
            on_commit(lambda: ond())
        else:
            ond()


pre_delete.connect(log_instance_deletion)
# post_delete.connect(log_deletion)

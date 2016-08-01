# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete
from django.db.transaction import on_commit

registry = []


class DeletionQuerySet(models.QuerySet):
    def filter_model(self, model):
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content_type=content_type)

    def create_for_model(self, model, **kwargs):
        content_type = ContentType.objects.get_for_model(model)
        kwargs['content_type'] = content_type
        return self.create(**kwargs)


class AbstractDeletion(models.Model):
    when = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    table_name = models.CharField(max_length=100)
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
        on_commit(lambda: ond())


pre_delete.connect(log_instance_deletion)
# post_delete.connect(log_deletion)

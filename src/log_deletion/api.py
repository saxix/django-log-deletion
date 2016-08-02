# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer

from log_deletion.models import Deletion

logger = logging.getLogger(__name__)


class DeletionSerializer(ModelSerializer):
    class Meta:
        model = Deletion


class ListDeletion(ListAPIView):
    serializer_class = DeletionSerializer
    queryset = Deletion.objects.all()
    filter_fields = ('when', 'content_type', 'table_name')
    # filter_backends = (QueryStringFilterBackend, )

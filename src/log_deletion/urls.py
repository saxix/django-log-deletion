# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from log_deletion.api import ListDeletion

urlpatterns = (url('deletions/', ListDeletion.as_view(), name='deletions'),)

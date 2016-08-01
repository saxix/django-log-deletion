# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from log_deletion.models import Deletion

logger = logging.getLogger(__name__)


@admin.register(Deletion)
class DeletionAdmin(ModelAdmin):
    pass

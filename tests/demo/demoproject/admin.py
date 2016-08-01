# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.admin import ModelAdmin


logger = logging.getLogger(__name__)


class DemoModelAdmin(ModelAdmin):
    pass

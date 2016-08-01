# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import six
from django.apps import apps

from log_deletion.models import registry

logger = logging.getLogger(__name__)


def monitor_app_deletion(app_label):
    app = apps.get_app_config(app_label)
    models = app.get_models(include_auto_created=True, include_swapped=True)
    monitor_deletion(*models)


def monitor_all_deletion():
    models = apps.get_models(include_auto_created=True, include_swapped=True)
    monitor_deletion(*models)


def monitor_deletion(*models):
    for model in models:
        if model not in registry:
            registry.append(model)


class log_deletion(object):
    def __init__(self, *models):
        self.models = models

    def __enter__(self):
        monitor_deletion(*self.models)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for model in self.models:
            if model in registry:
                registry.remove(model)
        if exc_type:
            six.reraise(exc_type, exc_val, exc_tb)


class disable_log_deletion(object):
    sender = None

    def __init__(self, sender):
        self.sender = sender

    def __enter__(self):
        registry.remove(self.sender)

    def __exit__(self, exc_type, exc_val, exc_tb):
        registry.append(self.sender)
        if exc_type:
            six.reraise(exc_type, exc_val, exc_tb)

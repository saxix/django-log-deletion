# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType

from demoproject.models import DemoModel2, DemoModel
from log_deletion.models import registry
from log_deletion.utils import monitor_app_deletion, monitor_deletion, monitor_all_deletion

logger = logging.getLogger(__name__)


def test_monitor():
    monitor_deletion(DemoModel)
    assert registry == [DemoModel]

    monitor_deletion(DemoModel, DemoModel2)
    assert registry == [DemoModel, DemoModel2]


def test_monitor_app():
    monitor_app_deletion('demoproject')
    assert registry == [DemoModel, DemoModel2]


def test_monitor_all():
    monitor_all_deletion()
    assert DemoModel in registry
    assert Group in registry
    assert User in registry
    assert ContentType in registry

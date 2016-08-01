# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.db import models


class DemoModel(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=10)


class DemoModel2(models.Model):
    name = models.CharField(max_length=10)

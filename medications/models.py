#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
class Medications(models.Model):
    name = models.CharField(max_length = 300)



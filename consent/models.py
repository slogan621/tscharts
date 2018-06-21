# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from register.models import Register

class Consent(models.Model):
    register = models.ForeignKey(Register)
    general_consent = models.BooleanField(default = False)
    photo_consent = models.BooleanField(default = False)

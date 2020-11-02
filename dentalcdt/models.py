#!/usr/bin/python

#(C) Copyright Syd Logan 2020
#(C) Copyright Thousand Smiles Foundation 2020
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
class DentalCDT(models.Model):
    category = models.CharField(max_length = 64)  
    code = models.CharField(max_length = 12)  # 5 digits + expansion
    desc = models.CharField(max_length = 500) # some descriptions are lengthy  

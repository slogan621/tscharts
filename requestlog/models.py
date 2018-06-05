#(C) Copyright Syd Logan 2017-2018
#(C) Copyright Thousand Smiles Foundation 2017-2018
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

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class RequestLog(models.Model):
    method = models.CharField(max_length=16)      # request.method,
    user = models.CharField(max_length=64)        # request.user.username,
    path = models.CharField(max_length=256)       # request.get_full_path(),
    origin = models.CharField(max_length=128)     # request.META.get('HTTP_HOST', u'Unknown'),
    useragent = models.CharField(max_length=128)  # request.META.get('HTTP_USER_AGENT', u'Unknown'),
    auth = models.CharField(max_length=128)       # request.auth,
    auths = models.CharField(max_length=128)      # u'\n    '.join(unicode(x) for x in request.authenticators),
    body = models.CharField(max_length=1024)      # request.body,
    files = models.CharField(max_length=1024)     # u'\n    '.join(u'%s: %s' % (k,v) for k,v in sorted(request.FILES.items())),
    content = models.CharField(max_length=1024)   # request.content_type,
    timestamp = models.DateTimeField(auto_now_add=True)

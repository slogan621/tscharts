# coding: utf-8 

#(C) Copyright Syd Logan 2018
#(C) Copyright Thousand Smiles Foundation 2018
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

import logging
LOGGER = logging.getLogger(__name__)
import sys

def log_request(func_to_decorate):
    def wrapper(*args, **kwargs):
        try:
            request = args[1]
            data = request.body
            LOGGER.info(u'REQUEST_LOG: %(method)s request on “%(path)s” for %(user)s '
                    u'from %(origin)s (%(useragent)s):\n'
                    u'auth: %(auth)s, authenticators: [\n%(auths)s\n]\n'
                    u'content-type: %(content)s\n'
                    u'data: %(data)s\n'
                    u'files: {\n    %(files)s\n}' % {
                        'method': request.method,
                        'user': request.user.username,
                        'path': request.get_full_path(),
                        'origin': request.META.get('HTTP_HOST', u'Unknown'),
                        'useragent': request.META.get('HTTP_USER_AGENT',
                                                   u'Unknown'),
                        'auth': request.auth,
                        'auths': u'\n    '.join(
                            unicode(x) for x in request.authenticators),
                        'data': data,
                        'files': u'\n    '.join(u'%s: %s' % (k,v)
                            for k,v in sorted(request.FILES.items())),
                        'content': request.content_type,
                        }
                    )
        except:
            LOGGER.info(u'REQUEST_LOG: Exception trying to log request {}'.format(sys.exc_info()[0]))
        result = func_to_decorate(*args, **kwargs)
        return result
    return wrapper

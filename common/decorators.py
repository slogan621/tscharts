# coding: utf-8

#(C) Copyright Syd Logan 2018-2026
#(C) Copyright Thousand Smiles Foundation 2018-2026
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
import sys

LOGGER = logging.getLogger(__name__)

from requestlog.models import RequestLog


def _as_text(value, max_len=None):
    """Normalize request fields for CharField / log output (Python 3)."""
    if value is None:
        text = ""
    elif isinstance(value, bytes):
        text = value.decode("utf-8", errors="replace")
    else:
        text = str(value)
    if max_len is not None:
        text = text[:max_len]
    return text


def log_request(func_to_decorate):
    def wrapper(*args, **kwargs):
        try:
            request = args[1]
            method = request.method
            user = _as_text(getattr(request.user, "username", ""), 64)
            path = _as_text(request.get_full_path(), 256)
            origin = _as_text(request.META.get("HTTP_HOST", "Unknown"), 128)
            useragent = _as_text(
                request.META.get("HTTP_USER_AGENT", "Unknown"), 128
            )
            auth = _as_text(request.auth, 128)
            authenticators = getattr(request, "authenticators", None) or ()
            auths = _as_text(
                "\n    ".join(str(x) for x in authenticators), 128
            )
            body = _as_text(request.body, 1024)
            files = _as_text(
                "\n    ".join(
                    "%s: %s" % (k, v) for k, v in sorted(request.FILES.items())
                ),
                1024,
            )
            content = _as_text(request.content_type, 1024)

            r = RequestLog(
                method=method,
                user=user,
                path=path,
                origin=origin,
                useragent=useragent,
                auth=auth,
                auths=auths,
                body=body,
                files=files,
                content=content,
            )
            r.save()
        except Exception:
            LOGGER.info(
                "REQUEST_LOG: Exception trying to log request %s",
                sys.exc_info()[0],
            )
            try:
                # logging to DB failed, try to log to file instead
                request = args[1]
                authenticators = getattr(request, "authenticators", None) or ()
                LOGGER.info(
                    "REQUEST_LOG: %(method)s request on “%(path)s” for %(user)s "
                    "from %(origin)s (%(useragent)s):\n"
                    "auth: %(auth)s, authenticators: [\n%(auths)s\n]\n"
                    "content-type: %(content)s\n"
                    "data: %(data)s\n"
                    "files: {\n    %(files)s\n}"
                    % {
                        "method": request.method,
                        "user": getattr(request.user, "username", ""),
                        "path": request.get_full_path(),
                        "origin": request.META.get("HTTP_HOST", "Unknown"),
                        "useragent": request.META.get(
                            "HTTP_USER_AGENT", "Unknown"
                        ),
                        "auth": request.auth,
                        "auths": "\n    ".join(
                            str(x) for x in authenticators
                        ),
                        "data": _as_text(request.body),
                        "files": "\n    ".join(
                            "%s: %s" % (k, v)
                            for k, v in sorted(request.FILES.items())
                        ),
                        "content": request.content_type,
                    }
                )
            except Exception:
                LOGGER.info(
                    "REQUEST_LOG: Exception trying to log request to file %s",
                    sys.exc_info()[0],
                )
        result = func_to_decorate(*args, **kwargs)
        return result

    return wrapper

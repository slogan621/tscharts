#(C) Copyright Syd Logan 2016-2018
#(C) Copyright Thousand Smiles Foundation 2016
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

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
import json
from common.decorators import *

class LoginView(APIView):

    authentication_classes = ()
    permission_classes = ()

    @log_request
    def post(self, request, format=None):
        badRequest = False
        forbidden = False

        data = json.loads(request.body)

        if not "username" in data:
            badRequest = True
        if not "password" in data:
            badRequest = True
        if not badRequest:
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                else:
                    forbidden = True
            else:
                forbidden = True
        if not forbidden and not badRequest:
            token = Token.objects.get_or_create(user=user)[0]
            return JsonResponse({"token": "{}".format(token.key),
                                 "id": "{}".format(user.id)})
        elif forbidden:
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()

class LogoutView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @log_request
    def post(self, request, format=None):
        logout(request)
        return HttpResponse()

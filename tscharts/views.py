#(C) Copyright Syd Logan 2016-2021
#(C) Copyright Thousand Smiles Foundation 2016-2021
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

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import json
from common.decorators import *
from pin.models import PIN
import traceback

import logging

LOG = logging.getLogger("tscharts")

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
        if not "password" in data and not "pin" in data:
            badRequest = True
        if not badRequest:
            username = data['username']
            if "password" in data:
                password = data['password']
                user = authenticate(username=username, password=password)
            else:
                LOG.error("traceback 0 {}".format(traceback.print_stack()))
                user = User.objects.get(username=username)
                if user:
                    LOG.error("traceback 1 {}".format(traceback.print_stack()))
                    pin = PIN.objects.get(user=user.id)
                    if pin:
                        LOG.error("traceback 2 {}".format(traceback.print_stack()))
                        if not pin.user == user:
                            LOG.error("traceback 3 {}".format(traceback.print_stack()))
                            user = None
                        elif not pin.pin == data["pin"]:
                            LOG.error("traceback 4 {}".format(traceback.print_stack()))
                            user = None
                    else:
                        LOG.error("traceback 5 {}".format(traceback.print_stack()))
                        user = None
            if user:
                LOG.error("traceback 6 {}".format(traceback.print_stack()))
                if user.is_active:
                    # XXX hack
                    try:
                        if not user.backend:
                            user.backend = 'django.contrib.auth.backends.ModelBackend'
                    except:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        
                    login(request, user)
                else:
                    LOG.error("traceback 7 {}".format(traceback.print_stack()))
                    forbidden = True
            else:
                LOG.error("traceback 8 {}".format(traceback.print_stack()))
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

class CreateUserView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @log_request
    def post(self, request, format=None):
        badRequest = False
        duplicateUser = False
        implError = False

        data = json.loads(request.body)

        if not "first" in data:
            badRequest = True
        if not "last" in data:
            badRequest = True
        if not "password" in data:
            badRequest = True
        if not "email" in data:
            badRequest = True
        if not "pin" in data:
            badRequest = True

        if not badRequest:
            first = data['first']
            last = data['last']
            password = data['password']
            email = data['email']

            try:
                user = User.objects.get(username=email)
            except:
                user = None

            if user:
                badRequest = True
                duplicateUser = True
        
        if not badRequest:
            try:
                user = User.objects.create_user(email, email, password)
                user.is_active = True
                user.first_name = first
                user.last_name = last
                user.save()
            except:
                user = None

            if user:
                kwargs = {}

                kwargs["pin"] = data['pin']
                kwargs["user"] = user

                try:
                    pin = PIN(**kwargs)
                    if pin:
                        pin.save()
                except:
                    pin = None

                if not pin:
                    implMsg = "Unable to create PIN"
                    implError = True
            else:
                implMsg = "Unable to create user"
                implError = True

        if badRequest:
            if duplicateUser:
                r = HttpResponse(status=status.HTTP_409_CONFLICT, reason="User (%d) already exists".format(user.id))
                return r
            else:
                return HttpResponseBadRequest()
        elif implError:
            return HttpResponseServerError(implMsg)
        else:
            return Response({'id': user.id})

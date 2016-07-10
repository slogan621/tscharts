from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
import json

class LoginView(APIView):

    authentication_classes = ()
    permission_classes = ()

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
            return JsonResponse({"token": "{}".format(token.key) })
        elif forbidden:
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()

class LogoutView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        logout(request)
        return HttpResponse()

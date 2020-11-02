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

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from dentalcdt.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json
import sys

import logging
import traceback

LOG = logging.getLogger("tscharts")


class DentalCDTView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["category"] = entry.category
        m["code"] = entry.code
        m["desc"] = entry.desc
        return m

    def get(self, request, dentalcdt_id=None, format=None):   
        badRequest = False
        notFound = False
        dentalcdt = None
        if dentalcdt_id:
            try:
                dentalcdt = DentalCDT.objects.get(id = dentalcdt_id)
                ret = self.serialize(dentalcdt)
            except:
                dentalcdt = None
                notFound = True
        else: 
            kwargs = {}
            try:
                code = request.GET.get('code','')
                if not code == None and not code == '': 
                    kwargs['code'] = code
            except:
                pass
                
            try:
                category = request.GET.get('category','')
                if not category == None and not category == '': 
                    kwargs['category'] = category
            except:
                pass
                
            try:
                desc = request.GET.get('desc','')
                if not desc == None and not desc == '': 
                    kwargs['desc'] = desc
            except:
                pass
                
            if not badRequest:
                try:
                    dentalcdt = DentalCDT.objects.filter(**kwargs)
                except:
                    dentalcdt = None

                if not dentalcdt or len(dentalcdt) == 0:
                    notFound = True
                else:
                    ret = []
                    for x in dentalcdt:
                        ret.append(self.serialize(x))

        if badRequest:
            return HttpResponseBadRequest()
        elif notFound:
            return HttpResponseNotFound()
        else:
            return Response(ret)
    
    def post(self, request, format = None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        
        try:
            category = data['category']
            if len(category) == 0:
                badRequest = True
        except:
            badRequest = True

        try:
            code = data['code']
            if len(code) == 0:
                badRequest = True
        except:
            badRequest = True

        try:
            desc = data['desc']
            if len(desc) == 0:
                badRequest = True
        except:
            badRequest = True

        if not badRequest:
            try:
                if DentalCDT.objects.all().filter(code = data['code']).exists():
                    badRequest = True
            except:
                implMsg = "DentalCDT.objects.all().filter {} {}".format(sys.exc_info()[0], data)
                implError = True

        if not badRequest and not implError:
            try:
                dentalcdt = DentalCDT(**data)
                if dentalcdt:
                    dentalcdt.save()
                else:
                    implMsg = "Unable to create dentalcdt"
                    implError = True
            except:
                implMsg = "DentalCDT create {} {}".format(sys.exc_info()[0], data)
                implError = True

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id':dentalcdt.id})

    def delete(self, request, dentalcdt_id = None, format = None):
        dentalcdt = None
        try:
            dentalcdt = DentalCDT.objects.get(id = dentalcdt_id)
        except:
            dentalcdt = None
        if not dentalcdt:
            raise NotFound
        else:
            dentalcdt.delete()
        return Response({})

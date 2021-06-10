#(C) Copyright Syd Logan 2021
#(C) Copyright Thousand Smiles Foundation 2021
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
from covidvac.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json
import sys

import logging
import traceback

LOG = logging.getLogger("tscharts")


class COVIDVacView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super(COVIDVacView, self).__init__()
        self._validFields = ["name"]

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["name"] = entry.name
        return m

    def get(self, request, covidvac_id=None, format=None):   
        badRequest = False
        notFound = False
        covidvac = None
        if covidvac_id:
            try:
                covidvac = COVIDVac.objects.get(id = covidvac_id)
                ret = self.serialize(covidvac)
            except:
                covidvac = None
                notFound = True
        else: 
            kwargs = {}
            try:
                name = request.GET.get('name','')
                if not name == None and not name == '': 
                    kwargs['name'] = name
            except:
                pass
                
            if not badRequest:
                try:
                    covidvac = COVIDVac.objects.filter(**kwargs)
                except:
                    covidvac = None

                if not covidvac or len(covidvac) == 0:
                    notFound = True
                else:
                    ret = []
                    for x in covidvac:
                        ret.append(self.serialize(x))

        if badRequest:
            return HttpResponseBadRequest()
        elif notFound:
            return HttpResponseNotFound()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        try:
            for key, val in data.iteritems():
                if not (key in self._validFields):
                    LOG.error("validatePostArgs invalid key {}".format(key))
                    return False, kwargs
        except:
            LOG.error("validatePostArgs name exception")
            valid = False

        if not "name" in data:
            LOG.error("validatePostArgs no name field")
            valid = False

        LOG.error("validatePostArgs return {}".format(valid))
        return valid, kwargs

    
    def post(self, request, format = None):
        badRequest = False
        implError = False

        data = json.loads(request.body)

        valid, kwargs = self.validatePostArgs(data)

        if valid == False:
            badRequest = True
        
        try:
            name = data['name']
            if len(name) == 0:
                badRequest = True
        except:
            badRequest = True

        if not badRequest:
            try:
                if COVIDVac.objects.all().filter(name = data['name']).exists():
                    badRequest = True
            except:
                implMsg = "COVIDVac.objects.all().filter {} {}".format(sys.exc_info()[0], data)
                implError = True

        if not badRequest and not implError:
            try:
                covidvac = COVIDVac(**kwargs)
                if covidvac:
                    covidvac.save()
                else:
                    implMsg = "Unable to create covidvac"
                    implError = True
            except:
                implMsg = "COVIDVac create {} {}".format(sys.exc_info()[0], data)
                implError = True

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id':covidvac.id})

    def delete(self, request, covidvac_id = None, format = None):
        covidvac = None
        try:
            covidvac = COVIDVac.objects.get(id = covidvac_id)
        except:
            covidvac = None
        if not covidvac:
            raise NotFound
        else:
            covidvac.delete()
        return Response({})

# -*- coding: utf-8 -*-

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

from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from category.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import json
import sys

class CategoryView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["name"] = entry.name
        return m

    @log_request
    def get(self, request, category_id=None, format=None):   
        badRequest = False
        notFound = False
        category = None
        if category_id:
            try:
                category = Category.objects.get(id = category_id)
                ret = self.serialize(category)
            except:
                category = None
                notFound = True
        else: 
            try:
                cat = request.GET.get('name','')
            except:
                badRequest = True

            if not cat == '' and not badRequest:
                try:
                    category = Category.objects.get(name = cat)
                    ret = self.serialize(category)
                except:
                    category = None
                    notFound = True
            else:
                ret = []
                for x in Category.objects.all():
                    ret.append(self.serialize(x))

        if badRequest:
            return HttpResponseBadRequest()
        elif notFound:
            return HttpResponseNotFound()
        else:
            return Response(ret)
    
    @log_request
    def post(self, request, format = None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        
        try:
            name = data['name']
            if len(name) == 0:
                badRequest = True
        except:
            badRequest = True

        if not badRequest:
            try:
                if Category.objects.all().filter(name = data['name']).exists():
                    badRequest = True
            except:
                implMsg = "Category.objects.all().filter {} {}".format(sys.exc_info()[0], data)
                implError = True

        if not badRequest and not implError:
            try:
                category = Category(**data)
                if category:
                    category.save()
                else:
                    implMsg = "Unable to create category"
                    implError = True
            except:
                implMsg = "Category create {} {}".format(sys.exc_info()[0], data)
                implError = True

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id':category.id})

    @log_request
    def delete(self, request, category_id = None, format = None):
        category = None
        try:
            category = Category.objects.get(id = category_id)
        except:
            category = None
        if not category:
            raise NotFound
        else:
            category.delete()
        return Response({})

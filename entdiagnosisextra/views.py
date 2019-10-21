#(C) Copyright Syd Logan 2019
#(C) Copyright Thousand Smiles Foundation 2019
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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from entdiagnosis.models import *
from entdiagnosisextra.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

class ENTDiagnosisExtraView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["entdiagnosis"] = entry.entdiagnosis_id
        m["name"] = entry.name
        m["value"] = entry.value
        m["time"] = entry.time

        return m

    @log_request
    def get(self, request, ent_diagnosis_extra_id=None, format=None):
        ent_diagnosis_extra = None
        badRequest = False
        aENTDiagnosis = None
        kwargs = {}

        if ent_diagnosis_extra_id:
            try:
                ent_diagnosis_extra = ENTDiagnosisExtra.objects.get(id = ent_diagnosis_extra_id)
            except:
                ent_diagnosis_extra = None
        else:
            # look for required arguments
            try:
                entdiagnosisid = request.GET.get('entdiagnosis', '')
                if entdiagnosisid != '':
                    try:
                        aENTDiagnosis = ENTDiagnosis.objects.get(id=entdiagnosisid)
                        if not aENTDiagnosis:
                            badRequest = True
                        else:
                            kwargs["entdiagnosis"] = aENTDiagnosis
                    except:
                        badRequest = True
            except:
                badRequest = True

            hasName = False
            name = None
            try:
                name = request.GET.get('name', '')
                if name != '':
                    hasName = True
            except:
                pass # no name subsearch

            if not badRequest:
                try:
                    ent_diagnosis_extra = ENTDiagnosisExtra.objects.filter(**kwargs)
                    if hasName == True:
                        # isn't django wonderful, just filter on the result :-)
                        ent_diagnosis_extra = ent_diagnosis_extra.filter(Q(name__icontains=name))
                except:
                    ent_diagnosis_extra = None

        if not ent_diagnosis_extra and not badRequest:
            raise NotFound
        elif not badRequest:
            if ent_diagnosis_extra_id:
                ret = self.serialize(ent_diagnosis_extra)
            else:
                ret = []
                for x in ent_diagnosis_extra:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if not "name" in data or not "entdiagnosis" in data or not "value" in data:
            valid = False

        if "name" in data and len(data["name"]) == 0:
            valid = False

        return valid, kwargs

    def validatePutArgs(self, data, ent_diagnosis_extra):
        valid = True

        if not "name" in data and not "value" in data:
            valid = False

        if valid == True:
            if "name" in data:
                if len(data["name"]) > 0:
                    ent_diagnosis_extra.name = data["name"]
                else: 
                    valid = False

        if valid == True:
            if "value" in data:
                ent_diagnosis_extra.value = data["value"]

        return valid, ent_diagnosis_extra

    @log_request
    def post(self, request, format=None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        try:
            entdiagnosisid = int(data["entdiagnosis"])
        except:
            badRequest = True

        # validate the post data, and get a kwargs dict for
        # creating the object 

        valid, kwargs = self.validatePostArgs(data)

        if not valid:
            badRequest = True

        if not badRequest:

            # get the instances

            try:
                aENTDiagnosis = ENTDiagnosis.objects.get(id=entdiagnosisid)
            except:
                aENTDiagnosis = None
 
            if not aENTDiagnosis:
                raise NotFound

        if not badRequest:
            try:
                kwargs["entdiagnosis"] = aENTDiagnosis
                ent_diagnosis_extra = ENTDiagnosisExtra(**kwargs)
                if ent_diagnosis_extra:
                    ent_diagnosis_extra.save()
                else:
                    implError = True
            except Exception as e:
                implError = True
                implMsg = sys.exc_info()[0] 

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': ent_diagnosis_extra.id})

    @log_request
    def put(self, request, ent_diagnosis_extra_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_diagnosis_extra_id:
            badRequest = True

        if not badRequest:
            ent_diagnosis_extra = None

            try:
                ent_diagnosis_extra = ENTDiagnosisExtra.objects.get(id=ent_diagnosis_extra_id)
            except:
                pass

            if not ent_diagnosis_extra:
                notFound = True 
            else:
                try:
                    valid = True
                    data = json.loads(request.body)
                    valid, ent_diagnosis_extra = self.validatePutArgs(data, ent_diagnosis_extra)
                    if valid == True:
                        ent_diagnosis_extra.save()
                    else:
                        badRequest = True
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({})
       
    @log_request 
    def delete(self, request, ent_diagnosis_extra_id=None, format=None):
        ent_diagnosis_extra = None

        # see if the ent diagnosis extra object exists

        if not ent_diagnosis_extra_id:
            return HttpResponseBadRequest()
        try:
            ent_diagnosis_extra = ENTDiagnosisExtra.objects.get(id=ent_diagnosis_extra_id)
        except:
            ent_diagnosis_extra = None

        if not ent_diagnosis_extra:
            raise NotFound
        else:
            ent_diagnosis_extra.delete()

        return Response({})

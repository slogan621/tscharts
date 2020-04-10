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

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from audiogram.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import numbers

from common.decorators import *

import json
import sys

class AudiogramView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, x):
        ret = {}

        ret["id"] = x.id
        ret["clinic"] = x.clinic.id  
        ret["patient"] = x.patient.id  
        ret["image"] = x.image.id  
        ret["comment"] = x.comment  
        return ret

    @log_request
    def get(self, request, audiogram_id=None, format=None):
        notFound = False
        audiogram = None
        if audiogram_id:
            try:
                audiogram = Audiogram.objects.get(id = audiogram_id)
            except:
                audiogram = None
        else:
            kwargs = {}
            try:
                clinicid = request.GET.get('clinic', '')
                if clinicid != '':
                    clinicid = int(clinicid)
                    try:
                        aClinic = Clinic.objects.get(id=clinicid)
                        kwargs["clinic"] = aClinic
                    except:
                        notFound = True
            except:
                pass

            try:
                imageid = request.GET.get('image', '')
                if imageid != '':
                    imageid = int(imageid)
                    try:
                        aImage = Image.objects.get(id=imageid)
                        kwargs["image"] = aImage
                    except:
                        notFound = True
            except:
                pass

            try:
                patientid = request.GET.get('patient', '')
                if patientid != '':
                    patientid = int(patientid)
                    try:
                        aPatient = Patient.objects.get(id=patientid)
                        kwargs["patient"] = aPatient
                    except:
                        notFound = True
            except:
                pass

            try:
                audiogram = Audiogram.objects.filter(**kwargs)
            except:
                audiogram = None

        if notFound or not audiogram:
            raise NotFound
        elif audiogram_id: 
            ret = self.serialize(audiogram)
        else:
            ret = []
            for x in audiogram:
                m = self.serialize(x)
                ret.append(m)
        return Response(ret)

    @log_request
    def put(self, request, id=None, format=None):
        badRequest = False
        implError = False
        notFound = False
        comment = None

        data = json.loads(request.body)
        try:
            comment = data["comment"]
            if not isinstance(comment, basestring):
                comment = None
        except:
            pass

        if comment == None:
            badRequest = True

        if not badRequest:
            audiogram = None

            # see if the audiogram already exists

            try:
                audiogram = Audiogram.objects.get(id=id)
            except:
                pass

            if not audiogram:
                notFound = True 
            else:
                try:
                    if comment != None:
                        audiogram.comment=comment
                    audiogram.save()
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
    def post(self, request, format=None):
        badRequest = False
        notFound = False
        implError = False
        aClinic = None
        aPatient = None
        aImage = None

        data = json.loads(request.body)
        try:
            clinic = data["clinic"]
        except:
            badRequest = True
        try:
            patient = data["patient"]
        except:
            badRequest = True
        try:
            image = data["image"]
        except:
            badRequest = True
        try:
            comment = data["comment"]
        except:
            badRequest = True

        if not badRequest:
            try:
                aClinic = Clinic.objects.get(id=clinic)
            except:
                aClinic = None

            try:
                aImage = Image.objects.get(id=image)
            except:
                aImage = None

            try:
                aPatient = Patient.objects.get(id=patient)
            except:
                aPatient = None

            if not aClinic or not aImage or not aPatient:
                notFound = True

        if not badRequest and not notFound:

            audiogram = None

            # see if the audiogram already exists

            try:
                audiogram = Audiogram.objects.filter(clinic=aClinic,
                                                 patient=aPatient,
                                                 image=aImage)
                if not audiogram or len(audiogram) == 0:
                    audiogram = None
                else:
                    audiogram = audiogram[0]
                    if audiogram:
                        audiogram.comment = comment
                        audiogram.save()
            except:
                implMsg = "Audiogram.objects.filter {} {}".format(sys.exc_info()[0], data)
                implError = True

            if not audiogram:
                try:
                    audiogram = Audiogram(clinic=aClinic,
                                      patient=aPatient,
                                      image=aImage,
                                      comment=comment)
                    if audiogram:
                        audiogram.save()
                    else:
                        implMsg = "Unable to create audiogram"
                        implError = True
                except:
                    implMsg = "Audiogram create {} {}".format(sys.exc_info()[0], data)
                    implError = True
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': audiogram.id})
       
    @log_request 
    def delete(self, request, audiogram_id=None, format=None):
        audiogram = None

        # see if the audiogram exists

        try:
            audiogram = Audiogram.objects.get(id=audiogram_id)
        except:
            audiogram = None

        if not audiogram:
            raise NotFound
        else:
            audiogram.delete()

        return Response({})

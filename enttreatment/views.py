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
from clinic.models import *
from patient.models import *
from enttreatment.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

class ENTTreatmentView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def ENTTreatmentToString(self, val):
        ret = None 
        for x in ENTTreatment.ENT_TREATMENT_CHOICES:
            if x[0] == val:
                ret = x[1]
                break
        return ret

    def stringToENTTreatment(self, val):
        ret = None
        for x in ENTTreatment.ENT_TREATMENT_CHOICES:
            if x[1] == val:
                ret = x[0]
                break
        return ret

    def sideToString(self, val):
        ret = None 
        for x in ENTTreatment.EAR_SIDE_CHOICES:
            if x[0] == val:
                ret = x[1]
                break
        return ret    

    def stringToSide(self, val):
        ret = None 
        for x in ENTTreatment.EAR_SIDE_CHOICES:
            if x[1] == val:
                ret = x[0]
                break
        return ret    

    def stringToBoolean(self, val):
        ret = None 
        if val == "true" or val == "True":
            ret = True
        elif val == "false" or val == "False":
            ret = False
        return ret    

    def booleanToString(self, val):
        ret = None 
        if val == True:
            ret = "true"
        elif val == False:
            ret = "false"
        return ret    

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["username"] = entry.username
        m["time"] = entry.time
        m["treatment"] = self.ENTTreatmentToString(entry.treatment)
        m["future"] = self.booleanToString(entry.future)
        m["side"] = self.sideToString(entry.side)
        m["comment"] = entry.comment 

        return m

    @log_request
    def get(self, request, ent_treatment_id=None, format=None):
        ent_treatment = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if ent_treatment_id:
            try:
                ent_treatment = ENTTreatment.objects.get(id = ent_treatment_id)
            except:
                ent_treatment = None
        else:
            # look for optional arguments
            try:
                patientid = request.GET.get('patient', '')
                if patientid != '':
                    try:
                        aPatient = Patient.objects.get(id=patientid)
                        if not aPatient:
                            badRequest = True
                        else:
                            kwargs["patient"] = aPatient
                    except:
                        badRequest = True
            except:
                pass # no patient ID

            try:
                clinicid = request.GET.get('clinic', '')
                if clinicid != '':
                    try:
                        aClinic = Clinic.objects.get(id=clinicid)
                        if not aClinic:
                            badRequest = True
                        else:
                            kwargs["clinic"] = aClinic
                    except:
                        badRequest = True
            except:
                pass # no clinic ID

            try:
                val = request.GET.get('treatment', '')
                if val != '':
                    val = self.stringToENTTreatment(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs["treatment"] = val
                        if val == ENT_TREATMENT_OTHER:
                            # comment is required if treatment is "other"
                            try:
                                val = request.GET.get('comment', '')
                                kwargs["comment"] = val
                            except:
                                badRequest = True
            except:
                pass

            try:
                val = request.GET.get('future', '')
                if val != '':
                    val = self.stringToBoolean(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs["future"] = val
            except:
                pass

            try:
                val = request.GET.get('side', '')
                if val != '':
                    val = self.stringToSide(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs["side"] = val
            except:
                pass

            if not badRequest:
                try:
                    ent_treatment = ENTTreatment.objects.filter(**kwargs)
                except:
                    ent_treatment = None

        if not ent_treatment and not badRequest:
            raise NotFound
        elif not badRequest:
            if ent_treatment_id:
                ret = self.serialize(ent_treatment)
            else:
                ret = []
                for x in ent_treatment:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if not "username" in data:
            valid = False
        elif len(data["username"]) == 0:
            valid = False
        else:
            kwargs["username"] = data["username"]

        try:
            val = self.stringToENTTreatment(data["treatment"])
            if val == None:
                valid = False
            else:
                kwargs["treatment"] = val
        except:
            valid = False

        try:
            val = self.stringToBoolean(data["future"])
            if val == None:
                valid = False
            else:
                kwargs["future"] = val
        except:
            valid = False

        try:
            val = self.stringToSide(data["side"])
            if val == None:
                valid = False
            else:
                kwargs["side"] = val
        except:
            valid = False

        return valid, kwargs

    def validatePutArgs(self, data, ent_treatment):
        valid = True

        try:
            if "treatment" in data:
                val = self.stringToENTTreatment(data["treatment"])
                if val == None:
                    valid = False
                else:
                    ent_treatment.treatment = val
                    if val == ENTTreatment.ENT_TREATMENT_OTHER:
                        if not "comment" in data:
                            valid = False
                        elif len(data["comment"]) == 0:
                            valid = False
                        else:
                            ent_treatment.comment = data["comment"]
        except:
            pass

        try:
            if "future" in data:
                val = self.stringToBoolean(data["future"])
                if val == None:
                    valid = False
                else:
                    ent_treatment.future = val
        except:
            pass

        try:
            if "side" in data:
                val = self.stringToSide(data["side"])
                if val == None:
                    valid = False
                else:
                    ent_treatment.side = val
        except:
            pass

        try:
            if "clinic" in data:
                aClinic = Clinic.objects.get(id=int(data["clinic"]))
                ent_treatment.clinic = data["clinic"]
        except:
            pass

        try:
            if "patient" in data:
                aPatient = Patient.objects.get(id=int(data["patient"]))
                ent_treatment.patient = aPatient
        except:
            pass

        try:
            if "comment" in data:
                ent_treatment.comment = data["comment"]
        except:
            pass

        val = "treatment" in data or "comment" in data or "future" in data or "side" in data or "comment" in data or "username" in data
        if val == False:
            valid = False

        return valid, ent_treatment

    @log_request
    def post(self, request, format=None):
        badRequest = False
        implError = False
        implMsg = ""

        data = json.loads(request.body)
        try:
            patientid = int(data["patient"])
        except:
            badRequest = True

        try:
            clinicid = int(data["clinic"])
        except:
            badRequest = True


        # validate the post data, and get a kwargs dict for
        # creating the object 

        valid, kwargs = self.validatePostArgs(data)

        if not valid:
            badRequest = True

        if not badRequest and not implError:

            # get the instances

            try:
                aPatient = Patient.objects.get(id=patientid)
            except:
                aPatient = None
 
            try:
                aClinic = Clinic.objects.get(id=clinicid)
            except:
                aClinic = None

            if not aPatient or not aClinic:
                raise NotFound

        if not badRequest and not implError:
            try:
                kwargs["patient"] = aPatient
                kwargs["clinic"] = aClinic
                ent_treatment = ENTTreatment(**kwargs)
                if ent_treatment:
                    ent_treatment.save()
                else:
                    badRequest = True
            except Exception as e:
                badRequest = True
                implMsg = sys.exc_info()[0] 

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': ent_treatment.id})

    @log_request
    def put(self, request, ent_treatment_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_treatment_id:
            badRequest = True

        if not badRequest:
            ent_treatment = None

            try:
                ent_treatment = ENTTreatment.objects.get(id=ent_treatment_id)
            except:
                pass

            if not ent_treatment:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, ent_treatment = self.validatePutArgs(data, ent_treatment)
                    if valid: 
                        ent_treatment.save()
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
    def delete(self, request, ent_treatment_id=None, format=None):
        ent_treatment = None

        # see if the object exists

        if not ent_treatment_id:
            return HttpResponseBadRequest()
        try:
            ent_treatment = ENTTreatment.objects.get(id=ent_treatment_id)
        except:
            ent_treatment = None

        if not ent_treatment:
            raise NotFound
        else:
            ent_treatment.delete()

        return Response({})

#(C) Copyright Syd Logan 2017
#(C) Copyright Thousand Smiles Foundation 2017
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
from medicalhistory.models import *
from clinic.models import *
from patient.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import sys
import numbers
import json

class MedicalHistoryView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["time"] = entry.time
        if entry.health == 'g':
            m["health"] = "Good"
        else:
            m["health"] = "Poor"
    
        m["pain"] = entry.pain
        m["recentcold"] = entry.recentcold  
        m["hivaids"] = entry.hivaids 
        m["anemia"] = entry.anemia  
        m["athsma"] = entry.athsma 
        m["cancer"] = entry.cancer  
        m["congenitalheartdefect"] = entry.congenitalheartdefect 
        m["diabetes"] = entry.diabetes 
        m["epilepsy"] = entry.epilepsy  
        m["hemophilia"] = entry.hemophilia  
        m["hepititis"] = entry.hepititis  
        m["tuberculosis"] = entry.tuberculosis  
        m["troublespeaking"] = entry.troublespeaking  
        m["troublehearing"] = entry.troublehearing  
        m["troubleeating"] = entry.troubleeating  
        m["pregnancy_duration"] = entry.pregnancy_duration  
        m["pregnancy_smoke"] = entry.pregnancy_smoke  
        m["birth_complications"] = entry.birth_complications  
        m["pregnancy_complications"] = entry.pregnancy_complications 
        m["mother_alcohol"] = entry.mother_alcohol  
        m["relative_cleft"] = entry.relative_cleft  
        m["parents_cleft"] = entry.parents_cleft  
        m["siblings_cleft"] = entry.siblings_cleft  
        m["meds"] = entry.meds  
        m["allergymeds"] = entry.allergymeds  

        return m

    def get(self, request, medical_history_id=None, format=None):
        medical_history = None
        badRequest = False
        aPatient = None
        aClinic = None
        aStation = None
        aClinicStation = None
        kwargs = {}

        if medical_history_id:
            try:
                medical_history = MedicalHistory.objects.get(id = medical_history_id)
            except:
                medical_history = None
        else:
            # look for optional arguments
            data = json.loads(request.body)
            try:
                patientid = int(data["patient"])
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
                clinicid = int(data["clinic"])
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

            if not badRequest and len(kwargs):
                # look for invalid arg combinations

                # there are 2 legal combinations of args

                case1 = False
                case2 = False
                case3 = False

                if aPatient and aClinic:
                    case1 = True
                elif aPatient and not aClinic:
                    case2 = True
                elif aClinic and not aPatient:
                    case3 = True
                else:
                    badRequest = True

            if not badRequest:
                kwargs = {}
                if case1:
                    kwargs["patient"] = aPatient
                    kwargs["clinic"] = aClinic
                elif case2:
                    kwargs["patient"] = aPatient
                elif case3:
                    kwargs["clinic"] = aClinic
                try:
                    medical_history = MedicalHistory.objects.filter(**kwargs)
                except:
                    medical_history = None

        if not medical_history and not badRequest:
            raise NotFound
        elif not badRequest:
            if medical_history_id:
                ret = self.serialize(medical_history)
            else:
                ret = []
                for x in medical_history:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        print data

        try:
            if not (data["health"] == "Good" or data["health"] == "Poor"):
                valid = False
            else:
                if data["health"] == "Good":
                    kwargs["health"] = 'g'
                else:
                    kwargs["health"] = 'p'
            val = data["pain"] 
            if not (val == True or val == False):
                valid = False
            val = data["recentcold"] 
            if not (val == True or val == False):
                valid = False
            val = data["hivaids"] 
            if not (val == True or val == False):
                valid = False
            val = data["anemia"]
            if not (val == True or val == False):
                valid = False
            val = data["athsma"]
            if not (val == True or val == False):
                valid = False
            val = data["cancer"]
            if not (val == True or val == False):
                valid = False
            val = data["congenitalheartdefect"] 
            if not (val == True or val == False):
                valid = False
            val = data["diabetes"] 
            if not (val == True or val == False):
                valid = False
            val = data["epilepsy"] 
            if not (val == True or val == False):
                valid = False
            val = data["hemophilia"] 
            if not (val == True or val == False):
                valid = False
            val = data["hepititis"] 
            if not (val == True or val == False):
                valid = False
            val = data["tuberculosis"] 
            if not (val == True or val == False):
                valid = False
            val = data["troublespeaking"] 
            if not (val == True or val == False):
                valid = False
            val = data["troublehearing"] 
            if not (val == True or val == False):
                valid = False
            val = data["troubleeating"] 
            if not (val == True or val == False):
                valid = False
            val = int(data["pregnancy_duration"])
            if val < 5 or val > 10:
                valid = False
            else:
                kwargs["pregnancy_duration"] = val
            val = data["pregnancy_smoke"] 
            if not (val == True or val == False):
                valid = False
            val = data["birth_complications"] 
            if not (val == True or val == False):
                valid = False
            val = data["pregnancy_complications"] 
            if not (val == True or val == False):
                valid = False
            val = data["mother_alcohol"] 
            if not (val == True or val == False):
                valid = False
            val = data["relative_cleft"] 
            if not (val == True or val == False):
                valid = False
            val = data["parents_cleft"] 
            if not (val == True or val == False):
                valid = False
            val = data["siblings_cleft"] 
            if not (val == True or val == False):
                valid = False
        except:
            print "Exception!"
            valid = False

        print valid
        return valid, kwargs

    def validatePutArgs(self, data, medical_history):
        valid = True

        try:
            if "health" in data:
                if not (data["health"] == "Good" or data["health"] == "Poor"):
                    valid = False
                else:
                    if data["health"] == "Good":
                        medical_history.health = 'g'
                    else:
                        medical_history.health = 'p'
            if "pain" in data:
                val = data["pain"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.pain = val
            if "recentcold" in data:
                val = data["recentcold"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.recentcold = val
            if "hivaids" in data:
                val = data["hivaids"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.hivaids = val
            if "anemia" in data:
                val = data["anemia"]
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.anemia = val
            if "athsma" in data:
                val = data["athsma"]
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.athsma = val
            if "cancer" in data:
                val = data["cancer"]
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.cancer = val
            if "congenitalheartdefect" in data:
                val = data["congenitalheartdefect"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.congenitalheartdefect = val
            if "diabetes" in data:
                val = data["diabetes"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.diabetes = val
            if "epilepsy" in data:
                val = data["epilepsy"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.epilepsy = val
            if "hemophilia" in data:
                val = data["hemophilia"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.hemophilia = val
            if "hepititis" in data:
                val = data["hepititis"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.hepititis = val
            if "tuberculosis" in data:
                val = data["tuberculosis"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.tuberculosis = val
            if "troublespeaking" in data:
                val = data["troublespeaking"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.troublespeaking = val
            if "troublehearing" in data:
                val = data["troublehearing"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.troublehearing = val
            if "troubleeating" in data:
                val = data["troubleeating"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.troubleeating = val
            if "pregnancy_duration" in data:
                val = int(data["pregnancy_duration"])
                if (val < 5 or val > 10):
                    valid = False
                else:
                    medical_history.pregnancy_duration = val
            if "pregnancy_smoke" in data:
                val = data["pregnancy_smoke"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.pregnancy_smoke = val
            if "birth_complications" in data:
                val = data["birth_complications"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.birth_complications = val
            if "pregnancy_complications" in data:
                val = data["pregnancy_complications"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.pregnancy_complications = val
            if "mother_alcohol" in data:
                val = data["mother_alcohol"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.mother_alcohol = val
            if "relative_cleft" in data:
                val = data["relative_cleft"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.foo = relative_cleft
            if "parents_cleft" in data:
                val = data["parents_cleft"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.parents_cleft = val
            if "siblings_cleft" in data:
                val = data["siblings_cleft"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.siblings_cleft = val
            if "meds" in data:
                val = data["meds"] 
                if not isinstance(val, basestring):
                    valid = False
                else:
                    medical_history.meds = val

            if "allergymeds" in data:
                val = data["allergymeds"] 
                if not isinstance(val, basestring):
                    valid = False
                else:
                    medical_history.meds = val
        except:
            valid = False

        return valid, medical_history

    def post(self, request, format=None):
        badRequest = False
        implError = False

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

        print valid, kwargs

        if not valid:
            badRequest = True

        if not badRequest:

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

        if not badRequest:
                
            try:
                kwargs["patient"] = aPatient
                kwargs["clinic"] = aClinic
                medical_history = MedicalHistory(**kwargs)
                if medical_history:
                    medical_history.save()
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
            return Response({'id': medical_history.id})

    def put(self, request, medical_history_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not medical_history_id:
            badRequest = True

        if not badRequest:
            medical_history = None

            try:
                medical_history = MedicalHistory.objects.get(id=medical_history_id)
            except:
                pass

            if not medical_history:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, medical_history = self.validatePutArgs(data, medical_history)
                    if valid: 
                        medical_history.save()
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
        
    def delete(self, request, medical_history_id=None, format=None):
        medical_history = None

        # see if the state change object exists

        if not medical_history_id:
            return HttpResponseBadRequest()
        try:
            medical_history = MedicalHistory.objects.get(id=medical_history_id)
        except:
            medical_history = None

        if not medical_history:
            raise NotFound
        else:
            medical_history.delete()

        return Response({})

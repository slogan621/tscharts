#(C) Copyright Syd Logan 2017-2021
#(C) Copyright Thousand Smiles Foundation 2017-2021
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

from common.decorators import *

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
        m["cold_cough_fever"] = entry.cold_cough_fever  
        m["hivaids"] = entry.hivaids 
        m["anemia"] = entry.anemia  
        m["athsma"] = entry.athsma 
        m["cancer"] = entry.cancer  
        m["congenitalheartdefect"] = entry.congenitalheartdefect 
        m["congenitalheartdefect_workup"] = entry.congenitalheartdefect_workup
        m["congenitalheartdefect_planforcare"] = entry.congenitalheartdefect_planforcare 
        m["diabetes"] = entry.diabetes 
        m["epilepsy"] = entry.epilepsy  
        m["bleeding_problems"] = entry.bleeding_problems  
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
        m["first_crawl"] = entry.first_crawl  
        m["first_sit"] = entry.first_sit  
        m["first_walk"] = entry.first_walk  
        m["first_words"] = entry.first_words  
        m["birth_weight"] = entry.birth_weight 
        m["birth_weight_metric"] = entry.birth_weight_metric 
        m["height"] = entry.height  
        m["height_metric"] = entry.height_metric  
        m["weight"] = entry.weight  
        m["weight_metric"] = entry.weight_metric  
        m["born_with_cleft_lip"] = entry.born_with_cleft_lip  
        m["born_with_cleft_palate"] = entry.born_with_cleft_palate  

        return m

    @log_request
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
            elif case1 and len(medical_history) == 1:
                ret = self.serialize(medical_history[0])
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

        try:
            val = data["cold_cough_fever"] 
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
            val = data["congenitalheartdefect_workup"] 
            if not (val == True or val == False):
                valid = False
            val = data["congenitalheartdefect_planforcare"] 
            if not (val == True or val == False):
                valid = False
            val = data["diabetes"] 
            if not (val == True or val == False):
                valid = False
            val = data["epilepsy"] 
            if not (val == True or val == False):
                valid = False
            val = data["bleeding_problems"] 
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
            val = int(data["first_crawl"])
            if val < 0:
                valid = False
            else:
                kwargs["first_crawl"] = val
            val = int(data["first_sit"])
            if val < 0:
                valid = False
            else:
                kwargs["first_sit"] = val
            val = int(data["first_walk"])
            if val < 0:
                valid = False
            else:
                kwargs["first_walk"] = val
            val = int(data["first_words"])
            if val < 0:
                valid = False
            else:
                kwargs["first_words"] = val
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
            val = int(data["birth_weight"])
            if val < 0:
                valid = False
            else:
                kwargs["birth_weight"] = val
            val = data["birth_weight_metric"]
            if not (val == True or val == False):
                valid = False
            val = int(data["height"])
            if val < 0:
                valid = False
            else:
                kwargs["height"] = val
            val = data["height_metric"]
            if not (val == True or val == False):
                valid = False
            val = int(data["weight"])
            if val < 0:
                valid = False
            else:
                kwargs["weight"] = val
            val = data["weight_metric"]
            if not (val == True or val == False):
                valid = False
            val = data["born_with_cleft_lip"] 
            if not (val == True or val == False):
                valid = False
            val = data["born_with_cleft_palate"] 
            if not (val == True or val == False):
                valid = False
        except:
            valid = False

        return valid, kwargs

    def validatePutArgs(self, data, medical_history):
        valid = True

        try:
            if "cold_cough_fever" in data:
                val = data["cold_cough_fever"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.cold_cough_fever = val
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
            if "congenitalheartdefect_workup" in data:
                val = data["congenitalheartdefect_workup"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.congenitalheartdefect_workup = val
            if "congenitalheartdefect_planforcare" in data:
                val = data["congenitalheartdefect_planforcare"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.congenitalheartdefect_planforcare = val
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
            if "bleeding_problems" in data:
                val = data["bleeding_problems"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.bleeding_problems = val
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
                    medical_history.relative_cleft = val
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
                    medical_history.allergymeds = val

            if "first_crawl" in data:
                val = int(data["first_crawl"])
                if (val < 0):
                    valid = False
                else:
                    medical_history.first_crawl = val
            if "first_sit" in data:
                val = int(data["first_sit"])
                if (val < 0):
                    valid = False
                else:
                    medical_history.first_sit = val
            if "first_walk" in data:
                val = int(data["first_walk"])
                if (val < 0):
                    valid = False
                else:
                    medical_history.first_walk = val
            if "first_words" in data:
                val = int(data["first_words"])
                if (val < 0):
                    valid = False
                else:
                    medical_history.first_words = val
            if "birth_weight" in data:
                val = int(data["birth_weight"])
                if (val < 0):
                    valid = False
                else:
                    medical_history.birth_weight = val
            if "birth_weight_metric" in data:
                val = data["birth_weight_metric"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.birth_weight_metric = val
            if "height" in data:
                val = int(data["height"])
                if (val < 0):
                    valid = False
                else:
                    medical_history.height = val
            if "height_metric" in data:
                val = data["height_metric"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.height_metric = val
            if "weight" in data:
                val = int(data["weight"])
                if (val < 0):
                    valid = False
                else:
                    medical_history.weight = val
            if "weight_metric" in data:
                val = data["weight_metric"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.weight_metric = val
            if "born_with_cleft_lip" in data:
                val = data["born_with_cleft_lip"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.born_with_cleft_lip = val
            if "born_with_cleft_palate" in data:
                val = data["born_with_cleft_palate"] 
                if not (val == True or val == False):
                    valid = False
                else:
                    medical_history.born_with_cleft_palate = val
        except:
            valid = False

        return valid, medical_history

    @log_request
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

    @log_request
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
       
    @log_request 
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

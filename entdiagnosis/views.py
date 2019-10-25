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
from entdiagnosis.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

class ENTDiagnosisView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    sideKeyNames = ["hlConductive", "hl", "hlMixed", "hlSensory", "externalCerumenImpaction", "externalEarCanalFB", "externalMicrotia", "tympanicAtelectasis", "tympanicGranuloma", "tympanicMonomer", "tympanicTube", "tympanicPerf", "middleEarCholesteatoma", "middleEarEustTubeDysTMRetraction", "middleEarOtitisMedia", "middleEarSerousOtitisMedia", "syndromeHemifacialMicrosomia", "syndromePierreRobin"]
    booleanKeyNames = ["oralAnkyloglossia", "oralTonsilEnlarge", "oralCleftLipRepairDeformity", "oralCleftLipUnilateral", "oralCleftLipBilateral", "oralCleftLipUnrepaired", "oralCleftLipRepaired", "oralCleftPalateUnilateral", "oralCleftPalateBilateral", "oralCleftPalateUnrepaired", "oralCleftPalateRepaired", "oralSpeechProblem", "noseDeviatedSeptum", "noseTurbinateHypertrophy", "noseDeformitySecondaryToCleftPalate"]

    def sideToString(self, val):
        ret = None 
        data = {ENTDiagnosis.EAR_SIDE_LEFT:"left",
                ENTDiagnosis.EAR_SIDE_RIGHT:"right",
                ENTDiagnosis.EAR_SIDE_BOTH:"both",
                ENTDiagnosis.EAR_SIDE_NONE:"none"}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToSide(self, val):
        ret = None 
        data = {"left":ENTDiagnosis.EAR_SIDE_LEFT,
                "right":ENTDiagnosis.EAR_SIDE_RIGHT,
                "both":ENTDiagnosis.EAR_SIDE_BOTH,
                "none":ENTDiagnosis.EAR_SIDE_NONE}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["username"] = entry.username
        m["time"] = entry.time
        m["comment"] = entry.comment 

        m["hlConductive"] = self.sideToString(entry.hlConductive)
        m["hl"] = self.sideToString(entry.hl)
        m["hlMixed"] = self.sideToString(entry.hlMixed)
        m["hlSensory"] = self.sideToString(entry.hlSensory)
        m["externalCerumenImpaction"] = self.sideToString(entry.externalCerumenImpaction)
        m["externalEarCanalFB"] = self.sideToString(entry.externalEarCanalFB)
        m["externalMicrotia"] = self.sideToString(entry.externalMicrotia)
        m["tympanicAtelectasis"] = self.sideToString(entry.tympanicAtelectasis)
        m["tympanicGranuloma"] = self.sideToString(entry.tympanicGranuloma)
        m["tympanicMonomer"] = self.sideToString(entry.tympanicMonomer)
        m["tympanicTube"] = self.sideToString(entry.tympanicTube)
        m["tympanicPerf"] = self.sideToString(entry.tympanicPerf)
        m["middleEarCholesteatoma"] = self.sideToString(entry.middleEarCholesteatoma)
        m["middleEarEustTubeDysTMRetraction"] = self.sideToString(entry.middleEarEustTubeDysTMRetraction)
        m["middleEarOtitisMedia"] = self.sideToString(entry.middleEarOtitisMedia)
        m["middleEarSerousOtitisMedia"] = self.sideToString(entry.middleEarSerousOtitisMedia)
        m["syndromeHemifacialMicrosomia"] = self.sideToString(entry.syndromeHemifacialMicrosomia)
        m["syndromePierreRobin"] = self.sideToString(entry.syndromePierreRobin)

        m["oralAnkyloglossia"] = entry.oralAnkyloglossia
        m["oralTonsilEnlarge"] = entry.oralTonsilEnlarge
        m["oralCleftLipRepairDeformity"] = entry.oralCleftLipRepairDeformity
        m["oralCleftLipUnilateral"] = entry.oralCleftLipUnilateral
        m["oralCleftLipBilateral"] = entry.oralCleftLipBilateral
        m["oralCleftLipUnrepaired"] = entry.oralCleftLipUnrepaired
        m["oralCleftLipRepaired"] = entry.oralCleftLipRepaired
        m["oralCleftPalateUnilateral"] = entry.oralCleftPalateUnilateral
        m["oralCleftPalateBilateral"] = entry.oralCleftPalateBilateral
        m["oralCleftPalateUnrepaired"] = entry.oralCleftPalateUnrepaired
        m["oralCleftPalateRepaired"] = entry.oralCleftPalateRepaired
        m["oralSpeechProblem"] = entry.oralSpeechProblem
        m["noseDeviatedSeptum"] = entry.noseDeviatedSeptum
        m["noseTurbinateHypertrophy"] = entry.noseTurbinateHypertrophy
        m["noseDeformitySecondaryToCleftPalate"] = entry.noseDeformitySecondaryToCleftPalate
        return m

    @log_request
    def get(self, request, ent_diagnosis_id=None, format=None):
        ent_diagnosis = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if ent_diagnosis_id:
            try:
                ent_diagnosis = ENTDiagnosis.objects.get(id = ent_diagnosis_id)
            except:
                ent_diagnosis = None
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

            if not badRequest:
                try:
                    ent_diagnosis = ENTDiagnosis.objects.filter(**kwargs)
                except:
                    ent_diagnosis = None

        if not ent_diagnosis and not badRequest:
            raise NotFound
        elif not badRequest:
            if ent_diagnosis_id:
                ret = self.serialize(ent_diagnosis)
            else:
                ret = []
                for x in ent_diagnosis:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if not "clinic" in data:
            valid = False

        if not "patient" in data:
            valid = False

        if not "comment" in data:
            valid = False

        if not "username" in data:
            valid = False
        elif len(data["username"]) == 0:
            valid = False
        
        for x in self.sideKeyNames:
            if not x in data:
                valid = False
                break
            try:
                val = self.stringToSide(data[x])
                if val == None:
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                valid = False
                break

        for x in self.booleanKeyNames:
            if not x in data:
                valid = False
                break
            try:
                val = data[x]
                if not val in [True, False]:
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                valid = False
                break

        return valid, kwargs

    def validatePutArgs(self, data, ent_diagnosis):
        valid = True
        foundOne = False

        for x in self.sideKeyNames:
            if not x in data:
                continue
            try:
                val = self.stringToSide(data[x])
                if val == None:
                    valid = False
                    break
                else:
                    if x == "hlConductive":
                        ent_diagnosis.hlConductive = val
                        foundOne = True
                    elif x == "hl":
                        ent_diagnosis.hl = val
                        foundOne = True
                    elif x == "hlMixed":
                        ent_diagnosis.hlMixed = val
                        foundOne = True
                    elif x == "hlSensory":
                        ent_diagnosis.hlSensory = val
                        foundOne = True
                    elif x == "externalCerumenImpaction":
                        ent_diagnosis.externalCerumenImpaction = val
                        foundOne = True
                    elif x == "externalEarCanalFB":
                        ent_diagnosis.externalEarCanalFB = val
                        foundOne = True
                    elif x == "externalMicrotia":
                        ent_diagnosis.externalMicrotia = val
                        foundOne = True
                    elif x == "tympanicAtelectasis":
                        ent_diagnosis.tympanicAtelectasis = val
                        foundOne = True
                    elif x == "tympanicGranuloma":
                        ent_diagnosis.tympanicGranuloma = val
                        foundOne = True
                    elif x == "tympanicMonomer":
                        ent_diagnosis.tympanicMonomer = val
                        foundOne = True
                    elif x == "tympanicTube":
                        ent_diagnosis.tympanicTube = val
                        foundOne = True
                    elif x == "tympanicPerf":
                        ent_diagnosis.tympanicPerf = val
                        foundOne = True
                    elif x == "middleEarCholesteatoma":
                        ent_diagnosis.middleEarCholesteatoma = val
                        foundOne = True
                    elif x == "middleEarEustTubeDysTMRetraction":
                        ent_diagnosis.middleEarEustTubeDysTMRetraction = val
                        foundOne = True
                    elif x == "middleEarOtitisMedia":
                        ent_diagnosis.middleEarOtitisMedia = val
                        foundOne = True
                    elif x == "middleEarSerousOtitisMedia":
                        ent_diagnosis.middleEarSerousOtitisMedia = val
                        foundOne = True
                    elif x == "syndromeHemifacialMicrosomia":
                        ent_diagnosis.syndromeHemifacialMicrosomia = val
                        foundOne = True
                    elif x == "syndromePierreRobin":
                        ent_diagnosis.syndromePierreRobin = val
                        foundOne = True
            except:
                valid = False
                break

            if foundOne == False:
                valid = False

        for x in self.booleanKeyNames:
            if not x in data:
                continue
            try:
                val = data[x]
                if val == None:
                    valid = False
                    break
                elif not val in [True, False]:
                    valid = False
                    break
                    
                if x == "oralAnkyloglossia":
                    ent_diagnosis.oralAnkyloglossia = val
                    foundOne = True
                elif x == "oralTonsilEnlarge":
                    ent_diagnosis.oralTonsilEnlarge = val
                    foundOne = True
                elif x == "oralCleftLipRepairDeformity":
                    ent_diagnosis.oralCleftLipRepairDeformity = val
                    foundOne = True
                elif x == "oralCleftLipUnilateral":
                    ent_diagnosis.oralCleftLipUnilateral = val
                    foundOne = True
                elif x == "oralCleftLipBilateral":
                    ent_diagnosis.oralCleftLipBilateral = val
                    foundOne = True
                elif x == "oralCleftLipUnrepaired":
                    ent_diagnosis.oralCleftLipUnrepaired = val
                    foundOne = True
                elif x == "oralCleftLipRepaired":
                    ent_diagnosis.oralCleftLipRepaired = val
                    foundOne = True
                elif x == "oralCleftPalateUnilateral":
                    ent_diagnosis.oralCleftPalateUnilateral = val
                    foundOne = True
                elif x == "oralCleftPalateBilateral": 
                    ent_diagnosis.oralCleftPalateBilateral = val
                    foundOne = True
                elif x == "oralCleftPalateUnrepaired":
                    ent_diagnosis.oralCleftPalateUnrepaired = val
                    foundOne = True
                elif x == "oralCleftPalateRepaired":
                    ent_diagnosis.oralCleftPalateRepaired = val
                    foundOne = True
                elif x == "oralSpeechProblem":
                    ent_diagnosis.oralSpeechProblem = val
                    foundOne = True
                elif x == "noseDeviatedSeptum":
                    ent_diagnosis.noseDeviatedSeptum = val
                    foundOne = True
                elif x == "noseTurbinateHypertrophy":
                    ent_diagnosis.noseTurbinateHypertrophy = val
                    foundOne = True
                elif x == "noseDeformitySecondaryToCleftPalate":
                    ent_diagnosis.noseDeformitySecondaryToCleftPalate = val
                    foundOne = True
            except:
                valid = False
                break

        if foundOne == False:
            valid = False

        return valid, ent_diagnosis

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
                ent_diagnosis = ENTDiagnosis(**kwargs)
                if ent_diagnosis:
                    ent_diagnosis.save()
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
            return Response({'id': ent_diagnosis.id})

    @log_request
    def put(self, request, ent_diagnosis_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_diagnosis_id:
            badRequest = True

        if not badRequest:
            ent_diagnosis = None

            try:
                ent_diagnosis = ENTDiagnosis.objects.get(id=ent_diagnosis_id)
            except:
                pass

            if not ent_diagnosis:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, ent_diagnosis = self.validatePutArgs(data, ent_diagnosis)
                    if valid: 
                        ent_diagnosis.save()
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
    def delete(self, request, ent_diagnosis_id=None, format=None):
        ent_diagnosis = None

        # see if the ent exam object exists

        if not ent_diagnosis_id:
            return HttpResponseBadRequest()
        try:
            ent_diagnosis = ENTDiagnosis.objects.get(id=ent_diagnosis_id)
        except:
            ent_diagnosis = None

        if not ent_diagnosis:
            raise NotFound
        else:
            ent_diagnosis.delete()

        return Response({})

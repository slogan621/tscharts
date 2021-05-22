#(C) Copyright Syd Logan 2019-2021
#(C) Copyright Thousand Smiles Foundation 2019-2021
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
from entexam.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

class ENTExamView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def tubeToString(self, val):
        ret = None 
        data = {ENTExam.ENT_TUBE_IN_PLACE:"in place",
                ENTExam.ENT_TUBE_EXTRUDING:"extruding", 
                ENTExam.ENT_TUBE_IN_CANAL:"in canal",
                ENTExam.ENT_TUBE_NONE:"none"}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def stringToTube(self, val):
        ret = None
        data = {"in place":ENTExam.ENT_TUBE_IN_PLACE,
                "extruding":ENTExam.ENT_TUBE_EXTRUDING, 
                "in canal":ENTExam.ENT_TUBE_IN_CANAL,
                "none":ENTExam.ENT_TUBE_NONE}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def tympanoToString(self, val):
        ret = None      
        data = {ENTExam.ENT_TYMPANOSCLEROSIS_ANTERIOR:'anterior', 
                ENTExam.ENT_TYMPANOSCLEROSIS_POSTERIOR:'posterior', 
                ENTExam.ENT_TYMPANOSCLEROSIS_25:'25 percent', 
                ENTExam.ENT_TYMPANOSCLEROSIS_50:'50 percent', 
                ENTExam.ENT_TYMPANOSCLEROSIS_75:'75 percent', 
                ENTExam.ENT_TYMPANOSCLEROSIS_TOTAL:'total', 
                ENTExam.ENT_TYMPANOSCLEROSIS_NONE:'none'}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def stringToTympano(self, val):
        ret = None 
        data = {'anterior': ENTExam.ENT_TYMPANOSCLEROSIS_ANTERIOR, 
                'posterior': ENTExam.ENT_TYMPANOSCLEROSIS_POSTERIOR, 
                '25 percent': ENTExam.ENT_TYMPANOSCLEROSIS_25, 
                '50 percent': ENTExam.ENT_TYMPANOSCLEROSIS_50, 
                '75 percent': ENTExam.ENT_TYMPANOSCLEROSIS_75, 
                'total': ENTExam.ENT_TYMPANOSCLEROSIS_TOTAL, 
                'none': ENTExam.ENT_TYMPANOSCLEROSIS_NONE}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def perfToString(self, val):
        ret = None      
        data = {ENTExam.ENT_PERF_ANTERIOR:'anterior', 
                ENTExam.ENT_PERF_POSTERIOR:'posterior', 
                ENTExam.ENT_PERF_MARGINAL:'marginal', 
                ENTExam.ENT_PERF_25:'25 percent', 
                ENTExam.ENT_PERF_50:'50 percent', 
                ENTExam.ENT_PERF_75:'75 percent', 
                ENTExam.ENT_PERF_TOTAL:'total', 
                ENTExam.ENT_PERF_NONE:'none'}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def stringToPerf(self, val):
        ret = None 
        data = {'anterior': ENTExam.ENT_PERF_ANTERIOR, 
                'posterior': ENTExam.ENT_PERF_POSTERIOR, 
                'marginal': ENTExam.ENT_PERF_MARGINAL, 
                '25 percent': ENTExam.ENT_PERF_25, 
                '50 percent': ENTExam.ENT_PERF_50, 
                '75 percent': ENTExam.ENT_PERF_75, 
                'total': ENTExam.ENT_PERF_TOTAL, 
                'none': ENTExam.ENT_PERF_NONE}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def sideToString(self, val):
        ret = None 
        data = {ENTExam.EAR_SIDE_LEFT:"left",
                ENTExam.EAR_SIDE_RIGHT:"right",
                ENTExam.EAR_SIDE_BOTH:"both",
                ENTExam.EAR_SIDE_NONE:"none"}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToSide(self, val):
        ret = None 
        data = {"left":ENTExam.EAR_SIDE_LEFT,
                "right":ENTExam.EAR_SIDE_RIGHT,
                "both":ENTExam.EAR_SIDE_BOTH,
                "none":ENTExam.EAR_SIDE_NONE}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def voiceTestToString(self, val):
        ret = None 
        data = {ENTExam.ENT_VOICE_TEST_NORMAL:"normal",
                ENTExam.ENT_VOICE_TEST_ABNORMAL:"abnormal",
                ENTExam.ENT_VOICE_TEST_NONE:"none"}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToVoiceTest(self, val):
        ret = None 
        data = {"normal":ENTExam.ENT_VOICE_TEST_NORMAL,
                "abnormal":ENTExam.ENT_VOICE_TEST_ABNORMAL,
                "none":ENTExam.ENT_VOICE_TEST_NONE}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def forkTestToString(self, val):
        ret = None 
        data = {ENTExam.ENT_FORK_TEST_A_GREATER_B:"a greater b",
                ENTExam.ENT_FORK_TEST_B_GREATER_A:"b greater a",
                ENTExam.ENT_FORK_TEST_EQUAL:"a equal b",
                ENTExam.ENT_FORK_TEST_NONE:"none"}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToForkTest(self, val):
        ret = None 
        data = {"a greater b":ENTExam.ENT_FORK_TEST_A_GREATER_B,
                "b greater a":ENTExam.ENT_FORK_TEST_B_GREATER_A,
                "a equal b":ENTExam.ENT_FORK_TEST_EQUAL,
                "none":ENTExam.ENT_FORK_TEST_NONE}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def bcToString(self, val):
        ret = None 

        data = {ENTExam.ENT_BC_AD_LAT_TO_AD: 'ad lat ad',
                ENTExam.ENT_BC_AD_LAT_TO_AS: 'ad lat as',
                ENTExam.ENT_BC_AS_LAT_TO_AD: 'as lat ad', 
                ENTExam.ENT_BC_AS_LAT_TO_AS: 'as lat as', 
                ENTExam.ENT_BC_NONE: 'none'}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToBc(self, val):
        ret = None 

        data = {'ad lat ad': ENTExam.ENT_BC_AD_LAT_TO_AD,
                'ad lat as': ENTExam.ENT_BC_AD_LAT_TO_AS,
                'as lat ad': ENTExam.ENT_BC_AS_LAT_TO_AD, 
                'as lat as': ENTExam.ENT_BC_AS_LAT_TO_AS, 
                'none': ENTExam.ENT_BC_NONE}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def forkToString(self, val):
        ret = None 

        data = {ENTExam.ENT_FORK_256: '256',
                ENTExam.ENT_FORK_512: '512',
                ENTExam.ENT_FORK_NONE: 'none'}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToFork(self, val):
        ret = None 

        data = {'256': ENTExam.ENT_FORK_256,
                '512': ENTExam.ENT_FORK_512,
                'none': ENTExam.ENT_BC_NONE}

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

        m["normal"] = self.sideToString(entry.normal)
        m["microtia"] = self.sideToString(entry.microtia)
        m["wax"] = self.sideToString(entry.wax)
        m["drainage"] = self.sideToString(entry.drainage)
        m["externalOtitis"] = self.sideToString(entry.externalOtitis)
        m["fb"] = self.sideToString(entry.fb)
        m["tubeRight"] = self.tubeToString(entry.tubeRight)
        m["tubeLeft"] = self.tubeToString(entry.tubeLeft)
        m["tympanoRight"] = self.tympanoToString(entry.tympanoRight)
        m["tympanoLeft"] = self.tympanoToString(entry.tympanoLeft)
        m["tmGranulations"] = self.sideToString(entry.tmGranulations)
        m["tmRetraction"] = self.sideToString(entry.tmRetraction)
        m["tmAtelectasis"] = self.sideToString(entry.tmAtelectasis)
        m["perfLeft"] = self.perfToString(entry.perfLeft)
        m["perfRight"] = self.perfToString(entry.perfRight)
        m["voiceTest"] = self.voiceTestToString(entry.voiceTest)
        m["forkAD"] = self.forkTestToString(entry.forkAD)
        m["forkAS"] = self.forkTestToString(entry.forkAS)
        m["bc"] = self.bcToString(entry.bc)
        m["fork"] = self.forkToString(entry.fork)
        m["effusion"] = self.sideToString(entry.effusion)
        m["middle_ear_infection"] = self.sideToString(entry.middle_ear_infection)

        return m

    @log_request
    def get(self, request, ent_exam_id=None, format=None):
        ent_exam = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if ent_exam_id:
            try:
                ent_exam = ENTExam.objects.get(id = ent_exam_id)
            except:
                ent_exam = None
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
                    ent_exam = ENTExam.objects.filter(**kwargs)
                except:
                    ent_exam = None

        if not ent_exam and not badRequest:
            raise NotFound
        elif not badRequest:
            if ent_exam_id:
                ret = self.serialize(ent_exam)
            else:
                ret = []
                for x in ent_exam:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if not "comment" in data:
            valid = False

        if not "username" in data:
            valid = False
        elif len(data["username"]) == 0:
            valid = False

        try:
            val = self.stringToSide(data["normal"])
            if val == None:
                valid = False
            else:
                kwargs["normal"] = val
        except:
            valid = False
        try:
            val = self.stringToSide(data["microtia"])
            if val == None:
                valid = False
            else:
                kwargs["microtia"] = val
        except:
            valid = False
        try:
            val = self.stringToSide(data["wax"])
            if val == None:
                valid = False
            else:
                kwargs["wax"] = val
        except:
            valid = False
        try:
            val = self.stringToSide(data["drainage"])
            if val == None:
                valid = False
            else:
                kwargs["drainage"] = val
        except:
            valid = False
        try:
            val = self.stringToSide(data["externalOtitis"])
            if val == None:
                valid = False
            else:
                kwargs["externalOtitis"] = val
        except:
            valid = False
        try:
            val = self.stringToSide(data["fb"])
            if val == None:
                valid = False
            else:
                kwargs["fb"] = val
        except:
            valid = False

        try:
            val = self.stringToTube(data["tubeRight"])
            if val == None:
                valid = False
            else:
                kwargs["tubeRight"] = val
        except:
            valid = False
        try:
            val = self.stringToTube(data["tubeLeft"])
            if val == None:
                valid = False
            else:
                kwargs["tubeLeft"] = val
        except:
            valid = False

        try:
            val = self.stringToTympano(data["tympanoLeft"])
            if val == None:
                valid = False
            else:
                kwargs["tympanoLeft"] = val
        except:
            valid = False

        try:
            val = self.stringToTympano(data["tympanoRight"])
            if val == None:
                valid = False
            else:
                kwargs["tympanoRight"] = val
        except:
            valid = False

        try:
            val = self.stringToSide(data["tmGranulations"])
            if val == None:
                valid = False
            else:
                kwargs["tmGranulations"] = val
        except:
            valid = False

        try:
            val = self.stringToSide(data["tmRetraction"])
            if val == None:
                valid = False
            else:
                kwargs["tmRetraction"] = val
        except:
            valid = False

        try:
            val = self.stringToSide(data["tmAtelectasis"])
            if val == None:
                valid = False
            else:
                kwargs["tmAtelectasis"] = val
        except:
            valid = False

        try:
            val = self.stringToPerf(data["perfRight"])
            if val == None:
                valid = False
            else:
                kwargs["perfRight"] = val
        except:
            valid = False

        try:
            val = self.stringToPerf(data["perfLeft"])
            if val == None:
                valid = False
            else:
                kwargs["perfLeft"] = val
        except:
            valid = False

        try:
            val = self.stringToVoiceTest(data["voiceTest"])
            if val == None:
                valid = False
            else:
                kwargs["voiceTest"] = val
        except:
            valid = False

        try:
            val = self.stringToForkTest(data["forkAD"])
            if val == None:
                valid = False
            else:
                kwargs["forkAD"] = val
        except:
            valid = False

        try:
            val = self.stringToForkTest(data["forkAS"])
            if val == None:
                valid = False
            else:
                kwargs["forkAS"] = val
        except:
            valid = False

        try:
            val = self.stringToBc(data["bc"])
            if val == None:
                valid = False
            else:
                kwargs["bc"] = val
        except:
            valid = False

        try:
            val = self.stringToFork(data["fork"])
            if val == None:
                valid = False
            else:
                kwargs["fork"] = val
        except:
            valid = False

        try:
            val = self.stringToSide(data["effusion"])
            if val == None:
                valid = False
            else:
                kwargs["effusion"] = val
        except:
            valid = False

        try:
            val = self.stringToSide(data["middle_ear_infection"])
            if val == None:
                valid = False
            else:
                kwargs["middle_ear_infection"] = val
        except:
            valid = False

        return valid, kwargs

    def validatePutArgs(self, data, ent_exam):
        valid = True

        try:
            if "normal" in data:
                val = self.stringToSide(data["normal"])
                if val == None:
                    valid = False
                else:
                    ent_exam.normal = val
        except:
            pass

        try:
            if "microtia" in data:
                val = self.stringToSide(data["microtia"])
                if val == None:
                    valid = False
                else:
                    ent_exam.microtia = val
        except:
            pass

        try:
            if "wax" in data:
                val = self.stringToSide(data["wax"])
                if val == None:
                    valid = False
                else:
                    ent_exam.wax = val
        except:
            pass

        try:
            if "drainage" in data:
                val = self.stringToSide(data["drainage"])
                if val == None:
                    valid = False
                else:
                    ent_exam.drainage = val
        except:
            pass

        try:
            if "externalOtitis" in data:
                val = self.stringToSide(data["externalOtitis"])
                if val == None:
                    valid = False
                else:
                    ent_exam.externalOtitis = val
        except:
            pass

        try:
            if "fb" in data:
                val = self.stringToSide(data["fb"])
                if val == None:
                    valid = False
                else:
                    ent_exam.fb = val
        except:
            pass

        try:
            if "tubeRight" in data:
                val = self.stringToTube(data["tubeRight"])
                if val == None:
                    valid = False
                else:
                    ent_exam.tubeRight = val
        except:
            pass

        try:
            if "tubeLeft" in data:
                val = self.stringToTube(data["tubeLeft"])
                if val == None:
                    valid = False
                else:
                    ent_exam.tubeLeft = val
        except:
            pass

        try:
            if "tympanoLeft" in data:
                val = self.stringToTympano(data["tympanoLeft"])
                if val == None:
                    valid = False
                else:
                    ent_exam.tympanoLeft = val
        except:
            pass

        try:
            if "tympanoRight" in data:
                val = self.stringToTympano(data["tympanoRight"])
                if val == None:
                    valid = False
                else:
                    ent_exam.tympanoRight = val
        except:
            pass

        try:
            if "tmGranulations" in data:
                val = self.stringToSide(data["tmGranulations"])
                if val == None:
                    valid = False
                else:
                    ent_exam.tmGranulations = val
        except:
            pass

        try:
            if "tmRetraction" in data:
                val = self.stringToSide(data["tmRetraction"])
                if val == None:
                    valid = False
                else:
                    ent_exam.tmRetraction = val
        except:
            pass

        try:
            if "tmAtelectasis" in data:
                val = self.stringToSide(data["tmAtelectasis"])
                if val == None:
                    valid = False
                else:
                    ent_exam.tmAtelectasis = val
        except:
            pass

        try:
            if "perfRight" in data:
                val = self.stringToPerf(data["perfRight"])
                if val == None:
                    valid = False
                else:
                    ent_exam.perfRight = val
        except:
            pass

        try:
            if "perfLeft" in data:
                val = self.stringToPerf(data["perfLeft"])
                if val == None:
                    valid = False
                else:
                    ent_exam.perfLeft = val
        except:
            pass

        try:
            if "voiceTest" in data:
                val = self.stringToVoiceTest(data["voiceTest"])
                if val == None:
                    valid = False
                else:
                    ent_exam.voiceTest = val
        except:
            pass

        try:
            if "forkAD" in data:
                val = self.stringToForkTest(data["forkAD"])
                if val == None:
                    valid = False
                else:
                    ent_exam.forkAD = val
        except:
            pass

        try:
            if "forkAS" in data:
                val = self.stringToForkTest(data["forkAS"])
                if val == None:
                    valid = False
                else:
                    ent_exam.forkAS = val
        except:
            pass

        try:
            if "bc" in data:
                val = self.stringToBc(data["bc"])
                if val == None:
                    valid = False
                else:
                    ent_exam.bc = val
        except:
            pass

        try:
            if "fork" in data:
                val = self.stringToFork(data["fork"])
                if val == None:
                    valid = False
                else:
                    ent_exam.fork = val
        except:
            pass

        try:
            if "clinic" in data:
                aClinic = Clinic.objects.get(id=int(data["clinic"]))
                ent_exam.clinic = data["clinic"]
        except:
            pass

        try:
            if "patient" in data:
                aPatient = Patient.objects.get(id=int(data["patient"]))
                ent_exam.patient = aPatient
        except:
            pass

        try:
            if "comment" in data:
                ent_exam.comment = data["comment"]
        except:
            pass

        try:
            if "effusion" in data:
                val = self.stringToSide(data["effusion"])
                if val == None:
                    valid = False
                else:
                    ent_exam.effusion = val
        except:
            pass


        try:
            if "middle_ear_infection" in data:
                val = self.stringToSide(data["middle_ear_infection"])
                if val == None:
                    valid = False
                else:
                    ent_exam.middle_ear_infection = val
        except:
            pass

        val = "normal" in data or "microtia" in data or "wax" in data or "drainage" in data or "externalOtitis" in data or "fb" in data or "tubeLeft" in data or "tubeRight" in data or "tympanoLeft" in data or "tympanoRight" in data or "tmGranulations" in data or "tmRetraction" in data or "tmAtelectasis" in data or "perfRight" in data or "perfLeft" in data or "voiceTest" in data or "forkAD" in data or "forkAS" in data or "bc" in data or "fork" in data or "comment" in data or "username" in data or "effusion" in data or "middle_ear_infection" in data
        if val == False:
            valid = False

        return valid, ent_exam

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
                ent_exam = ENTExam(**kwargs)
                if ent_exam:
                    ent_exam.save()
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
            return Response({'id': ent_exam.id})

    @log_request
    def put(self, request, ent_exam_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_exam_id:
            badRequest = True

        if not badRequest:
            ent_exam = None

            try:
                ent_exam = ENTExam.objects.get(id=ent_exam_id)
            except:
                pass

            if not ent_exam:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, ent_exam = self.validatePutArgs(data, ent_exam)
                    if valid: 
                        ent_exam.save()
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
    def delete(self, request, ent_exam_id=None, format=None):
        ent_exam = None

        # see if the ent exam object exists

        if not ent_exam_id:
            return HttpResponseBadRequest()
        try:
            ent_exam = ENTExam.objects.get(id=ent_exam_id)
        except:
            ent_exam = None

        if not ent_exam:
            raise NotFound
        else:
            ent_exam.delete()

        return Response({})

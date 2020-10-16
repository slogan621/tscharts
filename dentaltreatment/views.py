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
from clinic.models import *
from patient.models import *
from dentaltreatment.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *
#from collections import namedtuple

import traceback

import sys
import json

import logging

LOG = logging.getLogger("tscharts")

class DentalTreatmentView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    anestheticFields = [
        "localAnesthetic",
    ]

    integerFields = [
        "localAnestheticNumberCarps",
    ]

    booleanFields = [
  	"exam",
  	"prophy",
  	"srpUR",
  	"srpLR",
  	"srpUL",
  	"srpLL",
  	"xraysViewed",
  	"headNeckOralCancerExam",
  	"oralHygieneInstruction",
  	"flourideTxVarnish",
  	"nutritionalCounseling",
  	"orthoEvaluation",
  	"orthoTx",
  	"oralSurgeryEvaluation",
  	"oralSurgeryTx",
    ]

    textFields = [
        "username",
  	"examComment",
  	"prophyComment",
  	"srpComment",
  	"xraysViewedComment",
  	"headNeckOralCancerExamComment",
  	"oralHygieneInstructionComment",
  	"flourideTxVarnishComment",
  	"nutritionalCounselingComment",
  	"orthoEvaluationComment",
  	"orthoTxComment",
  	"oralSurgeryEvaluationComment",
  	"oralSurgeryTxComment",
  	"comment",
    ]

    def anestheticToString(self, val):
        ret = None
        for x in DentalTreatment.DENTAL_ANESTHETIC_CHOICES:
            if x[0] == val:
                ret = x[1]
                break
        return ret

    def stringToAnesthetic(self, val):
        ret = None
        for x in DentalTreatment.DENTAL_ANESTHETIC_CHOICES:
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

        m["exam"] = self.booleanToString(entry.exam)
        m["examComment"] = entry.examComment

        m["prophy"] = self.booleanToString(entry.prophy)
        m["prophyComment"] = entry.prophyComment

        m["srpUR"] = self.booleanToString(entry.srpUR)
        m["srpLR"] = self.booleanToString(entry.srpLR)
        m["srpUL"] = self.booleanToString(entry.srpUL)
        m["srpLL"] = self.booleanToString(entry.srpLL)
        m["srpComment"] = entry.srpComment

        m["xraysViewed"] = self.booleanToString(entry.xraysViewed)
        m["xraysViewedComment"] = entry.xraysViewedComment

        m["headNeckOralCancerExam"] = self.booleanToString(entry.headNeckOralCancerExam)
        m["headNeckOralCancerExamComment"] = entry.headNeckOralCancerExamComment


        m["oralHygieneInstruction"] = self.booleanToString(entry.oralHygieneInstruction)
        m["oralHygieneInstructionComment"] = entry.oralHygieneInstructionComment

        m["flourideTxVarnish"] = self.booleanToString(entry.flourideTxVarnish)
        m["flourideTxVarnishComment"] = entry.flourideTxVarnishComment

        m["nutritionalCounseling"] = self.booleanToString(entry.nutritionalCounseling)
        m["nutritionalCounselingComment"] = entry.nutritionalCounselingComment

        m["orthoEvaluation"] = self.booleanToString(entry.orthoEvaluation)
        m["orthoEvaluationComment"] = entry.orthoEvaluationComment
        m["orthoTx"] = self.booleanToString(entry.orthoTx)
        m["orthoTxComment"] = entry.orthoTxComment

        m["oralSurgeryEvaluation"] = self.booleanToString(entry.oralSurgeryEvaluation)
        m["oralSurgeryEvaluationComment"] = entry.oralSurgeryEvaluationComment
        m["oralSurgeryTx"] = self.booleanToString(entry.oralSurgeryTx)
        m["oralSurgeryTxComment"] = entry.oralSurgeryTxComment

        m["localAnesthetic"] = self.anestheticToString(entry.localAnesthetic)
        m["localAnestheticNumberCarps"] = entry.localAnestheticNumberCarps
        m["localAnestheticComment"] = entry.localAnestheticComment

        m["comment"] = entry.comment

        return m

    @log_request
    def get(self, request, dental_treatment_id=None, format=None):
        dental_treatment = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if dental_treatment_id:
            try:
                dental_treatment = DentalTreatment.objects.get(id = dental_treatment_id)
            except:
                dental_treatment = None
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
                val = request.GET.get("localAnesthetic", '')
                if val != '':
                    val = self.stringToAnesthetic(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs[x] = val
            except:
                pass

            try:
                val = request.GET.get("localAnestheticNumberCarps", '')
                if val != '':
                    val = int(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs[x] = val
            except:
                pass

            for x in self.booleanFields:
                try:
                    val = request.GET.get(x, '')
                    if val != '':
                        val = self.stringToBoolean(val)
                        if val == None:
                            badRequest = True
                        else:
                            kwargs[x] = val
                except:
                    pass

            if not badRequest:
                try:
                    dental_treatment = DentalTreatment.objects.filter(**kwargs)
                except:
                    dental_treatment = None

        if not dental_treatment and not badRequest:
            raise NotFound
        elif not badRequest:
            if dental_treatment_id:
                ret = self.serialize(dental_treatment)
            else:
                ret = []
                for x in dental_treatment:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = {}
        kwargs = data

        for k, v in data.items():
            if not k in self.anestheticFields and not k in self.booleanFields and not k in self.textFields and not k in self.integerFields and k != "patient" and k != "clinic":
                valid = False
                LOG.warning("validatePostArgs: Failed to validate key {} value {}".format(k, v))
                break

        try:
            if not ("username" in data and len(data["username"]) > 0):
                valid = False
                LOG.warning("validatePostArgs: Failed to validate key username")
            else:
                kwargs["username"] = data["username"]
        except:
            LOG.warning("validatePostArgs: Exception: Failed to validate key username")
            valid = False

        try: 
            val = self.stringToAnesthetic(data["localAnesthetic"])
            if val == None:
                LOG.warning("validatePostArgs: Failed to validate key localAnesthetic val {}".format(data["localAnesthetic"]))
                valid = False
            else:
                kwargs["localAnesthetic"] = val
        except:
            LOG.warning("validatePostArgs: Failed to locate key {}: {}".format("localAnesthetic", sys.exc_info()[0]))
            valid = False
 
        try: 
            val = int(data["localAnestheticNumberCarps"])
            if val == None:
                LOG.warning("validatePostArgs: Failed to validate key localAnestheticNumberCarps val {}".format(data["localAnestheticNumberCarps"]))
                valid = False
            else:
                kwargs["localAnestheticNumberCarps"] = val
        except:
            LOG.warning("validatePostArgs: Failed to locate key {}".format("localAnestheticNumberCarps"))
            valid = False
 
        for x in self.booleanFields:
            try: 
                val = self.stringToBoolean(data[x])
                if val == None:
                    LOG.warning("validatePostArgs: Failed to validate key x {} val {}".format(x, data[x]))
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                LOG.warning("validatePostArgs: Failed to locate key x {}".format(x))
                valid = False

        for x in self.textFields:
            try: 
                val = str(data[x])
                if val == False:
                    LOG.warning("validatePostArgs: Failed to validate key x {} val {}".format(x, data[x]))
                    valid = False
                    break
                else:
                    kwargs[x] = data[x]
            except:
                LOG.warning("validatePostArgs: Failed to locate key x {}".format(x))
                valid = False

        return valid, kwargs

    def validatePutArgs(self, data, dental_treatment):
        valid = True
        found = False

        # first check to see if we have at least one item, and what
        # we have is paired with a valid value

        for k, v in data.items():
            if k in self.anestheticFields:
                found = True
                try:
                    z = self.stringToAnesthetic(v)
                    if z == None:
                        LOG.warning("validatePutArgs: invalid k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid k {} v {}".format(k, v))
                    valid = False

            elif k in self.booleanFields:
                found = True
                try:
                    z = self.stringToBoolean(v)
                    if z == None:
                        LOG.warning("validatePutArgs: invalid k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid k {} v {}".format(k, v))
                    valid = False

            elif k in self.integerFields:
                found = True
                try:
                    z = int(v)
                    if z == None:
                        LOG.warning("validatePutArgs: invalid k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid k {} v {}".format(k, v))
                    valid = False

            elif k in self.textFields:
                found = True
                try:
                    x = str(v)
                    if x == None:
                        LOG.warning("validatePutArgs: invalid text field k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid text field k {} v {}".format(k, v))
                    valid = False
            elif k in ["clinic", "patient", "id"]:
                found = True
            else:
                LOG.warning("validatePutArgs: unknown key k {} v {}".format(k, v))
                valid = False # unknown key

        # now, build up the dental treatment object

        if found == True and valid == True:
            for k, v in data.items():
                LOG.warning("validatePutArgs: bottom loop k {} v {}".format(k, v))
                if k == "exam":
                    dental_treatment.exam = self.stringToBoolean(v)
                elif k == "prophy":
                    dental_treatment.prophy = self.stringToBoolean(v)
  	        elif k == "srpUR":
                    dental_treatment.srpUR = self.stringToBoolean(v)
  	        elif k == "srpLR":
                    dental_treatment.srpLR = self.stringToBoolean(v)
  	        elif k == "srpUL":
                    dental_treatment.srpUL = self.stringToBoolean(v)
  	        elif k == "srpLL":
                    dental_treatment.srpLL = self.stringToBoolean(v)
  	        elif k == "xraysViewed":
                    dental_treatment.xraysViewed = self.stringToBoolean(v)
  	        elif k == "headNeckOralCancerExam":
                    dental_treatment.headNeckOralCancerExam = self.stringToBoolean(v)
  	        elif k == "oralHygieneInstruction":
                    dental_treatment.oralHygieneInstruction = self.stringToBoolean(v)
  	        elif k == "flourideTxVarnish":
                    dental_treatment.flourideTxVarnish = self.stringToBoolean(v)
  	        elif k == "nutritionalCounseling":
                    dental_treatment.nutritionalCounseling = self.stringToBoolean(v)
  	        elif k == "orthoEvaluation":
                    dental_treatment.orthoEvaluation = self.stringToBoolean(v)
  	        elif k == "orthoTx":
                    dental_treatment.orthoTx = self.stringToBoolean(v)
  	        elif k == "oralSurgeryEvaluation":
                    dental_treatment.oralSurgeryEvaluation = self.stringToBoolean(v)
  	        elif k == "oralSurgeryTx":
                    dental_treatment.oralSurgeryTx = self.stringToBoolean(v)
  	        elif k == "localAnesthetic":
                    dental_treatment.localAnesthetic = self.stringToAnesthetic(v)
  	        elif k == "localAnestheticNumberCarps":
                    dental_treatment.localAnestheticNumberCarps = int(v)

                elif k == "examComment":
                    dental_treatment.examComment = str(v)
                elif k == "prophyComment":
                    dental_treatment.prophyComment = str(v)
  	        elif k == "srpComment":
                    dental_treatment.srpComment = str(v)
  	        elif k == "xraysViewedComment":
                    dental_treatment.xraysViewedComment = str(v)
  	        elif k == "headNeckOralCancerExamComment":
                    dental_treatment.headNeckOralCancerExamComment = str(v)
  	        elif k == "oralHygieneInstructionComment":
                    dental_treatment.oralHygieneInstructionComment = str(v)
  	        elif k == "flourideTxVarnishComment":
                    dental_treatment.flourideTxVarnishComment = str(v)
  	        elif k == "nutritionalCounselingComment":
                    dental_treatment.nutritionalCounselingComment = str(v)
  	        elif k == "orthoEvaluationComment":
                    dental_treatment.orthoEvaluationComment = str(v)
  	        elif k == "orthoTxComment":
                    dental_treatment.orthoTxComment = str(v)
  	        elif k == "oralSurgeryEvaluationComment":
                    dental_treatment.oralSurgeryEvaluationComment = str(v)
  	        elif k == "oralSurgeryTxComment":
                    dental_treatment.oralSurgeryTxComment = str(v)
  	        elif k == "localAnestheticComment":
                    dental_treatment.localAnestheticComment = str(v)
  	        elif k == "localAnestheticNumberCarpsComment":
                    dental_treatment.localAnestheticNumberCarpsComment = str(v)
                elif k == "username":
                    dental_treatment.username = str(v)
  	        elif k == "comment":
                    dental_treatment.comment = str(v)

            try:
                if "clinic" in data:
                    aClinic = Clinic.objects.get(id=int(data["clinic"]))
                    dental_treatment.clinic = aClinic 
            except:
                LOG.warning("validatePutArgs: invalid clinic {}".format(data["clinic"]))
                valid = False

            try:
                if "patient" in data:
                    aPatient = Patient.objects.get(id=int(data["patient"]))
                    dental_treatment.patient = aPatient
            except:
                LOG.warning("validatePutArgs: invalid patient {}".format(data["patient"]))
                valid = False

        return valid, dental_treatment

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
            LOG.warning("post: Failed to validate!!")
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
                dental_treatment = DentalTreatment(**kwargs)
                if dental_treatment:
                    dental_treatment.save()
                else:
                    LOG.warning("post: unable to create DentalTreatment object!!")
                    badRequest = True
            except Exception as e:
                badRequest = True
                LOG.warning("post: exception!! {}".format(traceback.format_exc()))
                implMsg = sys.exc_info()[0] 

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': dental_treatment.id})

    @log_request
    def put(self, request, dental_treatment_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not dental_treatment_id:
            LOG.warning("put: missing ID arg")
            badRequest = True

        if not badRequest:
            dental_treatment = None

            try:
                LOG.warning("DentalTreatment put id is {}".format(dental_treatment_id))
                dental_treatment = DentalTreatment.objects.get(id=dental_treatment_id)
            except:
                LOG.warning("DentalTreatment put exception!!")

            if not dental_treatment:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, dental_treatment = self.validatePutArgs(data, dental_treatment)
                    if valid: 
                        dental_treatment.save()
                    else:
                        LOG.warning("put: validate put args failed")
                        badRequest = True
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
                    LOG.warning("DentalTreatment exception {}".format(implMsg))
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({})

    @log_request 
    def delete(self, request, dental_treatment_id=None, format=None):
        dental_treatment = None

        # see if the object exists

        if not dental_treatment_id:
            return HttpResponseBadRequest()
        try:
            dental_treatment = DentalTreatment.objects.get(id=dental_treatment_id)
        except:
            dental_treatment = None

        if not dental_treatment:
            raise NotFound
        else:
            dental_treatment.delete()

        return Response({})

#(C) Copyright Syd Logan 2019-2020
#(C) Copyright Thousand Smiles Foundation 2019-2020
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
from enthistory.models import *
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

class ENTTreatmentView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    sideFields = [
        "earCleanedSide",
        "audiogramSide",
  	"tympanogramSide",
  	"mastoidDebridedSide",
  	"boricAcidSide",
  	"foreignBodyRemoved",
  	"tubesTomorrow",
  	"tPlastyTomorrow",
  	"euaTomorrow",
  	"fbRemovalTomorrow",
  	"middleEarExploreMyringotomyTomorrow",
  	"cerumenTomorrow",
  	"granulomaTomorrow",
  	"tubesFuture",
  	"tPlastyFuture",
  	"euaFuture",
  	"fbRemovalFuture",
  	"middleEarExploreMyringotomyFuture",
  	"cerumenFuture",
  	"granulomaFuture"]

    booleanFields = [
  	"audiogramRightAway",
  	"tympanogramRightAway",
  	"mastoidDebridedHearingAidEval",
  	"antibioticDrops",
  	"antibioticOrally",
  	"antibioticAcuteInfection",
  	"antibioticAfterWaterExposureInfectionPrevention",
  	"boricAcidToday",
  	"boricAcidForHomeUse",
  	"return3Months",
  	"return6Months",
  	"returnPrn",
  	"referredPvtENTEnsenada",
  	"referredChildrensHospitalTJ",
  	"septorhinoplastyTomorrow",
  	"scarRevisionCleftLipTomorrow",
  	"frenulectomyTomorrow",
  	"septorhinoplastyFuture",
  	"scarRevisionCleftLipFuture",
  	"frenulectomyFuture"]

    textFields = [
        "username",
        "earCleanedComment",
  	"audiogramComment",
  	"audiogramRightAwayComment",
  	"tympanogramComment",
  	"tympanogramRightAwayComment",
  	"mastoidDebridedComment",
  	"mastoidDebridedHearingAidEvalComment",
  	"antibioticDropsComment",
  	"antibioticOrallyComment",
  	"antibioticAcuteInfectionComment",
  	"antibioticAfterWaterExposureInfectionPreventionComment",
  	"boricAcidTodayComment",
  	"boricAcidForHomeUseComment",
  	"boricAcidSideComment",
  	"foreignBodyRemovedComment",
  	"returnComment",
  	"referredPvtENTEnsenadaComment",
  	"referredChildrensHospitalTJComment",
  	"tubesTomorrowComment",
  	"tPlastyTomorrowComment",
  	"euaTomorrowComment",
  	"fbRemovalTomorrowComment",
  	"middleEarExploreMyringotomyTomorrowComment",
  	"cerumenTomorrowComment",
  	"granulomaTomorrowComment",
  	"septorhinoplastyTomorrowComment",
  	"scarRevisionCleftLipTomorrowComment",
  	"frenulectomyTomorrowComment",
  	"tubesFutureComment",
  	"tPlastyFutureComment",
  	"euaFutureComment",
  	"fbRemovalFutureComment",
  	"middleEarExploreMyringotomyFutureComment",
  	"cerumenFutureComment",
  	"granulomaFutureComment",
  	"septorhinoplastyFutureComment",
  	"scarRevisionCleftLipFutureComment",
  	"frenulectomyFutureComment",
  	"comment"]

    def sideToString(self, val):
        ret = None 
        for x in ENTHistory.EAR_SIDE_CHOICES:
            if x[0] == val:
                ret = x[1]
                break
        return ret    

    def stringToSide(self, val):
        ret = None 
        for x in ENTHistory.EAR_SIDE_CHOICES:
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
        m["earCleanedSide"] = self.sideToString(entry.earCleanedSide)
        m["earCleanedComment"] = entry.earCleanedComment
        m["audiogramSide"] = self.sideToString(entry.audiogramSide)
  	m["audiogramComment"] = entry.audiogramComment
  	m["audiogramRightAway"] = self.booleanToString(entry.audiogramRightAway)
  	m["audiogramRightAwayComment"] = entry.audiogramRightAwayComment
  	m["tympanogramSide"] = self.sideToString(entry.tympanogramSide)
  	m["tympanogramComment"] = entry.tympanogramComment
  	m["tympanogramRightAway"] = self.booleanToString(entry.tympanogramRightAway)
  	m["tympanogramRightAwayComment"] = entry.tympanogramRightAwayComment
  	m["mastoidDebridedSide"] = self.sideToString(entry.mastoidDebridedSide)
  	m["mastoidDebridedComment"] = entry.mastoidDebridedComment
  	m["mastoidDebridedHearingAidEval"] = self.booleanToString(entry.mastoidDebridedHearingAidEval)
  	m["mastoidDebridedHearingAidEvalComment"] = entry.mastoidDebridedHearingAidEvalComment
  	m["antibioticDrops"] = self.booleanToString(entry.antibioticDrops)
  	m["antibioticDropsComment"] = entry.antibioticDropsComment
  	m["antibioticOrally"] = self.booleanToString(entry.antibioticOrally)
  	m["antibioticOrallyComment"] = entry.antibioticOrallyComment
  	m["antibioticAcuteInfection"] = self.booleanToString(entry.antibioticAcuteInfection)
  	m["antibioticAcuteInfectionComment"] = entry.antibioticAcuteInfectionComment
  	m["antibioticAfterWaterExposureInfectionPrevention"] = self.booleanToString(entry.antibioticAfterWaterExposureInfectionPrevention)
  	m["antibioticAfterWaterExposureInfectionPreventionComment"] = entry.antibioticAfterWaterExposureInfectionPreventionComment
  	m["boricAcidToday"] = self.booleanToString(entry.boricAcidToday)
  	m["boricAcidTodayComment"] = entry.boricAcidTodayComment
  	m["boricAcidForHomeUse"] = self.booleanToString(entry.boricAcidForHomeUse)
  	m["boricAcidForHomeUseComment"] = entry.boricAcidForHomeUseComment
  	m["boricAcidSide"] = self.sideToString(entry.boricAcidSide)
  	m["boricAcidSideComment"] = entry.boricAcidSideComment
  	m["foreignBodyRemoved"] = self.sideToString(entry.foreignBodyRemoved)
  	m["foreignBodyRemovedComment"] = entry.foreignBodyRemovedComment
  	m["return3Months"] = self.booleanToString(entry.return3Months)
  	m["return6Months"] = self.booleanToString(entry.return6Months)
  	m["returnPrn"] = self.booleanToString(entry.returnPrn)
  	m["returnComment"] = entry.returnComment
  	m["referredPvtENTEnsenada"] = self.booleanToString(entry.referredPvtENTEnsenada)
  	m["referredPvtENTEnsenadaComment"] = entry.referredPvtENTEnsenadaComment
  	m["referredChildrensHospitalTJ"] = self.booleanToString(entry.referredChildrensHospitalTJ)
  	m["referredChildrensHospitalTJComment"] = entry.referredChildrensHospitalTJComment
  	m["tubesTomorrow"] = self.sideToString(entry.tubesTomorrow)
  	m["tubesTomorrowComment"] = entry.tubesTomorrowComment
  	m["tPlastyTomorrow"] = self.sideToString(entry.tPlastyTomorrow)
  	m["tPlastyTomorrowComment"] = entry.tPlastyTomorrowComment
  	m["euaTomorrow"] = self.sideToString(entry.euaTomorrow)
  	m["euaTomorrowComment"] = entry.euaTomorrowComment
  	m["fbRemovalTomorrow"] = self.sideToString(entry.fbRemovalTomorrow)
  	m["fbRemovalTomorrowComment"] = entry.fbRemovalTomorrowComment
  	m["middleEarExploreMyringotomyTomorrow"] = self.sideToString(entry.middleEarExploreMyringotomyTomorrow)
  	m["middleEarExploreMyringotomyTomorrowComment"] = entry.middleEarExploreMyringotomyTomorrowComment
  	m["cerumenTomorrow"] = self.sideToString(entry.cerumenTomorrow)
  	m["cerumenTomorrowComment"] = entry.cerumenTomorrowComment
  	m["granulomaTomorrow"] = self.sideToString(entry.granulomaTomorrow)
  	m["granulomaTomorrowComment"] = entry.granulomaTomorrowComment
  	m["septorhinoplastyTomorrow"] = self.booleanToString(entry.septorhinoplastyTomorrow)
  	m["septorhinoplastyTomorrowComment"] = entry.septorhinoplastyTomorrowComment
  	m["scarRevisionCleftLipTomorrow"] = self.booleanToString(entry.scarRevisionCleftLipTomorrow)
  	m["scarRevisionCleftLipTomorrowComment"] = entry.scarRevisionCleftLipTomorrowComment
  	m["frenulectomyTomorrow"] = self.booleanToString(entry.frenulectomyTomorrow)
  	m["frenulectomyTomorrowComment"] = entry.frenulectomyTomorrowComment

  	m["tubesFuture"] = self.sideToString(entry.tubesFuture)
  	m["tubesFutureComment"] = entry.tubesFutureComment
  	m["tPlastyFuture"] = self.sideToString(entry.tPlastyFuture)
  	m["tPlastyFutureComment"] = entry.tPlastyFutureComment
  	m["euaFuture"] = self.sideToString(entry.euaFuture)
  	m["euaFutureComment"] = entry.euaFutureComment
  	m["fbRemovalFuture"] = self.sideToString(entry.fbRemovalFuture)
  	m["fbRemovalFutureComment"] = entry.fbRemovalFutureComment
  	m["middleEarExploreMyringotomyFuture"] = self.sideToString(entry.middleEarExploreMyringotomyFuture)
  	m["middleEarExploreMyringotomyFutureComment"] = entry.middleEarExploreMyringotomyFutureComment
  	m["cerumenFuture"] = self.sideToString(entry.cerumenFuture)
  	m["cerumenFutureComment"] = entry.cerumenFutureComment
  	m["granulomaFuture"] = self.sideToString(entry.granulomaFuture)
  	m["granulomaFutureComment"] = entry.granulomaFutureComment
  	m["septorhinoplastyFuture"] = self.booleanToString(entry.septorhinoplastyFuture)
  	m["septorhinoplastyFutureComment"] = entry.septorhinoplastyFutureComment
  	m["scarRevisionCleftLipFuture"] = self.booleanToString(entry.scarRevisionCleftLipFuture)
  	m["scarRevisionCleftLipFutureComment"] = entry.scarRevisionCleftLipFutureComment
  	m["frenulectomyFuture"] = self.booleanToString(entry.frenulectomyFuture)
  	m["frenulectomyFutureComment"] = entry.frenulectomyFutureComment
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

            for x in self.sideFields:
                try:
                    val = request.GET.get(x, '')
                    if val != '':
                        val = self.stringToSide(val)
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
        kwargs = {}
        kwargs = data

        for k, v in data.items():
            if not k in self.sideFields and not k in self.booleanFields and not k in self.textFields and k != "patient" and k != "clinic":
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

        for x in self.sideFields:
            try: 
                val = self.stringToSide(data[x])
                if val == None:
                    LOG.warning("validatePostArgs: Failed to validate key x {} val {}".format(x, data[x]))
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                LOG.warning("validatePostArgs: Failed to locate key {}".format(x))
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

    def validatePutArgs(self, data, ent_treatment):
        valid = True
        found = False

        # first check to see if we have at least one item, and what
        # we have is paired with a valid value

        for k, v in data.items():
            LOG.warning("validatePutArgs: top loop k {} v {}".format(k, v))
            if k in self.sideFields:
                found = True
                try:
                    z = self.stringToSide(v)
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

        # now, build up the ent treatment object

        if found == True and valid == True:
            for k, v in data.items():
                LOG.warning("validatePutArgs: bottom loop k {} v {}".format(k, v))
                if k == "earCleanedSide":
                    ent_treatment.earCleanedSide = self.stringToSide(v)
                elif k == "audiogramSide":
                    ent_treatment.audiogramSide = self.stringToSide(v)
  	        elif k == "tympanogramSide":
                    ent_treatment.tympanogramSide = self.stringToSide(v)
  	        elif k == "mastoidDebridedSide":
                    ent_treatment.mastoidDebridedSide = self.stringToSide(v)
  	        elif k == "boricAcidSide":
                    ent_treatment.boricAcidSide = self.stringToSide(v)
  	        elif k == "foreignBodyRemoved":
                    ent_treatment.foreignBodyRemoved = self.stringToSide(v)
  	        elif k == "tubesTomorrow":
                    ent_treatment.tubesTomorrow = self.stringToSide(v)
  	        elif k == "tPlastyTomorrow":
                    ent_treatment.tPlastyTomorrow = self.stringToSide(v)
  	        elif k == "euaTomorrow":
                    ent_treatment.euaTomorrow = self.stringToSide(v)
  	        elif k == "fbRemovalTomorrow":
                    ent_treatment.fbRemovalTomorrow = self.stringToSide(v)
  	        elif k == "middleEarExploreMyringotomyTomorrow":
                    ent_treatment.middleEarExploreMyringotomyTomorrow = self.stringToSide(v)
  	        elif k == "cerumenTomorrow":
                    ent_treatment.cerumenTomorrow = self.stringToSide(v)
  	        elif k == "granulomaTomorrow":
                    ent_treatment.granulomaTomorrow = self.stringToSide(v)
  	        elif k == "tubesFuture":
                    ent_treatment.tubesFuture = self.stringToSide(v)
  	        elif k == "tPlastyFuture":
                    ent_treatment.tPlastyFuture = self.stringToSide(v)
  	        elif k == "euaFuture":
                    ent_treatment.euaFuture = self.stringToSide(v)
  	        elif k == "fbRemovalFuture":
                    ent_treatment.fbRemovalFuture = self.stringToSide(v)
  	        elif k == "middleEarExploreMyringotomyFuture":
                    ent_treatment.middleEarExploreMyringotomyFuture = self.stringToSide(v)
  	        elif k == "cerumenFuture":
                    ent_treatment.cerumenFuture = self.stringToSide(v)
  	        elif k == "granulomaFuture":
                    ent_treatment.granulomaFuture = self.stringToSide(v)

  	        elif k == "audiogramRightAway":
                    ent_treatment.audiogramRightAway = self.stringToBoolean(v)
  	        elif k == "tympanogramRightAway":
                    ent_treatment.tympanogramRightAway = self.stringToBoolean(v)
  	        elif k == "mastoidDebridedHearingAidEval":
                    ent_treatment.mastoidDebridedHearingAidEval = self.stringToBoolean(v)
  	        elif k == "antibioticDrops":
                    ent_treatment.antibioticDrops = self.stringToBoolean(v)
  	        elif k == "antibioticOrally":
                    ent_treatment.antibioticOrally = self.stringToBoolean(v)
  	        elif k == "antibioticAcuteInfection":
                    ent_treatment.antibioticAcuteInfection = self.stringToBoolean(v)
  	        elif k == "antibioticAfterWaterExposureInfectionPrevention":
                    ent_treatment.antibioticAfterWaterExposureInfectionPrevention = self.stringToBoolean(v)
  	        elif k == "boricAcidToday":
                    ent_treatment.boricAcidToday = self.stringToBoolean(v)
  	        elif k == "boricAcidForHomeUse":
                    ent_treatment.boricAcidForHomeUse = self.stringToBoolean(v)
  	        elif k == "return3Months":
                    ent_treatment.return3Months = self.stringToBoolean(v)
  	        elif k == "return6Months":
                    ent_treatment.return6Months = self.stringToBoolean(v)
  	        elif k == "returnPrn":
                    ent_treatment.returnPrn = self.stringToBoolean(v)
  	        elif k == "referredPvtENTEnsenada":
                    ent_treatment.referredPvtENTEnsenada = self.stringToBoolean(v)
  	        elif k == "referredChildrensHospitalTJ":
                    ent_treatment.referredChildrensHospitalTJ = self.stringToBoolean(v)
  	        elif k == "septorhinoplastyTomorrow":
                    ent_treatment.septorhinoplastyTomorrow = self.stringToBoolean(v)
  	        elif k == "scarRevisionCleftLipTomorrow":
                    ent_treatment.scarRevisionCleftLipTomorrow = self.stringToBoolean(v)
  	        elif k == "frenulectomyTomorrow":
                    ent_treatment.frenulectomyTomorrow = self.stringToBoolean(v)
  	        elif k == "septorhinoplastyFuture":
                    ent_treatment.septorhinoplastyFuture = self.stringToBoolean(v)
  	        elif k == "scarRevisionCleftLipFuture":
                    ent_treatment.scarRevisionCleftLipFuture = self.stringToBoolean(v)
  	        elif k == "frenulectomyFuture":
                    ent_treatment.frenulectomyFuture = self.stringToBoolean(v)

                elif k == "username":
                    ent_treatment.username = str(v)
                elif k == "earCleanedComment":
                    ent_treatment.earCleanedComment = str(v)
  	        elif k == "audiogramComment":
                    ent_treatment.audiogramComment = str(v)
  	        elif k == "tympanogramComment":
                    ent_treatment.tympanogramComment = str(v)
  	        elif k == "tympanogramRightAwayComment":
                    ent_treatment.tympanogramRightAwayComment = str(v)
  	        elif k == "mastoidDebridedComment":
                    ent_treatment.mastoidDebridedComment = str(v)
  	        elif k == "mastoidDebridedHearingAidEvalComment":
                    ent_treatment.mastoidDebridedHearingAidEvalComment = str(v)
  	        elif k == "antibioticDropsComment":
                    ent_treatment.antibioticDropsComment = str(v)
  	        elif k == "antibioticOrallyComment":
                    ent_treatment.antibioticOrallyComment = str(v)
  	        elif k == "antibioticAcuteInfectionComment":
                    ent_treatment.antibioticAcuteInfectionComment = str(v)
  	        elif k == "antibioticAfterWaterExposureInfectionPreventionComment":
                    ent_treatment.antibioticAfterWaterExposureInfectionPreventionComment = str(v)
  	        elif k == "boricAcidTodayComment":
                    ent_treatment.boricAcidTodayComment = str(v)
  	        elif k == "boricAcidForHomeUseComment":
                    ent_treatment.boricAcidForHomeUseComment = str(v)
  	        elif k == "boricAcidSideComment":
                    ent_treatment.boricAcidSideComment = str(v)
  	        elif k == "foreignBodyRemovedComment":
                    ent_treatment.foreignBodyRemovedComment = str(v)
  	        elif k == "returnComment":
                    ent_treatment.returnComment = str(v)
  	        elif k == "referredPvtENTEnsenadaComment":
                    ent_treatment.referredPvtENTEnsenadaComment = str(v)
  	        elif k == "referredChildrensHospitalTJComment":
                    ent_treatment.referredChildrensHospitalTJComment = str(v)
  	        elif k == "tubesTomorrowComment":
                    ent_treatment.tubesTomorrowComment = str(v)
  	        elif k == "tPlastyTomorrowComment":
                    ent_treatment.tPlastyTomorrowComment = str(v)
  	        elif k == "euaTomorrowComment":
                    ent_treatment.euaTomorrowComment = str(v)
  	        elif k == "fbRemovalTomorrowComment":
                    ent_treatment.fbRemovalTomorrowComment = str(v)
  	        elif k == "middleEarExploreMyringotomyTomorrowComment":
                    ent_treatment.middleEarExploreMyringotomyTomorrowComment = str(v)
  	        elif k == "cerumenTomorrowComment":
                    ent_treatment.cerumenTomorrowComment = str(v)
  	        elif k == "granulomaTomorrowComment":
                    ent_treatment.granulomaTomorrowComment = str(v)
  	        elif k == "septorhinoplastyTomorrowComment":
                    ent_treatment.septorhinoplastyTomorrowComment = str(v)
  	        elif k == "scarRevisionCleftLipTomorrowComment":
                    ent_treatment.scarRevisionCleftLipTomorrowComment = str(v)
  	        elif k == "frenulectomyTomorrowComment":
                    ent_treatment.frenulectomyTomorrowComment = str(v)
  	        elif k == "tubesFutureComment":
                    ent_treatment.tubesFutureComment = str(v)
  	        elif k == "tPlastyFutureComment":
                    ent_treatment.tPlastyFutureComment = str(v)
  	        elif k == "euaFutureComment":
                    ent_treatment.euaFutureComment = str(v)
  	        elif k == "fbRemovalFutureComment":
                    ent_treatment.fbRemovalFutureComment = str(v)
  	        elif k == "middleEarExploreMyringotomyFutureComment":
                    ent_treatment.middleEarExploreMyringotomyFutureComment = str(v)
  	        elif k == "cerumenFutureComment":
                    ent_treatment.cerumenFutureComment = str(v)
  	        elif k == "granulomaFutureComment":
                    ent_treatment.granulomaFutureComment = str(v)
  	        elif k == "septorhinoplastyFutureComment":
                    ent_treatment.septorhinoplastyFutureComment = str(v)
  	        elif k == "scarRevisionCleftLipFutureComment":
                    ent_treatment.scarRevisionCleftLipFutureComment = str(v)
  	        elif k == "frenulectomyFutureComment":
                    ent_treatment.frenulectomyFutureComment = str(v)
  	        elif k == "comment":
                    ent_treatment.comment = str(v)

            #ent_treatment = namedtuple("Treatment", data.keys())(*data.values())
            try:
                if "clinic" in data:
                    aClinic = Clinic.objects.get(id=int(data["clinic"]))
                    ent_treatment.clinic = aClinic 
            except:
                LOG.warning("validatePutArgs: invalid clinic {}".format(data["clinic"]))
                valid = False

            try:
                if "patient" in data:
                    aPatient = Patient.objects.get(id=int(data["patient"]))
                    ent_treatment.patient = aPatient
            except:
                LOG.warning("validatePutArgs: invalid patient {}".format(data["patient"]))
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
                ent_treatment = ENTTreatment(**kwargs)
                if ent_treatment:
                    ent_treatment.save()
                else:
                    LOG.warning("post: unable to create ENTTreatment object!!")
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
            return Response({'id': ent_treatment.id})

    @log_request
    def put(self, request, ent_treatment_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_treatment_id:
            LOG.warning("put: missing ID arg")
            badRequest = True

        if not badRequest:
            ent_treatment = None

            try:
                LOG.warning("ENTTreatment put id is {}".format(ent_treatment_id))
                ent_treatment = ENTTreatment.objects.get(id=ent_treatment_id)
            except:
                LOG.warning("ENTTreatment put exception!!")

            if not ent_treatment:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, ent_treatment = self.validatePutArgs(data, ent_treatment)
                    if valid: 
                        ent_treatment.save()
                    else:
                        LOG.warning("put: validate put args failed")
                        badRequest = True
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
                    LOG.warning("ENTTreatment exception {}".format(implMsg))
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

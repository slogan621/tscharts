# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from surgeryhistory.models import *
from surgerytype.models import *
from patient.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import sys
import numbers
import json 
from datetime import datetime 


class SurgeryHistoryView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["patient"] = entry.patient_id
        m["surgery"] = entry.surgery_id
        m["surgeryyear"] = entry.surgeryyear
        m["surgerymonth"] = entry.surgerymonth
        m["surgerylocation"] = entry.surgerylocation
        m["anesthesia_problems"] = entry.anesthesia_problems
        m["bleeding_problems"] = entry.bleeding_problems

        return m

    def get(self, request, surgery_history_id = None, format = None):
        surgery_history = None
        badRequest = False
        aPatient = None
        aSurgery = None
        kwargs = {}

        if surgery_history_id:
            try:
                surgery_history = SurgeryHistory.objects.get(id = surgery_history_id)
            except:
                surgery_history = None
        else:
            try:
                patientid = request.GET.get('patient','')
                if patientid != '':
                    try:
                        aPatient = Patient.objects.get(id = patientid)
                        if not aPatient:
                            badRequest = True
                        else:
                            kwargs["patient"] = aPatient
                    except:
                        badRequest = True
            except:
                pass #no patient ID

            try:
                surgeryid = request.GET.get('surgery','')
                if surgeryid != '':
                    try:
                        aSurgery = SurgeryType.objects.get(id=surgeryid)
                        if not aSurgery:
                            badRequest = True
                        else:
                            kwargs["surgery"] = aSurgery
                    except:
                        badRequest = True
            except:
                pass #no surgery ID
            if not badRequest and len(kwargs):
                case1 = False
                case2 = False
                case3 = False

                if aPatient and aSurgery:
                    case1 = True
                elif aPatient and not aSurgery:
                    case2 = True
                elif aSurgery and not aPatient:
                    case3 = True
                else:
                    badRequest = True

          
            if not badRequest:
                kwargs = {}
                if case1:
                    kwargs["patient"] = aPatient
                    kwargs["surgery"] = aSurgery
                if case2:
                    kwargs["patient"] = aPatient
                if case3:
                    kwargs["surgery"] = aSurgery
                try:
                    surgery_history = SurgeryHistory.objects.filter(**kwargs)
                except:
                    surgery_history = None
        if not surgery_history and not badRequest:
            raise NotFound
        elif not badRequest:
            if surgery_history_id:
                ret = self.serialize(surgery_history)
            else:
                ret = []
                for x in surgery_history:
                    y = self.serialize(x)
                    ret.append(y)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)
 
    def validatePostArgs(self, data, aPatient):
        valid = True
        kwargs = data
        
        patient_birth_year = int(str(aPatient.dob)[0:4])
        now = datetime.now()
        current_year = int(now.year)

        try:
            val = int(data["surgeryyear"])
            if val < patient_birth_year or val > current_year:
                valid = False
            else:
                kwargs["surgeryyear"] = val
            val = int(data["surgerymonth"])
            if val < 1 or val > 12:
                valid = False
            else:
                kwargs["surgerymonth"] = val
            val = data["surgerylocation"]
            if len(val) == 0:
                valid = False
            val = data["anesthesia_problems"]
            if not (val == True or val == False):
                valid = False
            val = data["bleeding_problems"]
            if not (val == True or val == False):
                valid = False
            
            for key in data:
                if key not in ["surgery","patient","surgeryyear","surgerymonth","surgerylocation","anesthesia_problems","bleeding_problems"]:
                    valid = False
    
        except:
            valid = False
        return valid, kwargs
 
    def validatePutArgs(self, data, surgery_history, aPatient):
        valid = True

        patient_birth_year = int(str(aPatient.dob)[0:4])
        now = datetime.now()
        current_year = int(now.year)

        try:
            if "surgery" in data:
                val = data["surgery"]
                try:
                    aSurgery = SurgeryType.objects.get(id = val)
                except:
                    valid = False
                surgery_history.surgery = aSurgery

            if "surgeryyear" in data:
                val = int(data["surgeryyear"])
                if val < patient_birth_year or val > current_year:
                    valid = False
                else:
                    surgery_history.surgeryyear = val

            if "surgerymonth" in data:
                val = int(data["surgerymonth"])
                if val < 1 or val > 12:
                    valid = False
                else:
                    surgery_history.surgerymonth = val

            if "surgerylocation" in data:
                val = data["surgerylocation"]
                if len(val) == 0:
                    valid = False
                else:
                    surgery_history.surgerylocation = val

            if "anesthesia_problems" in data:
                val = data["anesthesia_problems"]
                if not (val == True or val == False):
                    valid = False
                else:
                    surgery_history.anesthesia_problems = val

            if "bleeding_problems" in data:
                val = data["bleeding_problems"]
                if not (val == True or val == False):
                    valid = False
                else:
                    surgery_history.bleeding_problems = val
            for key in data:
                if key not in ["surgery", "surgeryyear","surgerymonth","surgerylocation","anesthesia_problems","bleeding_problems"]:
                    valid = False
        except:
            valid = False

        return valid, surgery_history
                
                
    def post(self, request, format = None):  
        badRequest = False
        implError = False
        
        data = json.loads(request.body)
        try:
            patientid = int(data["patient"])
        except:
            badRequest = True

        try:
            surgeryid = int(data["surgery"])
        except:
            badRequest = True

        if not badRequest:
            try:
                aPatient = Patient.objects.get(id = patientid)
            except:
                aPatient = None

            try:
                aSurgery = SurgeryType.objects.get(id = surgeryid)  
            except:
                aSurgery = None
            
            if not aSurgery or not aPatient:
                raise NotFound

        if not badRequest:
            valid, kwargs = self.validatePostArgs(data, aPatient)
            if not valid:
                badRequest = True
        if not badRequest:
        
            try:
                kwargs["patient"] = aPatient
                kwargs["surgery"] = aSurgery
                surgery_history = SurgeryHistory(**kwargs)
                if surgery_history:
                    surgery_history.save()
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
            return Response({'id': surgery_history.id})


    def put(self, request, surgery_history_id = None, format = None):
        badRequest = False
        implError = False
        notFound = False

        if not surgery_history_id:
            badRequest = True

        if not badRequest:
            surgery_history = None

            try:
                surgery_history = SurgeryHistory.objects.get(id = surgery_history_id)
                aPatient = surgery_history.patient
            except:
                pass

            if not surgery_history:
                notFound = True
            else:
                try:
                    data = json.loads(request.body)
                    valid, surgery_history = self.validatePutArgs(data, surgery_history, aPatient)
                    if valid:
                        surgery_history.save()
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

    def delete(self, request, surgery_history_id=None, format=None):
        surgery_history = None


        if not surgery_history_id:
            return HttpResponseBadRequest()
        try:
            surgery_history = SurgeryHistory.objects.get(id=surgery_history_id)
        except:
            surgery_history = None

        if not surgery_history:
            raise NotFound
        else:
            surgery_history.delete()

        return Response({})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from consent.models import *
from register.models import *
from clinic.models import *
from patient.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import sys
import numbers
import json 


class ConsentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["registration"] = entry.registration_id
        m["patient"] = entry.patient_id
        m["clinic"] = entry.clinic_id
        m["general_consent"] = entry.general_consent
        m["photo_consent"] = entry.photo_consent
        return m
    
    def get(self, request = None, consent_id = None, format = None):
        consent = None
        badRequest = False
        aRegistration = None
        aPatient = None
        aClinic = None
        kwargs = {}
        #consent id only returns a single consent item        
        if consent_id:
            try:
                consent = Consent.objects.get(id = consent_id)
            except:
                raise NotFound
            if not badRequest:
                ret = self.serialize(consent)

        else:
            try:
                registrationid = request.GET.get('registration','')
                if registrationid != '':
                    try:
                        aRegistration = Register.objects.get(id = registrationid)
                        if not aRegistration:
                            badRequest = True
                        else:
                            kwargs["registration"] = aRegistration
                    except:
                        badRequest = True
            except:
                pass #no registration ID

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
                clinicid = request.GET.get('clinic','')
                if clinicid != '':
                    try:
                        aClinic = Clinic.objects.get(id = clinicid)
                        if not aClinic:
                            badRequest = True
                        else:
                            kwargs["clinic"] = aClinic
                    except:
                        badRequest = True
            except:
                pass #no clinic ID

            
            if not badRequest and len(kwargs):
                aList = list(kwargs.keys())
                if len(aList) == 1:
                    if aList[0] == 'patient' or aList[0] == 'clinic':
                        consent = Consent.objects.filter(**kwargs)
                            
                        ret = []
                        for x in consent:
                            y = self.serialize(x)
                            ret.append(y)
                        if ret == []:
                            raise NotFound
                    #only one consent exists
                    elif aList[0] == 'registration':
                        try:
                            consent = Consent.objects.get(**kwargs)
                        except:
                            raise NotFound
                        ret = []
                        y = self.serialize(consent)
                        ret.append(y)
                else:
                    try:
                        consent = Consent.objects.get(**kwargs)
                    except:
                        raise NotFound
                    ret = []
                    y = self.serialize(consent)
                    ret.append(y) 
            

        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)
    
    def validatePostArgs(self, data):
        valid = True
        kwargs = data
        
        try:
            val = data["general_consent"]
            if not (val == True or val == False):
                valid = False
            val = data["photo_consent"]
            if not (val == True or val == False):
                valid = False
            
            for key in data:
                if key not in ["registration", "clinic", "patient", "general_consent", "photo_consent"]:
                    valid = False
        except:
            valid = False
        
        return valid, kwargs    

    def post(self, request, format = None):  
        badRequest = False
        implError = False
        
        data = json.loads(request.body)
        try:
            registrationid = int(data["registration"])
        except:
            badRequest = True
        
        try:
            clinicid = int(data["clinic"])
        except:
            badRequest = True

        try:
            patientid = int(data["patient"])
        except:
            badRequest = True
            
        if not badRequest:
            try:
                aRegistration = Register.objects.get(id = registrationid)
            except:
                aRegistration = None

        if not badRequest:
            try:
                aClinic = Clinic.objects.get(id = clinicid)
            except:
                aClinic = None

        if not badRequest:
            try:
                aPatient = Patient.objects.get(id = patientid)
            except:
                aPatient = None

        if not badRequest:
            valid, kwargs = self.validatePostArgs(data)
            if not valid:
                badRequest = True
        if not badRequest:
            if not aRegistration or not aClinic or not aPatient:
                badRequest = True
            else:
                kwargs["registration"] = aRegistration
                kwargs["clinic"] = aClinic
                kwargs["patient"] = aPatient
        if not badRequest:
            if aRegistration.clinic != aClinic or aRegistration.patient != aPatient:
                badRequest = True
        
        if not badRequest:
            try:
                if Consent.objects.all().filter(registration = aRegistration, clinic = aClinic, patient = aPatient).exists():
                    badRequest = True
            except:
                implMsg = "Consent.objects.all().filter {} {}".format(sys.exc_info()[0], data)
                implError = True
            

        if not badRequest:
            try:
                consent = Consent(**kwargs)
                if consent:
                    consent.save()
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
            return Response({'id': consent.id}) 

    def delete(self, request, consent_id=None, format=None):
        consent = None


        if not consent_id:
            return HttpResponseBadRequest()
        try:
            consent = Consent.objects.get(id=consent_id)
        except:
            consent = None

        if not consent:
            raise NotFound
        else:
            consent.delete()

        return Response({})   


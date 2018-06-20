# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
        m["register"] = entry.register_id
        m["general_consent"] = entry.general_consent
        m["photo_consent"] = entry.photo_consent
        return m
    '''
    def get(self, request, consent_id = None, format = None):
        consent = None
        badRequest = False
        aRegistration = None
        kwargs = {}
        
        if consent_id:
            try:
                consent = Consent.objects.get(id = consent_id)
            except:
                consent = None
        else:
            try:
                registrationid = request.GET.get('register','')
                if registrationid != '':
                    try:
                        aRegistration = Register.objects.get(id = registrationid)
                        if not aRegistration:
                            badRequest = True
                        else:
                            kwargs["register"] = aRegistration
                    except:
                        badRequest = True
            except:
                pass #no registration ID
            
            if not badRequest and len(kwargs):
                try:
                    consent = Consent.objects.filter(**kwargs)
                except:
                    consent = None
        
        if not consent and not badRequest:
            raise NotFound
        elif not badRequest:
            ret = self.serialize(consent)

        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)
    '''
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
                if key not in ["register", "general_consent", "photo_consent"]:
                    valid = False
        except:
            valid = False
        return valid, kwargs    

    def post(self, request, format = None):
        
        badRequest = False
        
        print("kkk")
        implError = False
        
 
        data = json.loads(request.body)
        try:
            registrationid = int(data["register"])
        except:
            badRequest = True

        if not badRequest:
            try:
                aRegistration = Register.objects.get(id = registrationid)
            except:
                raise NotFound
        
        if not badRequest:
            valid, kwargs = self.validatePostArgs(data)
            if not valid:
                badRequest = True
        if not badRequest:
            try:
                kwargs["register"] = aRegistration
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

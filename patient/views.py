#(C) Copyright Syd Logan 2016-2019
#(C) Copyright Thousand Smiles Foundation 2016-2019
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

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from patient.models import *
from clinic.models import *
from routingslip.models import *
from datetime import *
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import json
import sys

class PatientView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def toState(self, statecode):
        ret = None
        for x in Patient.STATE_CHOICES:
            if x[0] == statecode:
                ret = x[1]
        return ret 

    def serialize(self, entry):
        m = {}

        m["id"] = entry.id
        m["paternal_last"] = entry.paternal_last
        m["maternal_last"] = entry.maternal_last
        m["first"] = entry.first
        m["middle"] = entry.middle
        m["suffix"] = entry.suffix
        m["prefix"] = entry.prefix
        m["dob"] = entry.dob.strftime("%m/%d/%Y")
        if entry.gender == "f":
            m["gender"] = "Female"
        else:
            m["gender"] = "Male"
        m["street1"] = entry.street1
        m["street2"] = entry.street2
        m["city"] = entry.city
        m["colonia"] = entry.colonia
        m["state"] = self.toState(entry.state)
        m["phone1"] = entry.phone1
        m["phone2"] = entry.phone2
        m["email"] = entry.email
        m["emergencyfullname"] = entry.emergencyfullname
        m["emergencyphone"] = entry.emergencyphone
        m["emergencyemail"] = entry.emergencyemail
        m["curp"] = entry.curp
        m["oldid"] = entry.oldid

        return m

    @log_request
    def get(self, request, patient_id=None, format=None):

        badRequest = False
        notFound = False
        patient = None
        byClinicId = None
        aClinic = None
        
        if patient_id:
            try:
                patient = Patient.objects.get(id = patient_id)
            except:
                patient = None
        else:
            # look for optional arguments for searching
            byClinicId = request.GET.get("clinic", '')
            if byClinicId != '':
                aClinic = Clinic.objects.get(id=byClinicId)
                if not aClinic:
                    notFound = True

            if not notFound:
                kwargs = {}
                name = request.GET.get('name', '')
                if not name == '':
                    try:
                        patient = Patient.objects.filter(Q(paternal_last__icontains=name) | Q(maternal_last__icontains=name) | Q(first__icontains=name) | Q(middle__icontains=name))
                    except:
                        patient = None
                else:
                    paternal_last = request.GET.get('paternal_last', '')
                    if not paternal_last == '':
                        kwargs["paternal_last__icontains"] = paternal_last
                    maternal_last = request.GET.get('maternal_last', '')
                    if not maternal_last == '':
                        kwargs["maternal_last__icontains"] = maternal_last
                    first = request.GET.get('first', '')
                    if not first == '':
                        kwargs["first__icontains"] = first
                    dob = request.GET.get('dob', '')
                    if not dob == '':
                        x = dob.split("/")
                        if len(x) == 3:
                            try:
                                kwargs["dob"] = datetime.strptime(dob, "%m/%d/%Y")
                            except:
                                badRequest = True
                        else:
                            badRequest = True

                    curp = request.GET.get('curp', '')
                    if not curp == '':
                        kwargs["curp__icontains"] = curp
                    
                    oldid = request.GET.get('oldid', '')
                    if not oldid == '':
                        try:
                            kwargs["oldid"] = int(oldid)
                        except:
                            badRequest = True
                    
                    gender = request.GET.get('gender', '')
                    if not gender == '':
                        if gender == "Male":
                            kwargs["gender"] = "m"
                        elif gender == "Female":
                            kwargs["gender"] = "f"
                        else:
                            badRequest = True

                    if not badRequest:
                        try:
                            patient = Patient.objects.filter(**kwargs)
                        except:
                            patient = None

        if not patient and not badRequest:
            notFound = True
        elif patient:
            if patient_id:
                ret = self.serialize(patient)
            else: 
                ret = []
                for x in patient:
                    if aClinic != None:
                        routingSlip = RoutingSlip.objects.filter(patient=x.id, clinic=aClinic)
                        if routingSlip != None and len(routingSlip) > 0:
                            ret.append(x.id)
                    else:
                        ret.append(x.id)
                            
        if badRequest:
            return HttpResponseBadRequest()
        elif notFound:
            return HttpResponseNotFound()
        else:
            return Response(ret)

    def validateState(self, state):
        valid = False
        ret = None

        for val in Patient.STATE_CHOICES:
            if val[1] == state:
                valid = True
                ret = val[0]
                break
        return valid, ret 

    def validatePutArgs(self, data, patient):
        valid = True

        if "curp" in data: 
            patient.curp = data["curp"]
        if "oldid" in data: 
            patient.oldid = data["oldid"]
        if "paternal_last" in data: 
            patient.paternal_last = data["paternal_last"]
        if "maternal_last" in data:
            patient.maternal_last = data["maternal_last"]
        if "first" in data:
            patient.first = data["first"]
        if "middle" in data:
            patient.middle = data["middle"]
        if "suffix" in data:
            patient.suffix = data["suffix"]
        if "prefix" in data:
            patient.prefix = data["prefix"]
        if "dob" in data:
            dob = data["dob"]
            try: 
                dob = datetime.strptime(dob, "%m/%d/%Y")
                patient.dob = dob
            except:
                try: 
                    dob = datetime.strptime(dob, "%m-%d-%Y")
                    patient.dob = dob
                except:
                    valid = False
        if "gender" in data:
            gender = data["gender"]
            if gender != 'Female' and gender != 'Male':
                valid = False
            else:
                if gender == "Female":
                    gender = "f"
                else:
                    gender = "m"
                patient.gender = gender

        if "street1" in data:
            patient.street1 = data["street1"]
        if "street2" in data:
            patient.street2 = data["street2"]
        if "city" in data:
            patient.city = data["city"]
        if "colonia" in data:
            patient.colonia = data["colonia"]
        if "state" in data:
            validtmp, state = self.validateState(data["state"])
            if validtmp == True:
                patient.state = state
            else:
                valid = False
        if "phone1" in data:
            patient.phone1 = data["phone1"]
        if "phone2" in data:
            patient.phone2 = data["phone2"]
        if "email" in data:
            patient.email = data["email"]
        if "emergencyfullname" in data:
            patient.emergencyfullname = data["emergencyfullname"]
        if "emergencyphone" in data:
            patient.emergencyphone = data["emergencyphone"]
        if "emergencyemail" in data:
            patient.emergencyemail = data["emergencyemail"]

        return valid, patient

    @log_request
    def put(self, request, patient_id, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not patient_id:
            badRequest = True

        if not badRequest:
            patient = None

            try:
                patient = Patient.objects.get(id=patient_id)
            except:
                pass

            if not patient:
                notFound = True
            else:
                try:
                    data = json.loads(request.body)
                    valid, patient = self.validatePutArgs(data, patient)
                    if valid:
                        patient.save()
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

    def validatePostArgs(self, data):
        valid = True
        kwargs = data
        required = ["paternal_last",
                "maternal_last",
                "first",
                "middle",
                "suffix",
                "prefix",
                "dob",
                "gender",
                "street1",
                "street2",
                "city",
                "colonia",
                "state",
                "phone1",
                "phone2",
                "email",
                "emergencyfullname",
                "emergencyphone",
                "emergencyemail",
                "curp"]

        optional = ["oldid"]

        for key, val in data.iteritems():
            if not key in required and not key in optional:
                valid = False
                break

        for k in required:
            if not k in data:
                valid = False
                break

        if valid:
            try:
                validtmp, state = self.validateState(data["state"])
                if validtmp == True:
                    kwargs["state"] = state
                else:
                    valid = False
                try:
                    kwargs["dob"] = datetime.strptime(data["dob"], '%m/%d/%Y')
                except ValueError:
                    try:
                        kwargs["dob"] = datetime.strptime(data["dob"], '%m-%d-%Y')
                    except ValueError:
                        valid = False
                if data["gender"] in ["Male", "Female"]:
                    kwargs["gender"] = data["gender"][0].lower()
                else:
                    valid = False;
            except:
                valid = False

        return valid, kwargs
        
    @log_request
    def post(self, request, format=None):
        badRequest = False
        implError = False
        duplicatePatient = False

        data = json.loads(request.body)
        valid, kwargs = self.validatePostArgs(data)

        if not valid:
            badRequest = True

        if not badRequest:
            patient = None

            # see if the patient already exists, using core subset of data

            try:
                patient = Patient.objects.filter(paternal_last=kwargs["paternal_last"],
                                                 first=kwargs["first"],
                                                 dob=kwargs["dob"],
                                                 gender=kwargs["gender"])
                if patient and len(patient) > 0:
                    badRequest = True
                    duplicatePatient = True
            except:
                implMsg = "Patient.objects.filter {} {}".format(sys.exc_info()[0], data)
                implError = True

            if not badRequest and not implError:
                try:
                    patient = Patient(**kwargs)

                    if patient:
                        patient.save()
                    else:
                        implMsg = "Unable to create patient"
                        implError = True
                except:
                    implMsg = "Patient create {} {}".format(sys.exc_info()[0], data)
                    implError = True
        if badRequest:
            if duplicatePatient:
                r = HttpResponse(status=status.HTTP_409_CONFLICT, reason="Patient (%d) already exists".format(patient[0].id))
                return r
            else:
                return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': patient.id})
        
    @log_request
    def delete(self, request, patient_id=None, format=None):
        patient = None

        # see if the patient exists

        try:
            patient = Patient.objects.get(id=patient_id)
        except:
            patient = None

        if not patient:
            raise NotFound
        else:
            patient.delete()

        return Response({})

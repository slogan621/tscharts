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
from clinicstation.models import *
from station.models import *
from clinic.models import *
from routingslip.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json

class RoutingSlipView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):

        super(RoutingSlipView, self).__init__()

        self.catsToText = {'n': "New Cleft",
                           'd': "Dental",
                           'r': "Returning Cleft",
                           'o': "Ortho",
                           't': "Other",
                           'u': "Unknown"} 

        self.textToCats = {"New Cleft": 'n',
                           "Dental": 'd',
                           "Returning Cleft": 'r',
                           "Ortho": 'o',
                           "Other": 't',
                           "Unknown": 'u'} 

    def serialize(self, entry):

        error = False

        m = {}
        m["id"] = entry.id  
        m["patient"] = entry.patient_id
        m["clinic"] = entry.clinic_id
        m["category"] = self.catsToText[entry.category]

        try:
            routingslip = RoutingSlip.objects.get(id=entry.id)
        except:
            error = True

        if not error:
            m["routing"] = []
            try:
                entries = RoutingSlipEntry.objects.filter(routingslip = routingslip)
                if entries and len(entries):
                    #entries = entries.order_by("order")
                    for x in entries:
                        y = {}
                        y["id"] = x.id
                        m["routing"].append(y)
            except:
                error = True

        if not error:
            m["comments"] = []
            try:
                entries = RoutingSlipComment.objects.filter(routingslip = routingslip)
                if entries and len(entries):
                    #entries = entries.order_by('-updatetime')
                    for x in entries:
                        y = {}
                        y["id"] = x.id
                        m["comments"].append(y)
            except:
                error = True

        if error:
            m = None

        return m

    def get(self, request, routing_slip_id=None, format=None):
        routing_slip = None
        badParam = False
        notFound = False
        aClinic = None
        aPatient = None

        if routing_slip_id:
            try:
                routing_slip = RoutingSlip.objects.get(id = routing_slip_id)
            except:
                notFound = True
                routing_slip = None
        else:
            data = json.loads(request.body)
            try:
                clinicid = int(data["clinic"])
                try:
                    aClinic = Clinic.objects.get(id=clinicid)
                except:
                    aClinic = None
                    notFound = True
            except:
                pass

            if not notFound and not badParam:
                try:
                    patientid = data["patient"]
                    try:
                        aPatient = Patient.objects.get(id=patientid)
                    except:
                        notFound = True
                except:
                    pass

            if aPatient or aClinic:
                try:
                    if aPatient and aClinic:
                        routing_slip = RoutingSlip.objects.filter(patient=aPatient, clinic=aClinic)
                    elif aPatient:
                        routing_slip = RoutingSlip.objects.filter(patient=aPatient)
                    elif aClinic:
                        routing_slip = RoutingSlip.objects.filter(clinic=aClinic)
                except:
                    notFound = True
                    routing_slip = None

        if badParam:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if routing_slip: 
            if routing_slip_id:
                # one based on ID
                ret = self.serialize(routing_slip)
            elif aPatient:
                # one for patient [,clinic] pair
                ret = self.serialize(routing_slip[0])
            else:
                # array for all patients in clinic
                ret = []
                for x in routing_slip:
                    m = self.serialize(x);
                    if m == None:
                        ret = None
                        break
                    ret.append(m)
        if not ret:
            return HttpResponseServerError()
        return Response(ret)

    def post(self, request, format=None):
        badParam = False
        implError = False

        data = json.loads(request.body)
        try:
            clinicid = int(data["clinic"])
        except:
            badParam = True

        try:
            patientid = int(data["patient"])
        except:
            badParam = True

        try:
            category = data["category"]
        except:
            badParam = True

        if not category in ["Dental", "Ortho", "New Cleft", "Returning Cleft", "Unknown", "Other"]:
            badParam = True
        else:
            category = self.textToCats[category]

        if not badParam:

            # get the patient and clinic instances

            try:
                aClinic = Clinic.objects.get(id=clinicid)
            except:
                aClinic = None
 
            try:
                aPatient = Patient.objects.get(id=patientid)
            except:
                aPatient = None

            if not aClinic or not aPatient:
                raise NotFound

        if not badParam:

            routing_slip = None

            # see if the routing slip already exists

            try:
                routing_slip = RoutingSlip.objects.filter(clinic=aClinic,
                                                          patient=aPatient)
                if not routing_slip or len(routing_slip) == 0:
                    routing_slip = None
                else:
                    # exists, update the category (effectively, a PUT)
                    routing_slip = routing_slip[0]
                    routing_slip.category = category
                    routing_slip.save()
            except:
                pass

            if not routing_slip:
                try:
                    routing_slip = RoutingSlip(clinic=aClinic, patient=aPatient, category=category)
                    if routing_slip:
                        routing_slip.save()
                    else:
                        implError = True
                except Exception as e:
                    implError = True
                    implMsg = sys.exc_info()[0] 
        if badParam:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': routing_slip.id})

    def put(self, request, routing_slip_id=None, format=None):
        badParam = False
        implError = False
        notFound = False

        data = json.loads(request.body)
        try:
            category = data["category"]
            if not category in ["Dental", "Ortho", "New Cleft", "Returning Cleft", "Unknown", "Other"]:
                badParam = True
            else:
                category = self.textToCats[category]
        except:
            badParam = True

        if not badParam:
            routing_slip = None

            try:
                routing_slip = RoutingSlip.objects.filter(id=routing_slip_id)
                if not routing_slip or len(routing_slip) == 0:
                    routing_slip = None
                else:
                    routing_slip = routing_slip[0]
            except:
                pass

            if not routing_slip:
                notFound = True 
            else:
                try:
                    routing_slip.category=category
                    routing_slip.save()
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
        if badParam:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        return Response({})
        
    def delete(self, request, routing_slip_id=None, format=None):
        #remove routing slip, all comments, and all entries

        badParam = False 
        notFound = False 
        routing_slip = None

        if not routing_slip_id:
            badParam = True

        if not badParam:
            try:
                routing_slip = RoutingSlip.objects.get(id=routing_slip_id)
            except:
                notFound = True

        if not routing_slip:
            notFound = True

        if not badParam and not notFound:

            # remove dependent objects

            try:
                comments = RoutingSlipComment.objects.filter(routingslip=routing_slip)
            except:
                comments = None

            for x in comments:
                x.delete()

            try:
                entries = RoutingSlipEntry.objects.filter(routingslip=routing_slip)
            except:
                entries = None

            for x in entries:
                x.delete()

            routing_slip.delete()

        if badParam:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        return Response({})

class RoutingSlipEntryView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    stateToText = {"a": "Scheduled", "v": "Visited", "r": "Removed"}
    textToState = {"Scheduled": "a", "Visited": "v", "Removed": "r"}

    def serialize(self, entry):
        error = False

        try:
            m = {}
            m["id"] = entry.id  
            m["routingslip"] = entry.routingslip_id  
            m["clinicstation"] = entry.clinicstation_id
            m["order"] = entry.clinic_id
            m["state"] = stateToText[entry.state]
        except:
            error = True

        if error:
            m = None
        return m

    def get(self, request, routing_slip_entry_id=None, format=None):
        routing_slip_entry = None
        badParam = False
        notFound = False
        aRoutingSlip = None

        if routing_slip_entry_id:
            try:
                routing_slip_entry = RoutingSlipEntry.objects.filter(id = routing_slip_entry_id)
            except:
                routing_slip_entry = None
        else:
            data = json.loads(request.body)
            try:
                routingslipid = int(data["routingslip"])
                try:
                    aRoutingSlip = RoutingSlip.objects.get(id=routingslipid)
                    if not aRoutingSlip:
                        notFound = True
                except:
                    aRoutingSlip = None
                    notFound = True
            except:
                badParam = True

            if not notFound and not badParam:
                try:
                    routing_slip_entry = RoutingSlipEntry.objects.filter(routingslip=aRoutingSlip)
                except:
                    routing_slip_entry = None

        if badParam:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if routing_slip_entry:
            if routing_slip_entry_id:
                ret = serialize(routing_slip_entry)
            else:
                ret = []
                for x in routing_slip_entry:
                    ret.append(x.id)
            return Response(ret)

    def post(self, request, format=None):
        badParam = False
        implError = False

        data = json.loads(request.body)
        try:
            routingslipid = int(data["routingslip"])
        except:
            badParam = True

        try:
            clinicstationid = int(data["clinicstation"])
        except:
            badParam = True

        if not badParam:

            # get the routingslip and clinicstation instances

            try:
                aRoutingSlip = RoutingSlip.objects.get(id=routingslipid)
            except:
                aRoutingSlip = None
 
            try:
                aClinicStation = ClinicStation.objects.get(id=clinicstationd)
            except:
                aClinicStation = None

            if not aRoutingSlip or not aClinicStation:
                raise NotFound

        if not badParam:

            routing_slip_entry = None

            # see if the routing slip already exists

            try:
                routing_slip_entry = RoutingSlipEntry.objects.filter(clinicstation=aClinicStation, routingslip=aRoutingSlip)
                if not routing_slip_entry or len(routing_slip_entry) == 0:
                    routing_slip_entry = None
                else:
                    routing_slip_entry = routing_slip_entry[0]
            except:
                pass

            if not routing_slip_entry:
                try:
                    routing_slip_entry = RoutingSlipEntry(clinicstation=aClinicStation, order=0, category='a', routingslip=aRoutingSlip)
                    if routing_slipentry:
                        routing_slip_entry.save()
                    else:
                        implError = True
                except Exception as e:
                    implError = True
                    implMsg = sys.exc_info()[0] 
        if badParam:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': routing_slip_entry.id})

    def put(self, request, routing_slip_entry_id=None, format=None):
        badParam = False
        implError = False
        notFound = False

        data = json.loads(request.body)
        try:
            order = int(data["order"])
        except:
            order = None
        try:
            state = data["state"]
        except:
            state = None

        if not routing_slip_id:
            badParam = True

        if not badParam:
            if not state and not order: 
                badParam = True

        if not badParam:
            routing_slip_entry = None

            try:
                routing_slip_entry = RoutingSlipEntry.objects.get(id=routing_slip_entry_id)
            except:
                pass

            if not routing_slip_entry:
                notFound = True 
            else:
                if order:
                    routing_slip_entry.order = order
                if state:
                    routing_slip_entry.state = state
                try:
                    routing_slip_entry.save()
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
        
    def delete(self, request, routing_slip_entry_id=None, format=None):

        routing_slip_entry = None

        # see if the routing slip entry exists

        if not routing_slip_entry_id:
            return HttpResponseBadRequest()
        try:
            routing_slip_entry = RoutingSlipEntry.objects.get(id=routing_slip_entry_id)
        except:
            routing_slip_entry = None

        if not routing_slip_entry:
            raise NotFound
        else:
            routing_slip_entry.delete()

        return Response({})

class RoutingSlipCommentView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):

        m = {}
        m["id"] = entry.id  
        m["author"] = entry.author_id
        m["timestamp"] = entry.timestmap
        m["comment"] = entry.comment

        return m

    def get(self, request, routing_slip_comment_id=None, format=None):
        routing_slip_comment = None
        badRequest = False
        notFound = False
        aRoutingSlip = None

        if routing_slip_comment_id:
            try:
                routing_slip_comment = RoutingSlipComment.objects.get(id = routing_slip_comment_id)
            except:
                routing_slip_comment = None
        else:
            data = json.loads(request.body)
            try:
                routingslipid = int(data["routingslip"])
                try:
                    aRoutingSlip = RoutingSlip.objects.get(id=routingslipid)
                except:
                    aRoutingSlip = None
                    notFound = True
            except:
                badParam = True

            if not notFound and not badParam:
                try:
                   routing_slip_comment = RoutingSlipComment.objects.filter(routingslip=aRoutingSlip)
                except:
                    routing_slip_comment = None
                    notFound = True

        if badParam:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if routing_slip_comment:
            if routing_slip_comment_id:
                ret = serialize(routing_slip_comment)
            else:
                ret = []
                for x in routing_slip_comment:
                    ret.append(x.id)
            return Response(ret)

    def post(self, request, format=None):
        badParam = False
        implError = False

        data = json.loads(request.body)
        try:
            routingslipid = int(data["routingslip"])
        except:
            badParam = True

        try:
            authorid = int(data["author"])
        except:
            badParam = True

        try:
            comment = data["comment"]
        except:
            badParam = True

        if not badParam:

            # get the routingslip and person instances

            try:
                aRoutingSlip = RoutingSlip.objects.get(id=routingslipid)
            except:
                aRoutingSlip = None
 
            try:
                anAuthor = User.objects.get(id=authorid)
            except:
                anAuthor = None

            if not aRoutingSlip or not anAuthor:
                raise NotFound

        if not badParam:

            try:
                routing_slip_comment = RoutingSlipComment(routingslip=aRoutingSlip, author=anAuthor, comment=comment)
                if routing_slip_comment:
                    routing_slip_comment.save()
                else:
                    implError = True
            except Exception as e:
                implError = True
                implMsg = sys.exc_info()[0] 

        if badParam:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': routing_slip_comment.id})

    def delete(self, request, routing_slip_comment_id=None, format=None):

        routing_slip_comment = None

        # see if the routing slip comment exists

        if not routing_slip_comment_id:
            return HttpResponseBadRequest()
        try:
            routing_slip_comment = RoutingSlipComment.objects.get(id=routing_slip_comment_id)
        except:
            routing_slip_comment = None

        if not routing_slip_comment:
            raise NotFound
        else:
            routing_slip_comment.delete()

        return Response({})

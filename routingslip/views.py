#(C) Copyright Syd Logan 2017-2019
#(C) Copyright Thousand Smiles Foundation 2017-2019
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
from station.models import *
from clinic.models import *
from returntoclinicstation.models import *
from routingslip.models import *
from datetime import *
import sys
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

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
                           't': "Other"}

        self.textToCats = {"New Cleft": 'n',
                           "Dental": 'd',
                           "Returning Cleft": 'r',
                           "Ortho": 'o',
                           "Other": 't'}

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
                    entries = entries.order_by("order")
                    for x in entries:
                        m["routing"].append(x.id)
            except:
                error = True

        if not error:
            m["comments"] = []
            try:
                entries = RoutingSlipComment.objects.filter(routingslip = routingslip)
                if entries and len(entries):
                    entries = entries.order_by('-updatetime')
                    for x in entries:
                        m["comments"].append(x.id)
            except:
                error = True

        if error:
            m = None

        return m

    @log_request
    def get(self, request, routing_slip_id=None, format=None):
        routing_slip = None
        aClinic = None
        aPatient = None
        badRequest = False
        notFound = False
        ret = None

        if routing_slip_id:
            try:
                routing_slip = RoutingSlip.objects.get(id = routing_slip_id)
                if not routing_slip:
                    notFound = True
            except:
                notFound = True
                routing_slip = None
        else:
            # look for optional arguments
            try:
                clinicid = request.GET.get("clinic", '')
                if not clinicid == '':
                    try:
                        aClinic = Clinic.objects.get(id=clinicid)
                        if not aClinic:
                            notFound = True
                    except:
                        notFound = True
            except:
                pass # no clinic ID

            try:
                patientid = request.GET.get('patient', '')
                if not patientid == '':
                    try:
                        aPatient = Patient.objects.get(id=patientid)
                        if not aPatient:
                            notFound = True
                    except:
                        notFound = True
            except:
                pass # no patient ID

            if not notFound:
                if aPatient or aClinic:
                    try:
                        if aPatient and aClinic:
                            routing_slip = RoutingSlip.objects.get(patient=aPatient, clinic=aClinic)
                        elif aPatient:
                            routing_slip = RoutingSlip.objects.filter(patient=aPatient)
                        elif aClinic:
                            routing_slip = RoutingSlip.objects.filter(clinic=aClinic)
                    except:
                        notFound = True
                        routing_slip = None
                else:
                    badRequest = True

        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
	try:
            if routing_slip: 
                if routing_slip_id:
                    # one based on ID
                    ret = self.serialize(routing_slip)
                elif aPatient and aClinic:
                    # one for patient, clinic pair
                    ret = self.serialize(routing_slip)
                else:
                    # array
                    ret = []
                    for x in routing_slip:
                        m = self.serialize(x);
                        if m == None:
                            ret = None
                            break
                        ret.append(m)
                if ret:
                    return Response(ret)
                else:
                    return HttpResponseServerError() 
            else:
                return HttpResponseServerError() 
        except:
            return HttpResponseServerError()

    @log_request
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

        if not category in ["Dental", "Ortho", "New Cleft", "Returning Cleft", "Other"]:
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

    @log_request
    def put(self, request, routing_slip_id=None, format=None):
        badParam = False
        implError = False
        notFound = False

        data = json.loads(request.body)
        try:
            category = data["category"]
            if not category in ["Dental", "Ortho", "New Cleft", "Returning Cleft", "Other"]:
                badParam = True
            else:
                category = self.textToCats[category]
        except:
            badParam = True

        if not badParam:
            routing_slip = None

            try:
                routing_slip = RoutingSlip.objects.get(id=routing_slip_id)
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
       
    @log_request 
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

    def __init__(self):
        super(RoutingSlipEntryView, self).__init__()
        self.stateToText = {"n": "New", "s": "Scheduled", "i": "Checked In", "o": "Checked Out", "r": "Removed", "d": "Deleted", "l": "Return"}
        self.textToState = {"New": "n", "Scheduled": "s", "Checked In": "i", "Checked Out": "o", "Removed": "r", "Deleted": "d", "Return": "l"}

    def serialize(self, entry):
        error = False

        try:
            m = {}
            m["id"] = entry.id  
            m["routingslip"] = entry.routingslip_id  
            m["station"] = entry.station_id
            m["returntoclinicstation"] = entry.returntoclinicstation_id
            m["order"] = entry.order
            m["state"] = self.stateToText[entry.state]
        except:
            error = True

        if error:
            m = None
        return m

    @log_request
    def get(self, request, routing_slip_entry_id=None, format=None):
        routing_slip_entry = None
        aRoutingSlip = None
        aStation = None
        aReturnToClinicStation = None
        badRequest = False
        notFound = False
        stateFilters = []
        nullrcs = None
        kwargs = {}
        ret = None

        if routing_slip_entry_id:
            try:
                routing_slip_entry = RoutingSlipEntry.objects.get(id = routing_slip_entry_id)
                if not routing_slip_entry:
                    notFound = True
            except:
                routing_slip_entry = None
                notFound = True
        else:
            try:
                nullrcs = request.GET.get("nullrcs", '')
                if nullrcs == '':
                    nullrcs = None
                else:
                    if nullrcs == "true" or nullrcs == "True":
                        nullrcs = True
                    else:
                        nullrcs = False
            except:
                pass

            try:
                states = request.GET.get("states", '')
                if not states == '':
                    states = [x.strip() for x in states.split(",")]
                    if len(states):
                        for s in states:
                            try:
                                c = self.textToState[s]
                                stateFilters.append(c)
                            except:
                                badRequest = True
                                break
            except:
                pass

            try:
                routingslipid = request.GET.get("routingslip", '')
                if not routingslipid == '':
                    try:
                        aRoutingSlip = RoutingSlip.objects.get(id=routingslipid)
                        if not aRoutingSlip:
                            notFound = True
                        else:
                            kwargs["routingslip"] = aRoutingSlip
                    except:
                        notFound = True
            except:
                pass

            try:
                stationid = request.GET.get("station", '')
                if not stationid == '':
                    try:
                        aStation = Station.objects.get(id=stationid)
                        if not aStation:
                            notFound = True
                        else:
                            kwargs["station"] = aStation
                    except:
                        notFound = True
            except:
                pass

            try:
                returntoclinicstationid = request.GET.get("returntoclinicstation", '')
                if not returntoclinicstationid == '':
                    try:
                        aReturnToClinicStation = ReturnToClinicStation.objects.get(id=returntoclinicstationid)
                        if not aReturnToClinicStation:
                            notFound = True
                        else:
                            kwargs["returntoclinicstation"] = aReturnToClinicStation
                    except:
                        notFound = True
            except:
                pass

            if not notFound and not badRequest:
                try:
                    routing_slip_entry = RoutingSlipEntry.objects.filter(**kwargs)
                    if routing_slip_entry == None or len(routing_slip_entry) == 0:
                        routing_slip_entry = None
                        notFound = True
                except:
                    routing_slip_entry = None
                    notFound = True
        if notFound:
            return HttpResponseNotFound()
        if badRequest:
            return HttpResponseBadRequest()

        if routing_slip_entry:
            if routing_slip_entry_id:
                ret = self.serialize(routing_slip_entry)
            else:
                ret = []
                for x in routing_slip_entry:

                    # do some additional filtering

                    if nullrcs != None:
                        if nullrcs == True and x.returntoclinicstation:
                            continue
                        elif nullrcs == False and not x.returntoclinicstation:
                            continue

                    if len(stateFilters) and not x.state in stateFilters:
                            continue 

                    # got a match, append it

                    ret.append(x.id)
                if len(ret) == 0:
                    ret = None
                    return HttpResponseNotFound()
        if ret:
            return Response(ret)
        else:
            return HttpResponseNotFound()

    @log_request
    def post(self, request, format=None):
        badParam = False
        implError = False
        returntoclinicstationid = None
        kwargs = {}
        aReturnToClinicStation = None

        data = json.loads(request.body)
        try:
            routingslipid = int(data["routingslip"])
        except:
            badParam = True

        try:
            returntoclinicstationid = int(data["returntoclinicstation"])
        except:
            returntoclinicstationid = None

        try:
            stationid = int(data["station"])
        except:
            badParam = True

        if not badParam:

            # get the routingslip and station instances

            try:
                aRoutingSlip = RoutingSlip.objects.get(id=routingslipid)
                kwargs["routingslip"] = aRoutingSlip
            except:
                aRoutingSlip = None
 
            try:
                aStation = Station.objects.get(id=stationid)
                kwargs["station"] = aStation
            except:
                aStation = None

            if returntoclinicstationid != None:
                try:
                    aReturnToClinicStation = ReturnToClinicStation.objects.get(id=returntoclinicstationid)
                    if aReturnToClinicStation != None:
                        kwargs["returntoclinicstation"] = aReturnToClinicStation
                    else:
                        raise NotFound
                except:
                    raise NotFound

            if not aRoutingSlip or not aStation:
                raise NotFound

        if not badParam:

            routing_slip_entry = None

            # see if the routing slip already exists

            try:
                routing_slip_entry = RoutingSlipEntry.objects.filter(**kwargs)
                if not routing_slip_entry or len(routing_slip_entry) == 0:
                    routing_slip_entry = None
                else:
                    routing_slip_entry = routing_slip_entry[0]
            except:
                pass

            if not routing_slip_entry:
                try:
                    routing_slip_entry = RoutingSlipEntry(**kwargs)
                    if routing_slip_entry:
                        # set the order of the entry to the station level
                        routing_slip_entry.order = aStation.level
                        # if it is a returntoclinicstation, set state to "created"
                        if aReturnToClinicStation != None:
                            routing_slip_entry.state = "l"

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

    def verifyState(self, old, new):
        ret = True

        try:
            new = self.textToState[new]
        except:
            ret = False

        if ret:
            if old == "i":
                if new in ["s", "n", "r", "l"]:
                    ret = False
            elif old == "o":
                if new in ["s", "i", "n", 'l']:
                    ret = False
            elif old == "r":
                if new in ["i", "n", "o", "s"]:
                    ret = False
        return ret

    @log_request
    def put(self, request, routing_slip_entry_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False
        aReturnToClinicStation = None

        data = json.loads(request.body)
        try:
            order = int(data["order"])
        except:
            order = None
        try:
            state = data["state"]
        except:
            state = None
        try:
            returntoclinicstationid = int(data["returntoclinicstation"])
        except:
            returntoclinicstationid = None

        if returntoclinicstationid != None:
            try:
                aReturnToClinicStation = ReturnToClinicStation.objects.get(id=returntoclinicstationid)
                if aReturnToClinicStation == None:
                    raise NotFound
            except:
                raise NotFound

        if not routing_slip_entry_id:
            badRequest = True

        if not badRequest:
            if not state and not order and not returntoclinicstationid: 
                badRequest = True

        if not badRequest:
            routing_slip_entry = None

            try:
                routing_slip_entry = RoutingSlipEntry.objects.get(id=routing_slip_entry_id)
            except:
                pass

            if not routing_slip_entry:
                notFound = True 
            else:

                if state:
                    badRequest = not self.verifyState(routing_slip_entry.state, state)
                if not badRequest:
                    if aReturnToClinicStation:
                        routing_slip_entry.returntoclinicstation = aReturnToClinicStation
                    if order:
                        routing_slip_entry.order = order

                    if state:
                        routing_slip_entry.state = self.textToState[state]

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
       
    @log_request 
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
        m["routingslip"] = entry.routingslip_id  
        m["author"] = entry.author_id
        m["updatetime"] = entry.updatetime
        m["comment"] = entry.comment

        return m

    @log_request
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
                notFound = True
        else:
            # look for optional arguments
            try:
                routingslipid = request.GET.get("routingslip", '')
                if not routingslipid == '':
                    try:
                        aRoutingSlip = RoutingSlip.objects.get(id=routingslipid)
                        if not aRoutingSlip:
                            notFound = True
                    except:
                        notFound = True
            except:
                badRequest = True

            if not notFound and not badRequest:
                try:
                   routing_slip_comment = RoutingSlipComment.objects.filter(routingslip=aRoutingSlip)
                except:
                    routing_slip_comment = None
                    notFound = True

        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if routing_slip_comment:
            if routing_slip_comment_id:
                ret = self.serialize(routing_slip_comment)
            else:
                ret = []
                for x in routing_slip_comment:
                    ret.append(x.id)
            return Response(ret)

    @log_request
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

    @log_request
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

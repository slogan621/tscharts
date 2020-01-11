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
from enthistory.models import *
from enthistoryextra.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

import logging
LOG = logging.getLogger("tscharts")


class ENTHistoryExtraView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def durationToString(self, val):
        ret = None
        data = {ENTHistory.EAR_DURATION_NONE:"none",
                ENTHistory.EAR_DURATION_DAYS:"days",
                ENTHistory.EAR_DURATION_WEEKS:"weeks",
                ENTHistory.EAR_DURATION_MONTHS:"months",
                ENTHistory.EAR_DURATION_INTERMITTENT:"intermittent"}

        try:
            ret = data[val]
        except:
            pass
        return ret

    def stringToDuration(self, val):
        ret = None
        data = {"none":ENTHistory.EAR_DURATION_NONE,
                "days":ENTHistory.EAR_DURATION_DAYS,
                "weeks":ENTHistory.EAR_DURATION_WEEKS,
                "months":ENTHistory.EAR_DURATION_MONTHS,
                "intermittent":ENTHistory.EAR_DURATION_INTERMITTENT}

        try:
            ret = data[val]
        except:
            pass
        return ret

    def sideToString(self, val):
        ret = None
        data = {ENTHistory.EAR_SIDE_LEFT:"left",
                ENTHistory.EAR_SIDE_RIGHT:"right",
                ENTHistory.EAR_SIDE_BOTH:"both",
                ENTHistory.EAR_SIDE_NONE:"none"}

        try:
            ret = data[val]
        except:
            pass
        return ret

    def stringToSide(self, val):
        ret = None
        data = {"left":ENTHistory.EAR_SIDE_LEFT,
                "right":ENTHistory.EAR_SIDE_RIGHT,
                "both":ENTHistory.EAR_SIDE_BOTH,
                "none":ENTHistory.EAR_SIDE_NONE}

        try:
            ret = data[val]
        except:
            pass
        return ret

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["enthistory"] = entry.enthistory_id
        m["name"] = entry.name
        m["duration"] = self.durationToString(entry.duration)
        m["side"] = self.sideToString(entry.side)

        return m

    @log_request
    def get(self, request, ent_history_extra_id=None, format=None):
        ent_history_extra = None
        badRequest = False
        aENTHistory = None
        kwargs = {}

        if ent_history_extra_id:
            try:
                ent_history_extra = ENTHistoryExtra.objects.get(id = ent_history_extra_id)
            except:
                ent_history_extra = None
        else:
            # look for required arguments
            try:
                enthistoryid = request.GET.get('enthistory', '')
                if enthistoryid != '':
                    try:
                        aENTHistory = ENTHistory.objects.get(id=enthistoryid)
                        if not aENTHistory:
                            badRequest = True
                        else:
                            kwargs["enthistory"] = aENTHistory
                    except:
                        badRequest = True
            except:
                badRequest = True

            hasName = False
            name = None
            try:
                name = request.GET.get('name', '')
                if name != '':
                    hasName = True
            except:
                pass # no name subsearch

            if not badRequest:
                try:
                    ent_history_extra = ENTHistoryExtra.objects.filter(**kwargs)
                    if hasName == True:
                        # isn't django wonderful, just filter on the result :-)
                        ent_history_extra = ent_history_extra.filter(Q(name__icontains=name))
                except:
                    ent_history_extra = None

        if not ent_history_extra and not badRequest:
            raise NotFound
        elif not badRequest:
            if ent_history_extra_id:
                ret = self.serialize(ent_history_extra)
            else:
                ret = []
                for x in ent_history_extra:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if not "name" in data or not "enthistory" in data or not "duration" in data or not "side" in data:
            #LOG.info(u'validatePostArgs valid False 1 {}'.format(data))
            valid = False

        if "name" in data and len(data["name"]) == 0:
            #LOG.info(u'validatePostArgs valid False 2 {}'.format(data))
            valid = False

        try:
            val = self.stringToDuration(data["duration"])
            if val == None:
                #LOG.info(u'validatePostArgs valid False 3 {}'.format(data))
                valid = False
            else:
                kwargs["duration"] = val
        except:
            #LOG.info(u'validatePostArgs valid False 4 {}'.format(data))
            valid = False

        try:
            val = self.stringToSide(data["side"])
            if val == None:
                #LOG.info(u'validatePostArgs valid False 5 {}'.format(data))
                valid = False
            else:
                kwargs["side"] = val
        except:
            #LOG.info(u'validatePostArgs valid False 6 {}'.format(data))
            valid = False

        return valid, kwargs

    def validatePutArgs(self, data, ent_history_extra):
        valid = True

        if valid == True:
            if "name" in data:
                if len(data["name"]) > 0:
                    ent_history_extra.name = data["name"]
                else: 
                    valid = False

        try:
            if "duration" in data:
                val = self.stringToDuration(data["duration"])
                if val == None:
                    valid = False
                else:
                    ent_history_extra.duration = val
        except:
            pass

        try:
            if "side" in data:
                val = self.stringToSide(data["side"])
                if val == None:
                    valid = False
                else:
                    ent_history_extra.side = val
        except:
            pass

        return valid, ent_history_extra

    @log_request
    def post(self, request, format=None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        try:
            enthistoryid = int(data["enthistory"])
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
                aENTHistory = ENTHistory.objects.get(id=enthistoryid)
            except:
                aENTHistory = None
 
            if not aENTHistory:
                raise NotFound

        if not badRequest:
            try:
                kwargs["enthistory"] = aENTHistory
                ent_history_extra = ENTHistoryExtra(**kwargs)
                if ent_history_extra:
                    ent_history_extra.save()
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
            return Response({'id': ent_history_extra.id})

    @log_request
    def put(self, request, ent_history_extra_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_history_extra_id:
            badRequest = True

        if not badRequest:
            ent_history_extra = None

            try:
                ent_history_extra = ENTHistoryExtra.objects.get(id=ent_history_extra_id)
            except:
                pass

            if not ent_history_extra:
                notFound = True 
            else:
                try:
                    valid = True
                    data = json.loads(request.body)
                    valid, ent_history_extra = self.validatePutArgs(data, ent_history_extra)
                    if valid == True:
                        ent_history_extra.save()
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
    def delete(self, request, ent_history_extra_id=None, format=None):
        ent_history_extra = None

        # see if the ent history extra object exists

        if not ent_history_extra_id:
            return HttpResponseBadRequest()
        try:
            ent_history_extra = ENTHistoryExtra.objects.get(id=ent_history_extra_id)
        except:
            ent_history_extra = None

        if not ent_history_extra:
            raise NotFound
        else:
            ent_history_extra.delete()

        return Response({})

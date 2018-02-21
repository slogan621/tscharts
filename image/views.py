#(C) Copyright Syd Logan 2017-2018
#(C) Copyright Thousand Smiles Foundation 2017-2018
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
from image.models import *
from patient.models import *
from station.models import *
from clinic.models import *
from datetime import *
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from django.conf import settings
import json
import uuid
import os
import sys

class ImageView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def stringToType(self, aType):
        ret = None

        if aType == "Xray":
            ret = 'x'
        elif aType == "Surgery":
            ret = 's'
        elif aType == "Headshot":
            ret = 'h'
        return ret

    def typeToString(self, aType):
        ret = None

        if aType == "x":
            ret = 'Xray'
        elif aType == "s":
            ret = 'Surgery'
        elif aType == "h":
            ret = 'Headshot'
        return ret
    
    def getUUID(self):
        return uuid.uuid4()
    
    def getImageData(self, path, patient):
        # Build paths inside the project like this: os.path.join(BASE_DIR, ...)

        data = None
        patient = str(patient)
        try:
            imgPath = os.path.join(settings.CHART_IMAGES_DIR, patient, path)
            with open (imgPath, "r") as myfile:
                data=myfile.readlines()
        except:
            pass
        return data

    def deleteImageFile(self, path, patient):
        ret  = True
        patient = str(patient)
        try:
            imgPath = os.path.join(settings.CHART_IMAGES_DIR, patient, path)
            os.remove(imgPath)
        except:
            ret = False
        return ret

    def putImageData(self, path, patient, data):
        # Build paths inside the project like this: os.path.join(BASE_DIR, ...)

        implError = False
        implMsg = None
        patient = str(patient)

        try:
            patientDir = os.path.join(settings.CHART_IMAGES_DIR, patient)
            # create patient directory if it does not exist

            try:
                os.makedirs(patientDir)
            except:
                pass
            imgPath = os.path.join(patientDir, path)
            with open (imgPath, "w") as myfile:
                data=myfile.write(data)
        except:
            implError = True
            implMsg = sys.exc_info()[0] 

        return implError, implMsg

    def get(self, request, image_id=None, format=None):
        image = None
        badRequest = False
        notFound = False
        implError = False
        aClinic = None
        aStation = None
        aPatient = None
        sort = False
        newest = False

        if image_id:
            try:
                image = Image.objects.get(id=image_id)
            except:
                image = None
                notFound = True
        else:
            kwargs = {}

            sortarg = request.GET.get('sort', '')
            if not sortarg == '':
                if sortarg == "true":
                    sort = True
                elif sortarg == "false":
                    sort = False
                else:
                    badRequest = True 

            newest = request.GET.get('newest', '')
            if not newest == '':
                if newest == "true":
                    newest = True
                elif newest == "false":
                    newest = False
                else:
                    badRequest = True 

            if newest == True:
                sort = True             # force sort order

            patientid = request.GET.get('patient', '')
            if not patientid == '':
                patientid = int(patientid)
            else:
                patientid = None

            clinicid = request.GET.get('clinic', '')
            if not clinicid == '':
                clinicid = int(clinicid)
            else:
                clinicid = None

            stationid = request.GET.get('station', '')
            if not stationid == '':
                stationid = int(stationid)
            else:
                stationid = None

            if clinicid:
                try:
                    aClinic = Clinic.objects.get(id=clinicid)
                    if aClinic == None:
                        notFound = True
                    else:
                        kwargs["clinic"] = aClinic
                except:
                    notFound = True

            if stationid:
                try:
                    aStation = Station.objects.get(id=stationid)
                    if aStation == None:
                        notFound = True
                    else:
                        kwargs["station"] = aStation
                except:
                    notFound = True

            if patientid:
                try:
                    aPatient = Patient.objects.get(id=patientid)
                    if aPatient == None:
                        notFound = True
                    else:
                        kwargs["patient"] = aPatient
                except:
                    notFound = True

            if not badRequest and not notFound:
                typeid = request.GET.get('type', '')
                if typeid != '':
                    aType = self.stringToType(typeid)
                    if aType:
                        kwargs["imagetype"] = aType
                    else:
                        badRequest = True
                if not badRequest:
                    try:
                        if sort == True:
                            image = Image.objects.filter(**kwargs).order_by('-timestamp')
                        else:
                            image = Image.objects.filter(**kwargs)
                    except:
                        image = None
                    if not image:
                        notFound = True
                    elif len(image) == 0:
                        notFound == True

        if image and (not notFound) and (not badRequest):
            if image_id or (newest == True):
                ret = {}
                if newest == True:
                    image = image[0]
                ret["id"] = image.id
                ret["patient"] = image.patient_id
                ret["clinic"] = image.clinic_id
                ret["station"] = image.station_id
                ret["type"] = self.typeToString(image.imagetype)
                data = self.getImageData(image.path, image.patient_id)
                if not data:
                    implError = True
                else:
                    ret["data"] = data[0]
            else:
                ret = []
                for x in image:
                    ret.append(x.id)
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError() 

        return Response(ret)

    def post(self, request, format=None):
        badRequest = False
        implError = False
        clinicid = None
        stationid = None
        patientid = None

        kwargs = {}

        data = json.loads(request.body)
        if "clinic" in data:
            try:
                clinicid = int(data["clinic"])
            except:
                badRequest = True

        if "station" in data:
            try:
                stationid = int(data["station"])
            except:
                badRequest = True

        if "patient" in data:
            try:
                patientid = int(data["patient"])
            except:
                badRequest = True
        else:
            badRequest = True

        try:
            imagetype = self.stringToType(data["type"])
            if imagetype == None:
                badRequest = True
            else:
                kwargs["imagetype"] = imagetype
        except:
            badRequest = True

        try:
            imagedata = data["data"]
        except:
            badRequest = True

        if not badRequest:

            # get the patient, station and clinic instances

            if stationid != None:
                try:
                    aStation = Station.objects.get(id=stationid)
                    if aStation == None:
                        raise NotFound
                    kwargs["station"] = aStation   
                except:
                    raise NotFound

            if clinicid != None: 
                try:
                    aClinic = Clinic.objects.get(id=clinicid)
                    if aClinic == None:
                        raise NotFound
                    kwargs["clinic"] = aClinic   
                except:
                    raise NotFound

            try:
                aPatient = Patient.objects.get(id=patientid)
                if aPatient == None:
                    raise NotFound
                kwargs["patient"] = aPatient   
            except:
                raise NotFound

        if not badRequest:
            kwargs["path"] = path = str(self.getUUID())
            implError, implMsg = self.putImageData(path, patientid, imagedata)

        if not implError: 
            try:
                image = Image(**kwargs)
                if image:
                    image.save()
                else:
                    implError = True
                    implMsg = "Unable to create image object"
            except Exception as e:
                implError = True
                implMsg = sys.exc_info()[0] 
        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': image.id})

    def delete(self, request, image_id=None, format=None):
        image = None

        # see if the station exists

        if not image_id:
            return HttpResponseBadRequest()
        try:
            image = Image.objects.get(id=image_id)
        except:
            image = None

        if not image:
            raise NotFound
        else:
            self.deleteImageFile(image.path, image.patient_id) 
            image.delete()

        return Response({})

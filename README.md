# TSCharts
RESTful Patient Registration and Clinic Charts backend for Thousand Smiles Foundation.

# Overview

For background and overview on the context in which this project is being developed, please read the following:

 * [Registration requirements document](../master/docs/requirements/pdf/registration_requirements_1.2.pdf)

# API

The API consists of two major components. The first component is dedicated
to registration and routing of patients in our clinics. The second component
consists of the maintaining chart data to record the care that we give to our 
patients, organized by specialty.

The API is documented along with the source code in a README file located
in the same directory as the implementation. Links to each are provided
below.

The general structure of API requests follows RESTful principles:

 * POST - create objects
 * PUT - modify objects previously created
 * GET - retrieve objects. Most accept JSON paylods containing search terms,
or allow you to retrieve given a specific resource ID (all resource IDs are
unique and map to the primary key in the database for the item).
 * DELETE - remove a resource. Removal of a resource is provided but its use is
discouraged, generally we want the database to maintain a history of our 
clinics and deleting items is not consistent with that goal. There are uses
for DELETE however, such as unittest execution in an offline version of the
database.

The current API version is v1.

URLs are structured as follows:

/tscharts/v1/\<resource\>/[resource_id/]

In the above, \<resource\> is the name of a resource. It is used in the URL as
in the following example:

```
/tscharts/v1/clinicstation/17/
```

The above URL refers to the station and clinic pair with resource ID 17. Valid 
resource names are documented below.

Payloads (when provided as a part of POST and PUT requests) must be in JSON.

Generally, we use the following HTTP response codes to indicate the status
of a request:

 * 200 OK
 * 400 Bad Request
 * 404 Not Found
 * 500 Internal Server Error 

# Example Request and Response

```
GET /tscharts/v1/clinicstation/16/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae

HTTP/1.0 200 OK
Date: Fri, 14 Apr 2017 05:51:23 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS

{"active":true,"clinic":1553,"station":653,"id":16,"level":1}
```

# Python library (tschartslib)

The unit tests listed below are based on a Python library that thinly wraps 
the tscharts REST API. This library is named tschartslib, and can be installed 
using pip:

```
sudo pip install tschartslib
```

We are working on documentation for this library, but note that each module
includes unit tests that serve as examples for use. Here is a short example
that illustrates how to obtain a list of patients registered for a clinic:

```
from tschartslib.clinic.clinic import GetClinic
from tschartslib.register.register import GetAllRegistrations
from tschartslib.patient.patient import GetPatient

...

    # login. API requires an authentication token. Auth is basic Django Auth
    # username, password supplied by user. Check with system admin for host
    # and port (host is a string, port is an integer)

    token = None
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    if ret[0] == 200:
        token = ret[1]["token"]
    else:
        print("Unable to get access token {}".format(ret[0]))

    if token:
        # get today's clinic 

        x = GetClinic(host, port, token)
        x.setDate(datetime.utcnow().strftime("%m/%d/%Y"))
        ret = x.send(timeout=30)
        if ret[0] == 200:
            print("clinic {} on {} exists".format(ret[1]["id"], dateStr))
        elif ret[0] == 404:
            print("no clinic found on {}".format(dateStr))
        else:
            print("Unable to get clinic error code {}".format(ret[0]))

        # get all patients registered for the clinic

        if ret[0] == 200:
            clinicid = ret[1]["id"]
            x = GetAllRegistrations(host, port, token)
            x.setClinic(clinicid)
            ret = x.send(timeout=30)
            if ret[0] == 200:

                # now we have a list of registrations. Each includes
                # an id for the patient registered. Walk this list
                # and create an array of dicts with the patient details
                # that we care about

                registrations = ret[1]
                patients = []

                for x in registrations:
                    y = GetPatient(host, port, token)
                    y.setId(x["patient]")
                    registrationid = x["id"]
                    ret = y.send(timeout=30)
                    if ret[0] == 200:

                        # got the patient, extract details and add to list

                        patient = ret[1] 

                        p = {}
                        p["id"] = patient["id"]
                        p["registrationid"] = registrationid
                        p["clinicid"] = clinicid 
                        p["first"] = patient["first"]
                        p["first"] = patient["first"]
                        p["middle"] = patient["middle"]
                        p["paternal_last"] = patient["paternal_last"]
                        p["maternal_last"] = patient["maternal_last"]
                        p["dob"] = patient["dob"]
                        p["gender"] = patient["gender"]
                        patients.append(p)

        # list of patients registered for today's clinic

        return patients
```


For more information, visit https://pypi.org/project/tschartslib/


## Registration and Routing API

The following describes the registation and routing APIs. They are ordered in 
the generally expected order of use as a patient enters and leaves the clinic.

 * login - password-based login of user accessing the database. Returns token for use in Authorization header in subsequent requests.
    * [API](../master/tscharts/README.md)  
    * [Unit Tests](../master/tschartslib/tscharts/tscharts.py)
 * logout - logout user. 
    * [API](../master/tscharts/README.md)  
    * [Unit Tests](../master/tschartslib/tscharts/tscharts.py)
 * station - represents a class of station where care is given, e.g., a dental chair, ENT, Speech, Audiology, etc.. This resource is mostly static, created before any clinics are created. 
    * [API](../master/station/README.md)  
    * [Unit Tests](../master/tschartslib/station/station.py)
 * clinic - represents an instance of one of our clinics held at a specific location over a specific range of dates.  This resource is created offline before the clinic begins.
    * [API](../master/clinic/README.md)  
    * [Unit Tests](../master/tschartslib/clinic/clinic.py)
 * clinicstation - a tuple consisting of a clinic and a station. Each clinic instance will have a number of clinicstations.  This defines what stations were 
active at the clinic. Each clinicstation is created before the clinic.
    * [API](../master/clinicstation/README.md)  
    * [Unit Tests](../master/tschartslib/clinicstation/clinicstation.py)
 * patient - name, age, gender, and demographic information of a specific patient that has registered at one of our clinics. This information is gathered at registration time. 
    * [API](../master/patient/README.md)  
    * [Unit Tests](../master/tschartslib/patient/patient.py)
 * category - list of categories, one of which is assigned to the patient each time he or she is registered at a clinic. Used to determine what care is provided to the patient at the clinic.
    * [API](../master/category/README.md)  
    * [Unit Tests](../master/tschartslib/category/category.py)
 * image - image storage for a patient/clinic/station group. Used for x-rays, headshots, and surgery images. Images stored in base64. 
    * [API](../master/image/README.md)  
    * [Unit Tests](../master/tschartslib/image/image.py)
 * mexicanstates - used to get a list of Mexican state names as UTF-8 strings.
    * [API](../master/mexicanstates/README.md)  
    * [Unit Tests](../master/tschartslib/mexicanstates/mexicanstates.py)
 * queue - information about one or more clinic station queues as well as overall data related to patient wait times during an active clinic 
    * [API](../master/queue/README.md)  
    * [Unit Tests](../master/tschartslib/queue/queue.py)
 * register - a tuple that records the registration of a patient at a specific clinic. Also records the checkin and checkout times of the patient. 
    * [API](../master/register/README.md)  
    * [Unit Tests](../master/tschartslib/register/register.py)
 * routingslip - the routing slip for a patient. This defines what stations a patient is scheduled to visit or has visited at a specific clinic.
    * [API](../master/routingslip/routingslip.md)  
    * [Unit Tests](../master/tschartslib/routingslip/routingslip.py)
 * routingslipentry - an ordered routingslip/clinicstation tuple. Unique for a given routingslip.  
    * [API](../master/routingslip/routingslipentry.md)  
    * [Unit Tests](../master/tschartslib/routingslip/routingslip.py)
 * routingslipcomment - a comment made by a user on a specific routingslip, typically to document why a routingslipentry is present.  Records the comment and who made it. Multiple comments can be made by multiple people against a given routingslip.
    * [API](../master/routingslip/routingslipcomment.md)  
    * [Unit Tests](../master/tschartslib/routingslip/routingslip.py)
 * statechange - tracks the activity of patients and clinicstations for a specific clinic. Patients check "in" and "out" of clinicstations. Used to determine rputing of the patient. 
    * [API](../master/statechange/README.md)  
    * [Unit Tests](../master/tschartslib/statechange/statechange.py)
 * returntoclinic - used to record that a patient needs to return to a future clinic and visit a specific station at that future clinic. Used to prefill the routing slip of the patient at a subsequent visit. 
    * [API](../master/returntoclinic/README.md)  
    * [Unit Tests](../master/tschartslib/returntoclinic/returntoclinic.py)
 * returntoclinicstation - used to record that a patient needs to return during
the current clinic to a station the patient has aleady visited after visiting another clinic station. For example, a dentist may send a patient to x-ray and want the patient to be returned to dental once the x-rays have been taken. 
    * [API](../master/returntoclinicstation/README.md)  
    * [Unit Tests](../master/tschartslib/returntoclinicstation/returntoclinicstation.py)
 * consent - used to add, delete, update and get consent information from the database. Used to record the consent information of the patients.
    * [API](../master/consent/README.md)
    * [Unit Tests](../master/tschartslib/consent/consent.py) 

## Clinical Data APIs

The remaining APIs are oriented towards storing clinic data related to a
specialty.

 * audiogram - records audiogram images organized by patient and clinic 
    * [API](../master/audiogram/README.md)  
    * [Unit Tests](../master/tschartslib/audiogram/audiogram.py)

 * medicalhistory - patient status recorded at the time the patient registers. Records the overall health of the patient. 
    * [API](../master/medicalhistory/README.md)  
    * [Unit Tests](../master/tschartslib/medicalhistory/medicalhistory.py)

 * medications - used to add, delete and get medication names from the database. Used to update and retrieve the entire list of medications from the database.
    * [API](../master/medications/README.md)
    * [Unit Tests](../master/tschartslib/medications/medications.py)

 * surgerytype - used to add, delete and get surgery types from the database. Used to update and retrieve the entire list of surgery types from the database.
    * [API](../master/surgerytype/README.md)
    * [Unit Tests](../master/tschartslib/surgerytype/surgerytype.py)

 * surgeryhistory - used to add, delete, update and get surgery histories from the database. Used to record the surgery histories of the patients.
    * [API](../master/surgeryhistory/README.md)
    * [Unit Tests](../master/tschartslib/surgeryhistory/surgeryhistory.py)

 * xray - used to add, delete, modify and get xray records from the database. 
    * [API](../master/xray/README.md)
    * [Unit Tests](../master/tschartslib/xray/xray.py)

 * dentalcdt - used to add, delete, modify and get dental cdt code records from the database. 
    * [API](../master/dentalcdt/README.md)
    * [Unit Tests](../master/tschartslib/dentalcdt/dentalcdt.py)

 * dentalstate - used to add, delete, modify and get dental state records from the database. 
    * [API](../master/dentalstate/README.md)
    * [Unit Tests](../master/tschartslib/dentalstate/dentalstate.py)

 * dentaltreatment - used to add, delete, modify and get dental treatment records from the database. 
    * [API](../master/dentaltreatment/README.md)
    * [Unit Tests](../master/tschartslib/dentaltreatment/dentaltreatment.py)

 * enthistory - used to add, delete, modify and get ENT medical history records from the database. 
    * [API](../master/enthistory/README.md)
    * [Unit Tests](../master/tschartslib/enthistory/enthistory.py)

 * enthistoryextra - used to add, delete, modify and get ENT history "extra" records from the database. These are records that contain data not supported by enthistory tables, extending the conditions recorded for a specific enthistory record.
    * [API](../master/enthistoryextra/README.md)
    * [Unit Tests](../master/tschartslib/enthistoryextra/enthistoryextra.py)

 * enttreatment - used to add, delete, modify and get ENT treatment records from the database. 
    * [API](../master/enttreatment/README.md)
    * [Unit Tests](../master/tschartslib/enttreatment/enttreatment.py)

 * entexam - used to add, delete, modify and get ENT exam records from the database. 
    * [API](../master/entexam/README.md)
    * [Unit Tests](../master/tschartslib/entexam/entexam.py)

 * entsurgicalhistory - used to add, delete, modify and get ENT surgical history records from the database. 
    * [API](../master/entsurgicalhistory/README.md)
    * [Unit Tests](../master/tschartslib/entsurgicalhistory/entsurgicalhistory.py)

 * entdiagnosis - used to add, delete, modify and get ENT diagnosis records from the database. 
    * [API](../master/entdiagnosis/README.md)
    * [Unit Tests](../master/tschartslib/entdiagnosis/entdiagnosis.py)

 * entdiagnosisextra - used to add, delete, modify and get ENT diagnosis records from the database. These are records that contain data not supported by entdiagnosis tables, extending the conditions recorded for a specific entdiagnosis record.
    * [API](../master/entdiagnosisextra/README.md)
    * [Unit Tests](../master/tschartslib/entdiagnosisextra/entdiagnosisextra.py)


# License

```
(C) Copyright Syd Logan 2016-2021
(C) Copyright Thousand Smiles Foundation 2016-2021

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

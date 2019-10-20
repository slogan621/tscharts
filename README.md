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

## Registration and Routing API

The following describes the registation and routing APIs. They are ordered in 
the generally expected order of use as a patient enters and leaves the clinic.

 * login - password-based login of user accessing the database. Returns token for use in Authorization header in subsequent requests.
    * [API](../master/tscharts/README.md)  
    * [Unit Tests](../master/test/tscharts/tscharts.py)
 * logout - logout user. 
    * [API](../master/tscharts/README.md)  
    * [Unit Tests](../master/test/tscharts/tscharts.py)
 * station - represents a class of station where care is given, e.g., a dental chair, ENT, Speech, Audiology, etc.. This resource is mostly static, created before any clinics are created. 
    * [API](../master/station/README.md)  
    * [Unit Tests](../master/test/station/station.py)
 * clinic - represents an instance of one of our clinics held at a specific location over a specific range of dates.  This resource is created offline before the clinic begins.
    * [API](../master/clinic/README.md)  
    * [Unit Tests](../master/test/clinic/clinic.py)
 * clinicstation - a tuple consisting of a clinic and a station. Each clinic instance will have a number of clinicstations.  This defines what stations were 
active at the clinic. Each clinicstation is created before the clinic.
    * [API](../master/clinicstation/README.md)  
    * [Unit Tests](../master/test/clinicstation/clinicstation.py)
 * patient - name, age, gender, and demographic information of a specific patient that has registered at one of our clinics. This information is gathered at registration time. 
    * [API](../master/patient/README.md)  
    * [Unit Tests](../master/test/patient/patient.py)
 * category - list of categories, one of which is assigned to the patient each time he or she is registered at a clinic. Used to determine what care is provided to the patient at the clinic.
    * [API](../master/category/README.md)  
    * [Unit Tests](../master/test/category/category.py)
 * image - image storage for a patient/clinic/station group. Used for x-rays, headshots, and surgery images. Images stored in base64. 
    * [API](../master/image/README.md)  
    * [Unit Tests](../master/test/image/image.py)
 * mexicanstates - used to get a list of Mexican state names as UTF-8 strings.
    * [API](../master/mexicanstates/README.md)  
    * [Unit Tests](../master/test/mexicanstates/mexicanstates.py)
 * queue - information about one or more clinic station queues as well as overall data related to patient wait times during an active clinic 
    * [API](../master/queue/README.md)  
    * [Unit Tests](../master/test/queue/queue.py)
 * register - a tuple that records the registration of a patient at a specific clinic. Also records the checkin and checkout times of the patient. 
    * [API](../master/register/README.md)  
    * [Unit Tests](../master/test/register/register.py)
 * routingslip - the routing slip for a patient. This defines what stations a patient is scheduled to visit or has visited at a specific clinic.
    * [API](../master/routingslip/routingslip.md)  
    * [Unit Tests](../master/test/routingslip/routingslip.py)
 * routingslipentry - an ordered routingslip/clinicstation tuple. Unique for a given routingslip.  
    * [API](../master/routingslip/routingslipentry.md)  
    * [Unit Tests](../master/test/routingslip/routingslip.py)
 * routingslipcomment - a comment made by a user on a specific routingslip, typically to document why a routingslipentry is present.  Records the comment and who made it. Multiple comments can be made by multiple people against a given routingslip.
    * [API](../master/routingslip/routingslipcomment.md)  
    * [Unit Tests](../master/test/routingslip/routingslip.py)
 * statechange - tracks the activity of patients and clinicstations for a specific clinic. Patients check "in" and "out" of clinicstations. Used to determine rputing of the patient. 
    * [API](../master/statechange/README.md)  
    * [Unit Tests](../master/test/statechange/statechange.py)
 * returntoclinic - used to record that a patient needs to return to a future clinic and visit a specific station at that future clinic. Used to prefill the routing slip of the patient at a subsequent visit. 
    * [API](../master/returntoclinic/README.md)  
    * [Unit Tests](../master/test/returntoclinic/returntoclinic.py)
 * returntoclinicstation - used to record that a patient needs to return during
the current clinic to a station the patient has aleady visited after visiting another clinic station. For example, a dentist may send a patient to x-ray and want the patient to be returned to dental once the x-rays have been taken. 
    * [API](../master/returntoclinicstation/README.md)  
    * [Unit Tests](../master/test/returntoclinicstation/returntoclinicstation.py)
 * consent - used to add, delete, update and get consent information from the database. Used to record the consent information of the patients.
    * [API](../master/consent/README.md)
    * [Unit Tests](../master/test/consent/consent.py) 

## Clinical Data APIs

The remaining APIs are oriented towards storing clinic data related to a
specialty.

 * medicalhistory - patient status recorded at the time the patient registers. Records the overall health of the patient. 
    * [API](../master/medicalhistory/README.md)  
    * [Unit Tests](../master/test/medicalhistory/medicalhistory.py)

 * medications - used to add, delete and get medication names from the database. Used to update and retrieve the entire list of medications from the database.
    * [API](../master/medications/README.md)
    * [Unit Tests](../master/test/medications/medications.py)

 * surgerytype - used to add, delete and get surgery types from the database. Used to update and retrieve the entire list of surgery types from the database.
    * [API](../master/surgerytype/README.md)
    * [Unit Tests](../master/test/surgerytype/surgerytype.py)

 * surgeryhistory - used to add, delete, update and get surgery histories from the database. Used to record the surgery histories of the patients.
    * [API](../master/surgeryhistory/README.md)
    * [Unit Tests](../master/test/surgeryhistory/surgeryhistory.py)

 * xray - used to add, delete, modify and get xray records from the database. 
    * [API](../master/xray/README.md)
    * [Unit Tests](../master/test/xray/xray.py)

 * enthistory - used to add, delete, modify and get ENT medical history records from the database. 
    * [API](../master/enthistory/README.md)
    * [Unit Tests](../master/test/enthistory/enthistory.py)

 * enttreatment - used to add, delete, modify and get ENT treatment records from the database. 
    * [API](../master/enttreatment/README.md)
    * [Unit Tests](../master/test/enttreatment/enttreatment.py)

 * entexam - used to add, delete, modify and get ENT exam records from the database. 
    * [API](../master/entexam/README.md)
    * [Unit Tests](../master/test/entexam/entexam.py)

 * entdiagnosis - used to add, delete, modify and get ENT diagnosis records from the database. 
    * [API](../master/entdiagnosis/README.md)
    * [Unit Tests](../master/test/entdiagnosis/entdiagnosis.py)


# License

```
(C) Copyright Syd Logan 2016-2019
(C) Copyright Thousand Smiles Foundation 2016-2019

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

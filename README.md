# TSCharts
RESTful Patient Registration and Clinic Charts backend for Thousand Smiles Foundation.

# Overview

For background on the context in which this project is being developed,
please read the [the requirements document](../blob/master/docs/requirements/pdf/registration_requirements_1.2.pdf)

# API

The API consists of two major components. The first component is dedicated
to registration and routing of patients in our clinics. The second component
consists of the maintining charting data to record the care we give to our 
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

/tscharts/v1/\<resourcei\>/[resource_id/]

In the above, \<resource\> is the name of a resource. It is used in the URL as
in the following example:

```
/tscharts/v1/clinicstation/17/
```

refers to the station and clinic pair with resource ID 17. Valid resource
names are documented in the next section.

## Registration and Routing API Resource Names

 * clinic - represents an instance of one of our clinics held at a specific location over a specific range of dates
 * station - represents a class of station that care is given, e.g., a dental chair, ENT, Speech, Audiology, etc.
 * clinicstation - a tuple consisting of a clinic and a station. Each clinic instance will have a number of clinic stations.
 * patient - name, agem gender, and demographics of a specific patient that has registered at one of our clinics.
 * medicalhistory - patient status recorded at the time the patient registers. Determine overall health of the patient.
 * register - a tuple that records the registration of a patient at a specific clinic. Also records checkin and checkout times.
 * tscharts - support resource, used for authentication of users accessing the
database
 * routingslip - the routing slip for a patient. This defines what stations a patient is scheduled to visit or has visited at a specific clinic
 * routingslipentry - an ordered routinglip/clinicstation/patient tuple.
 * routingslipcomment - a comment made by a user on a specific routingslip, typically to document why a routingslipentry is present.
 * statechange - tracks the activity of patients and clinicstations for a specific clinic. Patients check "in" and "out" of clinicstations. 
 * returntoclinic - used to record that a patient needs to return to a future clinic and visit a specific station at that future clinic.

Payload (when provided) must be in JSON.

Generally, we use the following HTTP response code to indicate the status
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

[{"active":true,"clinic":1553,"station":653,"id":16,"level":1}]
```

# License

(C) Copyright Syd Logan 2016
(C) Copyright Thousand Smiles Foundation 2016

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


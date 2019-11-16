**Get ENT Diagnosis**

----
  Returns json data about a single ENT diagnosis resource. 

* **URL**

  /tscharts/v1/entdiagnosis/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "hlConductive": "left" | "right" | "both" | "none", "hl":  "left" | "right" | "both" | "none", "hlMixed":  "left" | "right" | "both" | "none", "hlSensory":  "left" | "right" | "both" | "none", "externalCerumenImpaction":  "left" | "right" | "both" | "none", "externalEarCanalFB":  "left" | "right" | "both" | "none", "externalMicrotia": "left" | "right" | "both" | "none", "tympanicAtelectasis":  "left" | "right" | "both" | "none", "tympanicGranuloma":  "left" | "right" | "both" | "none", "tympanicMonomer":  "left" | "right" | "both" | "none", "tympanicTube":  "left" | "right" | "both" | "none", "tympanicPerf":  "left" | "right" | "both" | "none", "middleEarCholesteatoma":  "left" | "right" | "both" | "none", "middleEarEustTubeDysTMRetraction":  "left" | "right" | "both" | "none", "middleEarOtitisMedia":  "left" | "right" | "both" | "none", "middleEarSerousOtitisMedia":  "left" | "right" | "both" | "none", "syndromeHemifacialMicrosomia":  "left" | "right" | "both" | "none", "syndromePierreRobin":  "left" | "right" | "both" | "none", "oralAnkyloglossia":  true | false, "oralTonsilEnlarge":  true | false, "oralCleftLipRepairDeformity":  true | false, "oralCleftLipUnilateral":  true | false, "oralCleftLipBilateral":  true | false, "oralCleftLipUnrepaired":  true | false, "oralCleftLipRepaired":  true | false, "oralCleftPalateUnilateral":  true | false, "oralCleftPalateBilateral":  true | false, "oralCleftPalateUnrepaired":  true | false, "oralCleftPalateRepaired":  true | false, "oralSpeechProblem":  true | false, "noseDeviatedSeptum":  true | false, "noseTurbinateHypertrophy":  true | false, "noseDeformitySecondaryToCleftPalate":  true | false, "username" : text, "comment": text}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/entdiagnosis/12/ HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json

2c5
{"id" : 74, "clinic" : 14, "patient" : 29, "time" : "2017-12-11T01:02:24", "hlConductive": "left", "hl": "none", "hlMixed":  "right", "hlSensory":  "both", "externalCerumenImpaction":  "left", "externalEarCanalFB":  "left", "externalMicrotia": "right", "tympanicAtelectasis":  "right", "tympanicGranuloma":  "left", "tympanicMonomer": "none", "tympanicTube": "left", "tympanicPerf": "right", "middleEarCholesteatoma": "both", "middleEarEustTubeDysTMRetraction": "right", "middleEarOtitisMedia": "left", "middleEarSerousOtitisMedia": "left", "syndromeHemifacialMicrosomia": "both", "syndromePierreRobin": "none", "oralAnkyloglossia": true, "oralTonsilEnlarge": false, "oralCleftLipRepairDeformity": false, "oralCleftLipUnilateral": true, "oralCleftLipBilateral": false, "oralCleftLipUnrepaired": false, "oralCleftLipRepaired": true, "oralCleftPalateUnilateral": false, "oralCleftPalateBilateral": true, "oralCleftPalateUnrepaired": false, "oralCleftPalateRepaired": true, "oralSpeechProblem": false, "noseDeviatedSeptum": false, "noseTurbinateHypertrophy": false, "noseDeformitySecondaryToCleftPalate": true, "username" : "lebovits", "comment": ""}
```
  
**Get Multiple ENT Diagnosis Records**
----
  Returns data about all matching ENT diagnosis resources.

* **URL**

  /tscharts/v1/entdiagnosis/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

   `patient` patient id<br />
   `clinic` clinic id<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
 
   [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "hlConductive": "left" | "right" | "both" | "none", "hl":  "left" | "right" | "both" | "none", "hlMixed":  "left" | "right" | "both" | "none", "hlSensory":  "left" | "right" | "both" | "none", "externalCerumenImpaction":  "left" | "right" | "both" | "none", "externalEarCanalFB":  "left" | "right" | "both" | "none", "externalMicrotia": "left" | "right" | "both" | "none", "tympanicAtelectasis":  "left" | "right" | "both" | "none", "tympanicGranuloma":  "left" | "right" | "both" | "none", "tympanicMonomer":  "left" | "right" | "both" | "none", "tympanicTube":  "left" | "right" | "both" | "none", "tympanicPerf":  "left" | "right" | "both" | "none", "middleEarCholesteatoma":  "left" | "right" | "both" | "none", "middleEarEustTubeDysTMRetraction":  "left" | "right" | "both" | "none", "middleEarOtitisMedia":  "left" | "right" | "both" | "none", "middleEarSerousOtitisMedia":  "left" | "right" | "both" | "none", "syndromeHemifacialMicrosomia":  "left" | "right" | "both" | "none", "syndromePierreRobin":  "left" | "right" | "both" | "none", "oralAnkyloglossia":  true | false, "oralTonsilEnlarge":  true | false, "oralCleftLipRepairDeformity":  true | false, "oralCleftLipUnilateral":  true | false, "oralCleftLipBilateral":  true | false, "oralCleftLipUnrepaired":  true | false, "oralCleftLipRepaired":  true | false, "oralCleftPalateUnilateral":  true | false, "oralCleftPalateBilateral":  true | false, "oralCleftPalateUnrepaired":  true | false, "oralCleftPalateRepaired":  true | false, "oralSpeechProblem":  true | false, "noseDeviatedSeptum":  true | false, "noseTurbinateHypertrophy":  true | false, "noseDeformitySecondaryToCleftPalate":  true | false, "username" : text, "comment": text}, ...]

* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/entdiagnosis/?patient=3&clinic=17 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


859
[{"id" : 74, "clinic" : 17, "patient" : 3, "time" : "2017-12-11T01:02:24", "hlConductive": "left", "hl": "none", "hlMixed":  "right", "hlSensory":  "both", "externalCerumenImpaction":  "left", "externalEarCanalFB":  "left", "externalMicrotia": "right", "tympanicAtelectasis":  "right", "tympanicGranuloma":  "left", "tympanicMonomer": "none", "tympanicTube": "left", "tympanicPerf": "right", "middleEarCholesteatoma": "both", "middleEarEustTubeDysTMRetraction": "right", "middleEarOtitisMedia": "left", "middleEarSerousOtitisMedia": "left", "syndromeHemifacialMicrosomia": "both", "syndromePierreRobin": "none", "oralAnkyloglossia": true, "oralTonsilEnlarge": false, "oralCleftLipRepairDeformity": false, "oralCleftLipUnilateral": true, "oralCleftLipBilateral": false, "oralCleftLipUnrepaired": false, "oralCleftLipRepaired": true, "oralCleftPalateUnilateral": false, "oralCleftPalateBilateral": true, "oralCleftPalateUnrepaired": false, "oralCleftPalateRepaired": true, "oralSpeechProblem": false, "noseDeviatedSeptum": false, "noseTurbinateHypertrophy": false, "noseDeformitySecondaryToCleftPalate": true, "username" : "lebovits", "comment": ""}]
0
```
  
**Create an ENT Diagnosis Resource**
----
  Create an ENT diagnosis resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/diagnosis/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `comment` comment supplied by the user for this exam item<br />
   `username` name of logged in user making this change <br />

   `hlConductive` one of the following: "left", "right", "both", "none"<br/>
   `hl` one of the following: "left", "right", "both", "none"<br/>
   `hlMixed` one of the following: "left", "right", "both", "none"<br/>
   `hlSensory` one of the following: "left", "right", "both", "none"<br/>
   `externalCerumenImpaction` one of the following: "left", "right", "both", "none"<br/>
   `externalEarCanalFB` one of the following: "left", "right", "both", "none"<br/>
   `externalMicrotia` one of the following:"left", "right", "both", "none"<br/>
   `tympanicAtelectasis` one of the following: "left", "right", "both", "none"<br/>
   `tympanicGranuloma` one of the following: "left", "right", "both", "none"<br/>
   `tympanicMonomer` one of the following: "left", "right", "both", "none"<br/>
   `tympanicTube` one of the following: "left", "right", "both", "none"<br/>
   `tympanicPerf` one of the following: "left", "right", "both", "none"<br/>
   `middleEarCholesteatoma` one of the following: "left", "right", "both", "none"<br/>
   `middleEarEustTubeDysTMRetraction` one of the following: "left", "right", "both", "none"<br/>
   `middleEarOtitisMedia` one of the following: "left", "right", "both", "none"<br/>
   `middleEarSerousOtitisMedia` one of the following: "left", "right", "both", "none"<br/>
   `syndromeHemifacialMicrosomia` one of the following: "left", "right", "both", "none"<br/>
   `syndromePierreRobin` one of the following: "left", "right", "both", "none"<br/>
   `oralAnkyloglossia` one of the following: true, false<br/>
   `oralTonsilEnlarge` one of the following: true, false<br/>
   `oralCleftLipRepairDeformity` one of the following: true, false<br/>
   `oralCleftLipUnilateral` one of the following: true, false<br/>
   `oralCleftLipBilateral` one of the following: true, false<br/>
   `oralCleftLipUnrepaired` one of the following: true, false<br/>
   `oralCleftLipRepaired` one of the following: true, false<br/>
   `oralCleftPalateUnilateral` one of the following: true, false<br/>
   `oralCleftPalateBilateral` one of the following: true, false<br/>
   `oralCleftPalateUnrepaired` one of the following: true, false<br/>
   `oralCleftPalateRepaired` one of the following: true, false<br/>
   `oralSpeechProblem` one of the following: true, false<br/>
   `noseDeviatedSeptum` one of the following: true, false<br/>
   `noseTurbinateHypertrophy` one of the following: true, false<br/>
   `noseDeformitySecondaryToCleftPalate` one of the following: true, false<br/>

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "id" : id }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/entdiagnosis/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"clinic" : 14, "patient" : 29, "hlConductive": "left", "hl": "none", "hlMixed":  "right", "hlSensory":  "both", "externalCerumenImpaction":  "left", "externalEarCanalFB":  "left", "externalMicrotia": "right", "tympanicAtelectasis":  "right", "tympanicGranuloma":  "left", "tympanicMonomer": "none", "tympanicTube": "left", "tympanicPerf": "right", "middleEarCholesteatoma": "both", "middleEarEustTubeDysTMRetraction": "right", "middleEarOtitisMedia": "left", "middleEarSerousOtitisMedia": "left", "syndromeHemifacialMicrosomia": "both", "syndromePierreRobin": "none", "oralAnkyloglossia": true, "oralTonsilEnlarge": false, "oralCleftLipRepairDeformity": false, "oralCleftLipUnilateral": true, "oralCleftLipBilateral": false, "oralCleftLipUnrepaired": false, "oralCleftLipRepaired": true, "oralCleftPalateUnilateral": false, "oralCleftPalateBilateral": true, "oralCleftPalateUnrepaired": false, "oralCleftPalateRepaired": true, "oralSpeechProblem": false, "noseDeviatedSeptum": false, "noseTurbinateHypertrophy": false, "noseDeformitySecondaryToCleftPalate": true, "username" : "lebovits", "comment": ""}HTTP/1.0 200 OK
Date: Mon, 11 Dec 2017 01:02:23 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


8
{"id":2}
0
```

**Update an ENT Diagnosis Record**
----
  Update an ENT diagnosis instance

* **URL**

  /tscharts/v1/entdiagnosis/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `comment` comment supplied by the user for this exam item<br />
   `username` name of logged in user making this change <br />
   `hlConductive` one of the following: "left", "right", "both", "none"<br/>
   `hl` one of the following: "left", "right", "both", "none"<br/>
   `hlMixed` one of the following: "left", "right", "both", "none"<br/>
   `hlSensory` one of the following: "left", "right", "both", "none"<br/>
   `externalCerumenImpaction` one of the following: "left", "right", "both", "none"<br/>
   `externalEarCanalFB` one of the following: "left", "right", "both", "none"<br/>
   `externalMicrotia` one of the following:"left", "right", "both", "none"<br/>
   `tympanicAtelectasis` one of the following: "left", "right", "both", "none"<br/>
   `tympanicGranuloma` one of the following: "left", "right", "both", "none"<br/>
   `tympanicMonomer` one of the following: "left", "right", "both", "none"<br/>
   `tympanicTube` one of the following: "left", "right", "both", "none"<br/>
   `tympanicPerf` one of the following: "left", "right", "both", "none"<br/>
   `middleEarCholesteatoma` one of the following: "left", "right", "both", "none"<br/>
   `middleEarEustTubeDysTMRetraction` one of the following: "left", "right", "both", "none"<br/>
   `middleEarOtitisMedia` one of the following: "left", "right", "both", "none"<br/>
   `middleEarSerousOtitisMedia` one of the following: "left", "right", "both", "none"<br/>
   `syndromeHemifacialMicrosomia` one of the following: "left", "right", "both", "none"<br/>
   `syndromePierreRobin` one of the following: "left", "right", "both", "none"<br/>
   `oralAnkyloglossia` one of the following: true, false<br/>
   `oralTonsilEnlarge` one of the following: true, false<br/>
   `oralCleftLipRepairDeformity` one of the following: true, false<br/>
   `oralCleftLipUnilateral` one of the following: true, false<br/>
   `oralCleftLipBilateral` one of the following: true, false<br/>
   `oralCleftLipUnrepaired` one of the following: true, false<br/>
   `oralCleftLipRepaired` one of the following: true, false<br/>
   `oralCleftPalateUnilateral` one of the following: true, false<br/>
   `oralCleftPalateBilateral` one of the following: true, false<br/>
   `oralCleftPalateUnrepaired` one of the following: true, false<br/>
   `oralCleftPalateRepaired` one of the following: true, false<br/>
   `oralSpeechProblem` one of the following: true, false<br/>
   `noseDeviatedSeptum` one of the following: true, false<br/>
   `noseTurbinateHypertrophy` one of the following: true, false<br/>
   `noseDeformitySecondaryToCleftPalate` one of the following: true, false<br/>

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/entdiagnosis/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"noseTurbinateHypertrophy": true}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete an ENT Diagnosis Record**
----
  Delete an ENT diagnosis resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/entdiagnosis/id

* **Method:**

  `DELETE`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** None
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
DELETE /tscharts/v1/entdiagnosis/140/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:49 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```


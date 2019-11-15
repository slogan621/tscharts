**Get ENT Surgical History**

----
  Returns json data about a single ENT surgical history resource. 

* **URL**

  /tscharts/v1/entsurgicalhistory/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "tubes": "left" | "right" | "both" | "none", "tubescomment": text, "tplasty":  "left" | "right" | "both" | "none", "tplastycomment": text, "eua":  "left" | "right" | "both" | "none", "euacomment": text, "fb":  "left" | "right" | "both" | "none", "fbcomment": text, "myringotomy":  "left" | "right" | "both" | "none", "myringotomycomment": text, "cerumen":  "left" | "right" | "both" | "none", "cerumencomment": text, "granuloma": "left" | "right" | "both" | "none", "granulomacomment": text, "septorhinoplasty":  true | false, "septorhinoplastycomment": text, "scarrevision":  true | false, "scarrevisioncomment": text, "frenulectomy":  true | false, "frenulectomycomment": text, "username" : text}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/entsurgicalhistory/12/ HTTP/1.1
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
{"id" : id, "clinic" : 14, "patient" : 29, "time" : "2017-12-11T01:02:24", "tubes": "left", "tubescomment": "", "tplasty": "none", "tplastycomment": "", "eua":  "none", "euacomment": "", "fb":  "left", "fbcomment": "", "myringotomy":  "both", "myringotomycomment": "", "cerumen":  "both", "cerumencomment": "", "granuloma": "none", "granulomacomment": "", "septorhinoplasty":  false, "septorhinoplastycomment": "", "scarrevision":  false, "scarrevisioncomment": "", "frenulectomy": false, "frenulectomycomment": "", "username" : "lebovits"}
```
  
**Get Multiple ENT Diagnosis Records**
----
  Returns data about all matching ENT surgical history resources.

* **URL**

  /tscharts/v1/entsurgicalhistory/

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
   [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "tubes": "left" | "right" | "both" | "none", "tubescomment": text, "tplasty":  "left" | "right" | "both" | "none", "tplastycomment": text, "eua":  "left" | "right" | "both" | "none", "euacomment": text, "fb":  "left" | "right" | "both" | "none", "fbcomment": text, "myringotomy":  "left" | "right" | "both" | "none", "myringotomycomment": text, "cerumen":  "left" | "right" | "both" | "none", "cerumencomment": text, "granuloma": "left" | "right" | "both" | "none", "granulomacomment": text, "septorhinoplasty":  true | false, "septorhinoplastycomment": text, "scarrevision":  true | false, "scarrevisioncomment": text, "frenulectomy":  true | false, "frenulectomycomment": text, "username" : text}, ...]

* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/entsurgicalhistory/?patient=3&clinic=15 HTTP/1.1
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
[{"id" : id, "clinic" : 15, "patient" : 29, "time" : "2017-12-11T01:02:24", "tubes": "left", "tubescomment": "", "tplasty": "none", "tplastycomment": "", "eua":  "none", "euacomment": "", "fb":  "left", "fbcomment": "", "myringotomy":  "both", "myringotomycomment": "", "cerumen":  "both", "cerumencomment": "", "granuloma": "none", "granulomacomment": "", "septorhinoplasty":  false, "septorhinoplastycomment": "", "scarrevision":  false, "scarrevisioncomment": "", "frenulectomy": false, "frenulectomycomment": "", "username" : "lebovits"}]
0
```
  
**Create an ENT Diagnosis Resource**
----
  Create an ENT surgical history resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/surgicalhistory/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `username` name of logged in user making this change <br />
   `tubes` one of the following: "left", "right", "both", "none"<br/>
   `tubescomment` text
   `tplasty` one of the following: "left", "right", "both", "none"<br/>
   `tplastycomment` text
   `eua` one of the following: "left", "right", "both", "none"<br/>
   `euacomment` text
   `fb` one of the following: "left", "right", "both", "none"<br/>
   `fbcomment` text
   `myringotomy` one of the following: "left", "right", "both", "none"<br/>
   `myringotomycomment` text
   `cerumen` one of the following: "left", "right", "both", "none"<br/>
   `cerumencomment` text
   `granuloma` one of the following: "left", "right", "both", "none"<br/>
   `granulomacomment` text
   `septorhinoplasty` one of the following: true, false<br/>
   `septorhinoplastycomment` text
   `scarrevision` one of the following: true, false<br/>
   `scarrevisioncomment` text
   `frenulectomy` one of the following: true, false<br/>
   `frenulectomycomment` text

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
POST /tscharts/v1/entsurgicalhistory/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101
{"clinic" : 14, "patient" : 29, "time" : "2017-12-11T01:02:24", "tubes": "left", "tubescomment": "", "tplasty": "none", "tplastycomment": "", "eua":  "none", "euacomment": "", "fb":  "left", "fbcomment": "", "myringotomy":  "both", "myringotomycomment": "", "cerumen":  "both", "cerumencomment": "", "granuloma": "none", "granulomacomment": "", "septorhinoplasty":  false, "septorhinoplastycomment": "", "scarrevision":  false, "scarrevisioncomment": "", "frenulectomy": false, "frenulectomycomment": "", "username" : "lebovits"}HTTP/1.0 200 OK
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
  Update an ENT surgical history instance

* **URL**

  /tscharts/v1/entsurgicalhistory/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

   `username` name of logged in user making this change <br />
   `tubes` one of the following: "left", "right", "both", "none"<br/>
   `tubescomment` text
   `tplasty` one of the following: "left", "right", "both", "none"<br/>
   `tplastycomment` text
   `eua` one of the following: "left", "right", "both", "none"<br/>
   `euacomment` text
   `fb` one of the following: "left", "right", "both", "none"<br/>
   `fbcomment` text
   `myringotomy` one of the following: "left", "right", "both", "none"<br/>
   `myringotomycomment` text
   `cerumen` one of the following: "left", "right", "both", "none"<br/>
   `cerumencomment` text
   `granuloma` one of the following: "left", "right", "both", "none"<br/>
   `granulomacomment` text
   `septorhinoplasty` one of the following: true, false<br/>
   `septorhinoplastycomment` text
   `scarrevision` one of the following: true, false<br/>
   `scarrevisioncomment` text
   `frenulectomy` one of the following: true, false<br/>
   `frenulectomycomment` text

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/entsurgicalhistory/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"septorhinoplasty": true}HTTP/1.0 200 OK
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
  Delete an ENT surgical history resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/entsurgicalhistory/id

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
DELETE /tscharts/v1/entsurgicalhistory/140/ HTTP/1.1
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

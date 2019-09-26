**Get ENT Exam**

----
  Returns json data about a single ENT exam resource. 

* **URL**

  /tscharts/v1/entexam/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "normal": "left" | "right" | "both" | "none", "microtia":  "left" | "right" | "both" | "none", "wax":  "left" | "right" | "both" | "none", "drainage":  "left" | "right" | "both" | "none", "externalOtitis":  "left" | "right" | "both" | "none", "fb":  "left" | "right" | "both" | "none", "tubeRight": "in place" | "extruding" | "in canal" | "none", "tubeLeft": "in place" | "extruding" | "in canal" | "none", "tympanoLeft": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tympanoRight": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tmGranulations":  "left" | "right" | "both" | "none", "tmRetraction":  "left" | "right" | "both" | "none", "tmAtelectasis":  "left" | "right" | "both" | "none", "perfLeft": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "perfRight": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "voiceTest" : "normal" | "abnormal" | "none", "forkAD": "a greater b" | "b greater a" | "a equal b" | "none", "forkAS": "a greater b" | "b greater a" | "a equal b" | "none", "bc": "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as", "fork": "256" | "512" | "none", "username" : text, "comment": text}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/entexam/12/ HTTP/1.1
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
{"id" : 27, "clinic" : 9, "patient" : 6, "time" : "2017-12-11T01:02:24", "normal": "left", "microtia":  "right", "wax":  "both", "drainage": "none", "externalOtitis": "both", "fb": "none", "tubeRight": "extruding", "tubeLeft": "none", "tympanoLeft": "anterior", "tympanoRight": "25 percent", "tmGranulations": "right", "tmRetraction": "none", "tmAtelectasis": "left", "perfLeft": "none", "perfRight": "marginal", "voiceTest" : "normal", "forkAD": "a greater b", "forkAS": "a greater b", "bc": "as lat as", "fork": "256", "username" : "a user", "comment": "some comment"}
```
  
**Get Multiple ENT Exams**
----
  Returns data about all matching ENT exam resources.

* **URL**

  /tscharts/v1/entexam/

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
   [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "normal": "left" | "right" | "both" | "none", "microtia":  "left" | "right" | "both" | "none", "wax":  "left" | "right" | "both" | "none", "drainage":  "left" | "right" | "both" | "none", "externalOtitis":  "left" | "right" | "both" | "none", "fb":  "left" | "right" | "both" | "none", "tubeRight": "in place" | "extruding" | "in canal" | "none", "tubeLeft": "in place" | "extruding" | "in canal" | "none", "tympanoLeft": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tympanoRight": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tmGranulations":  "left" | "right" | "both" | "none", "tmRetraction":  "left" | "right" | "both" | "none", "tmAtelectasis":  "left" | "right" | "both" | "none", "perfLeft": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "perfRight": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "voiceTest" : "normal" | "abnormal" | "none", "forkAD": "a greater b" | "b greater a" | "a equal b" | "none", "forkAS": "a greater b" | "b greater a" | "a equal b" | "none", "bc": "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as", "fork": "256" | "512" | "none", "username" : text, "comment": text}, ...]
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/entexam/?clinic=3 HTTP/1.1
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
[{"id" : 27, "clinic" : 9, "patient" : 6, "time" : "2017-12-11T01:02:24", "normal": "left", "microtia":  "right", "wax":  "both", "drainage": "none", "externalOtitis": "both", "fb": "none", "tubeRight": "extruding", "tubeLeft": "none", "tympanoLeft": "anterior", "tympanoRight": "25 percent", "tmGranulations": "right", "tmRetraction": "none", "tmAtelectasis": "left", "perfLeft": "none", "perfRight": "marginal", "voiceTest" : "normal", "forkAD": "a greater b", "forkAS": "a greater b", "bc": "as lat as", "fork": "256", "username" : "a user", "comment": "some comment"}]
0
```
  
**Create an ENT Exam**
----
  Create an ENT exam resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/entexam/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   'normal' one of the following:  "left" | "right" | "both" | "none" <br/>
   `microtia` one of the following:  "left" | "right" | "both" | "none"<br/>
   `wax` one of the following:  "left" | "right" | "both" | "none"<br/>
   `drainage` one of the following:  "left" | "right" | "both" | "none"<br/>
   `externalOtitis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `fb` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tubeRight` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tubeLeft` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tympanoLeft` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tympanoRight` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tmGranulations` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmRetraction` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmAtelectasis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `perfLeft` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `perfRight` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `voiceTest`  one of the following: "normal" | "abnormal" | "none"<br/>
   `forkAD` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `forkAS` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `bc` one of the following: "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as"<br/>
   `fork` one of the following: "256" | "512" | "none"<br/>
   `comment` comment supplied by the user for this exam item<br /><
   `username` name of logged in user making this change <br />

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
POST /tscharts/v1/entexam/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"clinic" : 9, "patient" : 6, "normal": "left", "microtia": "right", "wax": "both", "drainage": "none", "externalOtitis": "both", "fb": "none", "tubeRight": "extruding", "tubeLeft": "none", "tympanoLeft": "anterior", "tympanoRight": "25 percent", "tmGranulations": "right", "tmRetraction": "none", "tmAtelectasis": "left", "perfLeft": "none", "perfRight": "marginal", "voiceTest" : "normal", "forkAD": "a greater b", "forkAS": "a greater b", "bc": "as lat as", "fork": "256", "username" : "a user", "comment": "some comment"}HTTP/1.1 200 OK
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

**Update an ENT Exam**
----
  Update an ENT exam instance

* **URL**

  /tscharts/v1/entexam/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   'normal' one of the following:  "left" | "right" | "both" | "none" <br/>
   `microtia` one of the following:  "left" | "right" | "both" | "none"<br/>
   `wax` one of the following:  "left" | "right" | "both" | "none"<br/>
   `drainage` one of the following:  "left" | "right" | "both" | "none"<br/>
   `externalOtitis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `fb` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tubeRight` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tubeLeft` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tympanoLeft` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tympanoRight` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tmGranulations` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmRetraction` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmAtelectasis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `perfLeft` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `perfRight` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `voiceTest`  one of the following: "normal" | "abnormal" | "none"<br/>
   `forkAD` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `forkAS` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `bc` one of the following: "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as"<br/>
   `fork` one of the following: "256" | "512" | "none"<br/>
   `comment` comment supplied by the user for this exam item<br /><
   `username` name of logged in user making this change <br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/entexam/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"forkAS": "a greater b"}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete an ENT Exam**
----
  Delete an ENT exam resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/entexam/id

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
DELETE /tscharts/v1/entexam/140/ HTTP/1.1
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


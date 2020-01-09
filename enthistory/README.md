**Get ENT History**

----
  Returns json data about a single ENT history resource. 

* **URL**

  /tscharts/v1/enthistory/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, 
    "painDuration": "none" | "days" | "weeks" | "months" | "intermittent", 
    "painSide" : "right" | "left" | "both" | "none", 
    "hearingLossDuration": "none" | "days" | "weeks" | "months" | "intermittent", 
    "hearingLossSide" : "right" | "left" | "both" | "none", 
    "drainageDuration": "none" | "days" | "weeks" | "months" | "intermittent", 
    "drainageSide" : "right" | "left" | "both" | "none", 
    "username" : text, "comment": text}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/enthistory/12/ HTTP/1.1
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
{"id":27, 
 "painSide": "left", "painDuration": "days",
 "hearingLossSide": "left", "hearingLossDuration": "days",
 "drainageSide": "left", "drainageDuration": "days",
 "clinic": 9,"patient":6,"time":"2017-12-11T01:02:24","username":"xxyyzz","comment":"Some comment here"}

```
  
**Get Multiple ENT Histories**
----
  Returns data about all matching ENT history resources.

* **URL**

  /tscharts/v1/enthistory/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

   `patient` patient id<br />
   `clinic` clinic id<br />
   `painSide` "left", "right", "none", or "both"<br />
   `painDuration` "days", "weeks", "months", "none", or "intermittent"<br />
   `hearingLossSide` "left", "right", "none", or "both"<br />
   `hearingLossDuration` "days", "weeks", "months", "none", or "intermittent"<br />
   `drainageSide` "left", "right", "none", or "both"<br />
   `drainageDuration` "days", "weeks", "months", "none", or "intermittent"<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/enthistory/?clinic=3 HTTP/1.1
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
[{"id":27, 
 "painSide": "left", "painDuration": "days",
 "hearingLossSide": "left", "hearingLossDuration": "days",
 "drainageSide": "left", "drainageDuration": "days",
 "clinic": 9,"patient":6,"time":"2017-12-11T01:02:24","username":"xxyyzz","comment":"Some comment here"}, ...]
0
```
  
**Create an ENT History**
----
  Create an ENT history resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/enthistory/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `painSide` one of the following: "none", "left", "right", "both"<br />
   `painDuration` one of the following: "none", "days", "weeks", "months", "intermittent"<br />
   `drainageSide` one of the following: "none", "left", "right", "both"<br />
   `drainageDuration` one of the following: "none", "days", "weeks", "months", "intermittent"<br />
   `hearingLossSide` one of the following: "none", "left", "right", "both"<br />
   `hearingLossDuration` one of the following: "none", "days", "weeks", "months", "intermittent"<br />
   `comment` comment supplied by the user for this history item<br />
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
POST /tscharts/v1/enthistory/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"painSide": "left", "painDuration": "weeks", "drainageSide": "none", "drainageDuration" : "none", "hearingLossSide" : "none", "hearingLossDuration": "none","clinic":3,"patient":6,"username":"xxyyzz","comment":"Some comment here"}HTTP/1.1 200 OK
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

**Update an ENT History**
----
  Update an ENT history instance

* **URL**

  /tscharts/v1/enthistory/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

   `comment` optional comment supplied by the user for this history item<br />
   `username` name of logged in user making this change <br />
   `painSide` one of the following: "none", "left", "right", "both"<br />
   `painDuration` one of the following: "none", "days", "weeks", "months", "intermittent"<br />
   `drainageSide` one of the following: "none", "left", "right", "both"<br />
   `drainageDuration` one of the following: "none", "days", "weeks", "months", "intermittent"<br />
   `hearingLossSide` one of the following: "none", "left", "right", "both"<br />
   `hearingLossDuration` one of the following: "none", "days", "weeks", "months", "intermittent"<br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/enthistory/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"hearingLossDuration": "days"}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete an ENT History**
----
  Delete an ENT history resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/enthistory/id

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
DELETE /tscharts/v1/enthistory/140/ HTTP/1.1
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

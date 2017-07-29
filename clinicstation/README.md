**Get Clinic Station**
----
  Returns json data about a single clinicstation resource. 

* **URL**

  /tscharts/v1/clinicstation/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"name": string,"active":[true|false],"clinic":id,"awaytime":integer,"away":[true|false], "willreturn":UTC time string,"station":id,"id":id,"level":integer,"nextpatient":[id | null], "activepatient": [id | null]}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST
  * **Code:** 404 NOT FOUND
  * **Code:** 500 INTERNAL ERROR

* **Example:**

```
GET /tscharts/v1/clinicstation/1/ HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Sat, 29 Jul 2017 22:36:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


ac
{"name":"test1","level":1,"activepatient":null,"away":true,"nextpatient":null,"awaytime":30,"clinic":1,"station":1,"active":false,"willreturn":"2017-07-29T22:36:21","id":1}
0
```
  
**Get Multiple Clinic Stations**
----
  Returns data about all matching clinicstation resources.

* **URL**

  /tscharts/v1/clinicstation/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `clinic` clinic id<br />

   **Optional:**
 
   `away` true or false<br />
   `active` true or false<br />
   `level` integer<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"name":string,"awaytime":integer,"willreturn":UTC time string,"away":[true|false],"active":[true|false],"clinic":id,"station":id,"id":id,"level":integer, "activepatient": [null | id], "nextpatient": [null | id]}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/clinicstation/?clinic=3 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Sat, 29 Jul 2017 22:36:22 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


34b
[{"name":"Dental 1","level":1,"activepatient":null,"away":true,"nextpatient":null,"awaytime":30,"clinic":3,"station":3,"active":false,"willreturn":"2017-07-29T22:36:22","id":7},{"name":"Dental 2","level":1,"activepatient":null,"away":true,"nextpatient":null,"awaytime":30,"clinic":3,"station":4,"active":false,"willreturn":"2017-07-29T22:36:22","id":8},{"name":"Ortho 1","level":1,"activepatient":null,"away":true,"nextpatient":null,"awaytime":30,"clinic":3,"station":5,"active":false,"willreturn":"2017-07-29T22:36:22","id":9},{"name":"Ortho 2","level":1,"activepatient":null,"away":true,"nextpatient":null,"awaytime":30,"clinic":3,"station":6,"active":false,"willreturn":"2017-07-29T22:36:22","id":10},{"name":"ENT","level":1,"activepatient":null,"away":true,"nextpatient":null,"awaytime":30,"clinic":3,"station":7,"active":false,"willreturn":"2017-07-29T22:36:22","id":11}]
0
```
  
**Create Clinic Station**
----
  Create a clinicstation instance.

* **URL**

  /tscharts/v1/clinicstation/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `station` station resource id<br />
   `name` name (e.g., "Dental 1")<br />

   **Optional:**
 
   `activepatient` id of the currently active patient<br />
   `nextpatient` id of the next patient in the queue<br />
   `away` true if clinic station is away (i.e., station personnel are not present), else false (default is true)<br />
   `active` true if clinic station is active (i.e., a patient is currently being seen), else false (default is false)<br />
   `level` priority level. Default is 1.<br />
   `awaytime` length of time from when `away` is set to true until the clinic station is expected to become available once again for patients (by setting `away` to false). Default is 30 minutes.<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/clinicstation/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 48
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"name":"Dental 1", "active": false, "away":true, "clinic": 360, "station": 227}HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":21}
```

**Update Clinic Station**
----
  Update a clinicstation instance.

* **URL**

  /tscharts/v1/clinicstation/

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following is required. 
 
   `away` true if station is away (no personnel) else false. See `awaytime`<br />
   `activepatient` id of the currently active patient<br />
   `nextpatient` id of the next patient in the queue<br />
   `active` true if clinic station is actively servicing a patient, else false<br />
   `name` clinic station name.<br />
   `level` priority level. Default is 1.<br />
   `awaytime` whenever `away` is set to true, `awaytime` is used to calculate the UTC time at which the station is expected to reopen. By default, `awaytime` is 30 minutes. In GET requests, the expected return time is returned as a UTC time string as `willreturn` in the JSON payload.<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/clinicstation/30/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 33
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"active": false, "away":true, "awaytime": 15}HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:17 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete Clinic Station**
----
  Delete a clinicstation instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/clinicstation/id

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
DELETE /tscharts/v1/clinicstation/122/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 20:17:14 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```


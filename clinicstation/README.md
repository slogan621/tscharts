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
    **Content:** `{"name": string,"active":[true|false],"clinic":id,"awaytime":integer,"away":[true|false], "willreturn":UTC time string,"station":id,"id":id,"level":integer}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/clinicstation/21/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"name":"Dental 1","level":1,"awaytime":30,"clinic":360,"station":227,"away":true,"active":false,"willreturn":"2017-04-26T05:29:15Z","id":21}
```
  
**Get Multiple Clinic Stations**
----
  Returns data about all matching clinicstation resources.

* **URL**

  /tscharts/v1/clinicstation/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic id<br />

   **Optional:**
 
   `away` true or false<br />
   `active` true or false<br />
   `level` integer level number<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"name":string,"awaytime":integer,"willreturn":UTC time string,"away":[true|false],"active":[true|false],"clinic":id,"station":id,"id":id,"level":integer}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/clinicstation/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 32
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"active": false, "clinic": 362}HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:16 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[{"name":"Dental 1","level":1,"awaytime":30,"clinic":362,"station":229,"active":false,"away":true,"willreturn":"2017-04-26T05:29:16Z","id":25},{"name":"Dental 2","level":1,"awaytime":30,"clinic":362,"station":207,"active":false,"away":true,"willreturn":"2017-04-26T05:29:16Z","id":26},{"name":"Dental 3","level":1,"awaytime":30,"clinic":362,"station":208,"active":false,"away":true,"willreturn":"2017-04-26T05:29:16Z","id":27},{"name":"Dental 4","level":1,"awaytime":30,"clinic":362,"station":209,"active":false,"away":true,"willreturn":"2017-04-26T05:29:16Z","id":28},{"name":"Dental 5","level":1,"awaytime":30,"clinic":362,"station":210,"active":false,"away":true,"willreturn":"2017-04-26T05:29:16Z","id":29}]
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
   `name` name (e.g., "Dental 1"<br />

   **Optional:**
 
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


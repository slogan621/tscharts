**Get Xray**

  Returns json data about a single xray resource. 

* **URL**

  /tscharts/v1/xray/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "xray_type" : "full" | "anteriors_bitewings", "teeth" : bitmask}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/xray/12/ HTTP/1.1
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
{"xray_type":"full","teeth":234,"id":12,"patient":6,"clinic":11,"time":"2017-12-11T01:02:24"}
0
```
  
**Get Multiple Xrays**
----
  Returns data about all matching xray resources.

* **URL**

  /tscharts/v1/xray/

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
   [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "xray_type": "full" | "anteriors_bitewings", "teeth": bitmask}, ...]
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/xray/?clinic=3 HTTP/1.1
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
[{"xray_type":"full","teeth":234,"id":12,"patient":6,"clinic":3,"time":"2017-12-11T02:02:24"},{"xray_type":"full","teeth":234,"id":14,"patient":8,"clinic":3,"time":"2017-12-11T01:02:24"},{"xray_type":"full","teeth":234,"id":32,"patient":15,"clinic":3,"time":"2017-12-11T15:02:24"},{"xray_type":"full","teeth":234,"id":7,"patient":17,"clinic":3,"time":"2017-12-11T03:02:24"},{"xray_type":"full","teeth":234,"id":56,"patient":19,"clinic":3,"time":"2017-12-11T07:02:24"},{"xray_type":"full","teeth":234,"id":45,"patient":32,"clinic":3,"time":"2017-12-11T01:25:24"}]
0
```
  
**Create an Xray**
----
  Create an xray resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/xray/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `xray_type` "full" | "anteriors_bitewings"<br />
   `teeth` integer bitmask of which teeth were xrayed. Bit 0 == tooth 1, bit 1 == tooth 2, etc.<br />

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
POST /tscharts/v1/medicalhistory/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"xray_type":"full", "teeth":48421, "clinic": 2, "patient": 2}HTTP/1.1 200 OK
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

**Update an Xray**
----
  Update an xray resource

* **URL**

  /tscharts/v1/xray/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the field/value pairs below:

   `xray_type` "full" | "anteriors_bitewings"<br />
   `teeth` integer bitmask of which teeth were xrayed. Bit 0 == tooth 1, bit 1 == tooth 2, etc.<br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/xray/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"teeth": 23145}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete an Xray resource**
----
  Delete an xray resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/xray/id

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
DELETE /tscharts/v1/xray/140/ HTTP/1.1
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


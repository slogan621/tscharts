**Get Return To Clinic Resource**
----
  Returns json data about a single returntoclinic resource. The return value
  contains the month and year that the patient is expected to return and the
  station to which the patient has been requested to return. Multiple 
  returntoclinic resources can exist for the same patient.

* **URL**

  /tscharts/v1/returntoclinic/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"patient":id,"interval":number of months,"month":month number [1-12] of expected return,"clinic":id,"station":id,"year":year number of expected return,"id":id}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/returntoclinic/61/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 03:34:22 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"patient":24,"interval":3,"month":5,"clinic":22,"station":15,"year":2016,"id":61}
```
  
**Get Multiple Return To Clinic Resources**
----
  Returns ids of all matching returntoclinic resources.

* **URL**

  /tscharts/v1/returntoclinic/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   None
 

   **Optional:**
 
   One or more of the following can be used to filter the results. 

   `patient` patient id<br />
   `clinic` clinic id<br />
   `station` station id<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"id":id}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/returntoclinic/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 15
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"station": 17}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 03:34:24 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[{"id":63}]
```
  
**Create a Return To Clinic Resource**
----

* **URL**

  /tscharts/v1/returntoclinic/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `station` station resource id<br />
   `interval` number of months from date of `clinic` that `patient` is being asked to return to visit the specified `station`<br />

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
POST /tscharts/v1/returntoclinic/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 59
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"clinic": 22, "station": 15, "patient": 24, "interval": 3}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 03:34:22 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":61}
```

**Update a Return To Clinic Resource**
----
  Update a returntoclinic instance (check in/out the patient).

* **URL**

  /tscharts/v1/returntoclinic/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   `interval` number of months 

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/returntoclinic/68/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 15
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"interval": 6}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 03:34:25 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete a Return To Clinic Resource**
----
  Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/returntoclinic/id

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
DELETE /tscharts/v1/returntoclinic/140/ HTTP/1.1
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

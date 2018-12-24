**Get Return To ClinicStation Resource**
----
  Returns json data about a single returntoclinicstation resource. The return 
  value contains the ids of the clinicstation that the patient needs to
  return to, the id of the clinicstation making the request, the id of the
  clinic, and the id of the patient. It also contains the state of the 
  return, either created, or finished. 

* **URL**

  /tscharts/v1/returntoclinicstation/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"patient":id, "clinic":id,"requestclinicstation":id,"clinicstation":id,"state":"created|scheduled","created":date,"scheduled":date}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/returntoclinicstation/59/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Tue, 25 Apr 2017 02:18:08 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"patient":405,"clinic":340,"requestingclinicstation":203,"clinicstation",45,"state":"created","created": 12345678, "scheduled":0}
```
  
**Get Multiple Return To ClinicStation Resources**
----
  Returns ids of all matching returntoclinicstation resources.

* **URL**

  /tscharts/v1/returntoclinicstation/

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
   `clinicstation` clinic station id<br />
   `requestingclinicstation` requesting clinic station id<br />
   `state` "created" | "scheduled"<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"id":id}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/returntoclinicstation/ HTTP/1.1
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
  
**Create a Return To ClinicStation Resource**
----

* **URL**

  /tscharts/v1/returntoclinicstation/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `patient` patient id<br />
   `clinic` clinic id<br />
   `clinicstation` clinic station id<br />
   `requestingclinicstation` requesting clinic station id<br />

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
POST /tscharts/v1/returntoclinicstation/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 77
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"patient": 45, "clinic": 337, "clinicstation": 196, "requestingclinicstation": 402}HTTP/1.0 200 OK
Date: Tue, 25 Apr 2017 02:18:06 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":52}
```

**Update a Return To ClinicStation Resource**
----
  Update a returntoclinicstation instance 

* **URL**

  /tscharts/v1/returntoclinicstation/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following is required:

   `state` "scheduled" 

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/returntoclinicstation/59/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 44
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"state": "scheduled"}HTTP/1.0 200 OK
Date: Tue, 25 Apr 2017 02:18:08 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete a Return To ClinicStation Resource**
----
  Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/returntoclinicstation/id

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
DELETE /tscharts/v1/returntoclinicstation/140/ HTTP/1.1
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

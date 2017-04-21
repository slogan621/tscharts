**Get Registration**
----
  Returns json data about a single register resource. 

* **URL**

  /tscharts/v1/register/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"patient":id,"state":"Checked In"|"Checked Out","clinic":id,"id":id,"timein":UTC time string, "timeout":UTC time string}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/register/141/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:54 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"patient":356,"state":"Checked In","clinic":287,"timeout":"2017-04-21T05:52:49Z","timein":"2017-04-21T05:52:54Z","id":141}
```
  
**Get Multiple Clinic Stations**
----
  Returns data about all matching register resources.

* **URL**

  /tscharts/v1/register/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   None
 

   **Optional:**
 
   One or more of the following can be used to filter the results. For example
   to get a count of how many clinics a patient has registered for, search 
   by patient. Or to get the number of patients registered for a clinic, search
   by clinic. To find out how many patients have been checked out of a clinic,
   specify both clinic and state = "Checked Out".

   `patient` clinic id<br />
   `clinic` clinic id<br />
   `state` "Checked In" | "Checked Out", case sensitive<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"patient":id,"state":"Checked In"|"Checked Out","clinic":id,"id":id,"timein":UTC time string, "timeout":UTC time string}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/register/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 16
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"patient": 354}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:48 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[{"patient":354,"state":"Checked In","clinic":285,"timeout":"2017-04-21T05:52:48Z","timein":"2017-04-21T05:52:48Z","id":139},{"patient":354,"state":"Checked In","clinic":284,"timeout":"2017-04-21T05:52:48Z","timein":"2017-04-21T05:52:48Z","id":136},{"patient":354,"state":"Checked In","clinic":283,"timeout":"2017-04-21T05:52:48Z","timein":"2017-04-21T05:52:48Z","id":133}]
```
  
**Create a Registration**
----
  Register a patient for a clinic. Records the time of the registration 
  and sets the state of the register object to "Checked In".

* **URL**

  /tscharts/v1/register/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "id" : id }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/register/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 31
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"clinic": 281, "patient": 350}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:47 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":129}
```

**Update a Registration**
----
  Update a register instance (check in/out the patient).

* **URL**

  /tscharts/v1/register/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   `state` "Checked In" | "Checked Out", case sensitive.

   Note that a register object is created (using POST) with a default state of "Checked In", so it is typically only necessary to check out patients with this API.

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/register/140/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 23
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"state": "Checked In"}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:49 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete a Registration**
----
  Delete a registration. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/register/id

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
DELETE /tscharts/v1/register/140/ HTTP/1.1
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


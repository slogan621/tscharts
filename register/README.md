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
  
**Search for Registration Objects**
----
  Returns data about all matching register resources.

* **URL**

  /tscharts/v1/register/

* **Method:**

  `GET`
  
*  **URL Params**

One or more of the following can be specified to filter the search results.

   `clinic` id<br/>
   `patient` id<br/>

* **Data Params**

    None
 
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"patient":id,"state":"Checked In"|"Checked Out","clinic":id,"id":id,"timein":UTC time string, "timeout":UTC time string}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/register/?clinic=3 HTTP/1.1
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
User-Agent: Dalvik/2.1.0 (Linux; U; Android 5.1.1; Android SDK built for x86 Build/LMY48X)
Host: 192.168.0.122
Connection: Keep-Alive
Accept-Encoding: gzip

HTTP/1.1 200 OK
Date: Sun, 08 Aug 2021 08:17:42 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=83
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

18e8
[{"patient":88,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:18:20.594","timein":"2021-08-06T10:18:20.594","id":88},{"patient":89,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:18:25.112","timein":"2021-08-06T10:18:25.112","id":89},{"patient":90,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:18:33.669","timein":"2021-08-06T10:18:33.669","id":90},{"patient":91,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:18:34.710","timein":"2021-08-06T10:18:34.710","id":91},{"patient":92,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:18:47.180","timein":"2021-08-06T10:18:47.180","id":92},{"patient":93,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:19:08.500","timein":"2021-08-06T10:19:08.500","id":93},{"patient":94,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:19:13.595","timein":"2021-08-06T10:19:13.595","id":94},{"patient":135,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:19:27.516","timein":"2021-08-06T10:19:27.516","id":95},{"patient":95,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:19:35.650","timein":"2021-08-06T10:19:35.650","id":96},{"patient":96,"state":"Checked In","clinic":3,"timeout":"2021-08-06T10:19:44.704","timein":"2021-08-06T10:19:44.704","id":97}]
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
  * **Code:** 409 CONFLICT<br />
  * **Code:** 500 SERVER ERROR

Note: 409 Conflict means patient was already registered for a clinic

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


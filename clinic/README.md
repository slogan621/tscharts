**Get Clinic**
----
  Returns json data about a single clinic.

* **URL**

  /tscharts/v1/clinic/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12, start : "mm/dd/yyyy", end : "mm/dd/yyyy", "location" : "Ensenada" }`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/clinic/262/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6   Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.0 200 OK
Date: Mon, 17 Apr 2017 22:36:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: AcceptX-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS

{"start":"02/05/2016","end":"02/06/2016","id":262,"location":"Ensenada"}
```
  
**Get Multiple Clinic**
----
  Returns data about all known clinics.

* **URL**

  /tscharts/v1/clinic/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{ id : 12, start : "mm/dd/yyyy", end : "mm/dd/yyyy", "location" : "Ensenada" }, ...]`
 
* **Error Response:**

  * None

* **Example:**

```
GET /tscharts/v1/clinic/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.0 200 OK
Date: Mon, 17 Apr 2017 22:36:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS

[{"start":"02/05/2016","end":"02/06/2016","id":93,"location":"test1"},{"start":"02/05/2016","end":"02/06/2016","id":94,"location":"test2"},{"start":"02/05/2016","end":"02/06/2016","id":95,"location":"test3"}]
```
  
**Create Clinic**
----
  Create a clinic instance.

* **URL**

  /tscharts/v1/clinic/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `start` clinic start date, mm/dd/yyyy<br />
   `end` clinic end data, mm/dd/yyyy<br />
   `location` text describing clinic location, e.g., city


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/clinic/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 68
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{"start": "02/05/2016", "end": "02/06/2016", "location": "Ensenada"}HTTP/1.0 200 OK
Date: Mon, 17 Apr 2017 22:36:20 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS

{"id":261}
```
**Delete Clinic**
----
  Delete a clinic instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/clinic/id

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
DELETE /tscharts/v1/clinic/261/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.0 200 OK
Date: Mon, 17 Apr 2017 22:36:20 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS

{}
```

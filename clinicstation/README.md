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
    **Content:** `{"active":false,"clinic":268,"station":108,"id":122,"level":1}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/clinicstation/122/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 20:17:14 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"active":false,"clinic":268,"station":108,"id":122,"level":1}
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
 
   `active` true or false<br />
   `level` integer level number<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{{"active":false,"clinic":270,"station":105,"id":130,"level":1}}, ...]`
 
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


{"active": false, "clinic": 270}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 20:17:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[{"active":false,"clinic":270,"station":105,"id":130,"level":1},{"active":false,"clinic":270,"station":97,"id":129,"level":1},{"active":false,"clinic":270,"station":96,"id":128,"level":1},{"active":false,"clinic":270,"station":95,"id":127,"level":1},{"active":false,"clinic":270,"station":110,"id":126,"level":1}]
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

   **Optional:**
 
   `active` true if station is active at creation, else false (default)<br />
   `level` priority level. Default is 1.<br />

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


{"active": false, "clinic": 268, "station": 108}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 20:17:14 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":122}
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

   One of the following is required. Both can be specified.
 
   `active` true if station is active at creation, else false<br />
   `level` priority level. Default is 1.<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/clinicstation/131/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 17
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"active": false}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 20:17:15 GMT
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


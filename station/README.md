**Get Station**
----
  Returns json data about a station. 

* **URL**

  /tscharts/v1/station/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "id" : integer, "name" : string, "level" : integer}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/station/99/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 00:12:56 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":99,"name":"ENT", "level": 2}
```
  
**Get Multiple Stations**
----
  Returns data about all known stations.

* **URL**

  /tscharts/v1/station/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"id": integer, "name" : string, "level": integer}, ...]`
 
* **Error Response:**

  * None

* **Example:**

```
GET /tscharts/v1/station/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 00:12:56 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[{"id":99,"name":"ENT", "level":1},{"id":95,"name":"Dental", "level":1},{"id":96,"name":"Ortho", "level":1},{"id":97,"name":"Screening", "level":1},{"id":100,"name":"test1", "level":1},{"id":101,"name":"test2", "level":1},{"id":102,"name":"test3", "level":1}]
```
  
**Create Station**
----
  Create a station instance. Stations are rarely created, since they are 
  mostly static for a physical clinic. To create instances of a station
  that are operational at a specific clinic, use clinicstation.

* **URL**

  /tscharts/v1/station/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `name` name of the station<br />

   **Optional:**

   `level` integer level of station. Higher number means higher priority when scheduling patients (e.g., if Dental is 1, and X-Ray is 2, patient will be sent to X-Ray before Dental<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/station/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 15
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"name": "ENT"}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 00:12:56 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":99}
```
**Delete Station**
----
  Delete a station instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/station/id

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
DELETE /tscharts/v1/station/104/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 00:12:56 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

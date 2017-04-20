**Get Image**
----
  Returns json data about a single image resource. 

* **URL**

  /tscharts/v1/image/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"patient":id,"data":"base64","clinic":id,"station":id,"type":"Headshot|Xray|Surgery","id":id}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/image/63/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Wed, 19 Apr 2017 01:53:04 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS


{"patient":343,"data":"ABCDEFG","clinic":276,"station":117,"type":"Headshot","id":63}
```
  
**Get Multiple Images**
----
  Returns a vector of image ids matching supplied search parameters.

* **URL**

  /tscharts/v1/image/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   None 

   **Optional:**
 
   `type` case-sensitive string, one of  "Headshot", "Surgery", or "Xray"<br />
   `clinic` clinic id<br />
   `station` station id<br />
   `patient` patient id<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[id, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/image/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 36
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"station": 119, "type": "Headshot"}HTTP/1.0 200 OK
Date: Wed, 19 Apr 2017 01:53:12 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS


[109,108,107,106,105,89,88,87,86,85,69,68,67,66,65]
```
  
**Create Image**
----
  Create a image instance.

* **URL**

  /tscharts/v1/image/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   `type` case-sensitive string, one of  "Headshot", "Surgery", or "Xray"<br />
   `clinic` clinic id<br />
   `station` station id<br />
   `patient` patient id<br />
   `data` base64 image data<br />

Note that clinic and station are both available in a clinicstation object.

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/image/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 86
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"type": "Headshot", "clinic": 276, "station": 117, "patient": 343, "data": "ABCDEFG"}HTTP/1.0 200 OK
Date: Wed, 19 Apr 2017 01:53:04 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS


{"id":63}
```

**Delete Image**
----
  Delete an image instance. 

* **URL**

  /tscharts/v1/image/id

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
DELETE /tscharts/v1/image/122/ HTTP/1.1
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


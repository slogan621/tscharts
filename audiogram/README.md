**Get Audiogram Resource**
----
  Returns json data about a single audiogram resource. The return value
  contains the clinic, patient, audiogram image id, and text comments 
  for the specified audiogram id.

* **URL**

  /tscharts/v1/audiogram/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"patient":id,"comment":string,"clinic":id,"image":id,"id":id}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/audiogram/59/ HTTP/1.1
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


{"comment":"A test comment","patient":405,"clinic":340,"image":203,"id":59}
```
  
**Get Multiple Audiogram Resources**
----
  Returns all matching audiogram resources.

* **URL**

  /tscharts/v1/audiogram/

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
   `image` image id<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"comment":text,"patient":id,"clinic":id,"image":id,"id":id},...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/audiogram/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 15
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 03:34:24 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[{"comment":"comment 1","patient":100,"clinic":5,"image":43,"id":7},{"comment":"comment 2","patient":73,"clinic":14,"image":56,"id":5},{"comment":"comment 3","patient":44,"clinic":12,"image":94,"id":8},{"comment":"comment 4","patient":18,"clinic":12,"image":6,"id":83}]
```
  
**Create a Audiogram Resource**
----

* **URL**

  /tscharts/v1/audiogram/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `image` image resource id<br />
   `comment` string<br />

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
POST /tscharts/v1/audiogram/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 77
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"comment": "", "clinic": 337, "image": 196, "patient": 402}HTTP/1.0 200 OK
Date: Tue, 25 Apr 2017 02:18:06 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":52}
```

**Update a Audiogram Resource**
----
  Update a audiogram instance 

* **URL**

  /tscharts/v1/audiogram/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following is required:

   `comment` text comment

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/audiogram/59/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 44
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"comment": "A test comment"}HTTP/1.0 200 OK
Date: Tue, 25 Apr 2017 02:18:08 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete a Audiogram Resource**
----
  Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/audiogram/id

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
DELETE /tscharts/v1/audiogram/140/ HTTP/1.1
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

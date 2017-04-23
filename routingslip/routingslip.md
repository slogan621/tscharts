**Get Routing Slip Resource**
----
  Returns json data about a single routing slip resource. Includes all 
  associated routingslipentry and routingslipcomment resources associated
  with the routingslip.

* **URL**

  /tscharts/v1/routingslip/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"category":"New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other" | "Unknown","patient":id,"comments":[id, id, id, ...],"clinic":id,"routing":[id, id, id,...],"id":id}`

* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/routingslip/26693/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 04:13:28 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"category":"New Cleft","patient":32,"comments":[],"clinic":47,"routing":[],"id":26693}
```
  
**Get Multiple Routing Slip Resources**
----
  Returns all matching routingslip resources. 
  None: return format based on search parameters. See below for details.

* **URL**

  /tscharts/v1/routingslip/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following must be used to filter the results. 

   `patient` patient id. If specified with a clinic, a single routing slip is returned. Otherwise, all routing slips for the patient are returned in an array.<br />
   `clinic` clinic id. If specified alone, routing slips for all patients are returned for the clinic. If specified with patient, then a single routing slip is returned. <br />

   **Optional:**

    None
 
* **Success Response:**

  * **Code:** 200 <br />
    **Content (patient & clinic):** `{"category":"New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other" | "Unknown","patient":id,"comments":[id, id, id, ...],"clinic":id,"routing":[id, id, id,...],"id":id}`
    **Content (patient | clinic):** `[{"category":"New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other" | "Unknown","patient":id,"comments":[id, id, id, ...],"clinic":id,"routing":[id, id, id,...],"id":id}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Examples:**

```
GET /tscharts/v1/routingslip/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 31
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"clinic": 428, "patient": 594}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 06:57:11 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"category":"New Cleft","patient":594,"comments":[],"clinic":428,"routing":[788,787,784,785,786],"id":32041}
```
  
```
GET /tscharts/v1/routingslip/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 15
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"clinic": 426}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 06:57:02 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[{"category":"New Cleft","patient":131,"comments":[],"clinic":426,"routing":[],"id":32039},{"category":"New Cleft","patient":130,"comments":[],"clinic":426,"routing":[],"id":32038}, ...]
```

**Create a Routing Slip Resource**
----

* **URL**

  /tscharts/v1/routingslip/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br/>
   `patient` patient resource id<br/>
   `category` string one of "New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other" | "Unknown"<br/>

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
POST /tscharts/v1/routingslip/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 54
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"category": "New Cleft", "clinic": 47, "patient": 32}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 04:13:24 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":26693}
```

**Update a Routing Slip Resource**
----
  Update a routingslip instance.

* **URL**

  /tscharts/v1/routingslip/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   `category` string one of "New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other" | "Unknown"<br/>

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/routingslip/32040/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 21
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"category": "Ortho"}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 06:57:08 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete a Routing Slip Resource**
----
  Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/routingslip/id

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
DELETE /tscharts/v1/routingslip/140/ HTTP/1.1
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

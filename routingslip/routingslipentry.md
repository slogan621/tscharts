**Get Routing Slip Entry Resource**
----
  Returns json data about a single routing slip resource. 

* **URL**

  /tscharts/v1/routingslipentry/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"order":integer [1-n],"state":"Scheduled" | "Checked In" | "Checked Out" | "Removed","routingslip":id,"id":id,"clinicstation":id}`

* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/routingslipentry/811/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 21:15:22 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"order":1,"state":"Checked In","routingslip":32479,"id":811,"clinicstation":353}
```
  
**Get Multiple Routing Slip Entry Resources**
----
  Returns all matching routingslipentry resources. 
  None: return format based on search parameters. See below for details.

* **URL**

  /tscharts/v1/routingslipentry/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following must be used to filter the results. Depending
   on what is passed, either a routingslip object or an array of routingslip
   object ids is returned.

   `routingslip` routingslip id. If specified with a clinicstation, a single routing slip entry is returned. Otherwise, all routing slip entries for the routing slip are returned in an array.<br />
   `clinicstation` clinicstation id. If specified alone, routing slips entires for all patients are returned for the clinicstation. If specified with routingslip, then a single routing slip entry is returned. <br />

   **Optional:**

    None
 
* **Success Response:**

  * **Code:** 200 <br />
    **Content (patient & clinic):** `[id, id, id, ...]`<br>
    **Content:** `{"order":integer [1-n],"state":"Scheduled" | "Checked In" | "Checked Out" | "Removed","routingslip":id,"id":id,"clinicstation":id}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Examples:**

```
GET /tscharts/v1/routingslipentry/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 22
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"routingslip": 32478}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 21:15:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


[810,809,806,807,808]
```
  
**Create a Routing Slip Entry Resource**
----

* **URL**

  /tscharts/v1/routingslipentry/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `routingslip` routingslip resource id<br/>
   `clinicstation` clinicstation resource id<br/>

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
POST /tscharts/v1/routingslipentry/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 44
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"routingslip": 32475, "clinicstation": 342}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 21:15:18 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":801}
```

**Update a Routing Slip Entry Resource**
----
  Update a routingslipentry instance.

* **URL**

  /tscharts/v1/routingslipentry/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One of the following is required. If both are missing, a bad request is returned.

   `order` integer - the order of this item in the set of routing slip entries for the specified routingslip
   `state` string, one of "Scheduled" | "Checked In" | "Checked Out" | "Removed" <br/>

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/routingslipentry/811/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 23
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"state": "Spaced Out"}HTTP/1.0 400 Bad Request
Date: Sun, 23 Apr 2017 21:15:22 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: text/html; charset=utf-8
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
```

**Delete a Routing Slip Entry Resource**
----
  Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/routingslipentry/id

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
DELETE /tscharts/v1/routingslipentry/140/ HTTP/1.1
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

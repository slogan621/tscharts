**Get Routing Slip Entry Resource**
----
  Returns json data about a single routing slip entry resource. 

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
    **Content:** `{"order":integer [1-n],"state":"New" | "Scheduled" | "Checked In" | "Checked Out" | "Removed" | "Deleted","Return","routingslip":id,"id":id,"station":id, "returntoclinicstation": id}`

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


{"order":1,"state":"Checked In","routingslip":32479,"id":811,"station":353, "returntoclinicstation": null}
```
  
**Get Multiple Routing Slip Entry Resources**
----
  Returns a list of all matching routing slip entry resources. 

* **URL**

  /tscharts/v1/routingslipentry/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following must be used to filter the results. 

   `routingslip` routingslip id. 
   `station` station id. 
   `returntoclinicstation` returntoclinicstation id. 
   `nullrcs` if "true" return only entries with a NULL returntoclinicstation field. If "false" return only non-NULL entries.<br />
   `states` return entries matching the specified states. Comma-separated list consisting of one or more of the following states: "New", "Scheduled", "Checked In", "Checked Out", "Return", "Removed", and "Deleted"<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content (patient & clinic):** `[id, id, id, ...]`<br>
    **Content:** `[{"order":integer [1-n],"state":"New" | "Scheduled" | "Checked In" | "Checked Out" | "Removed" | "Deleted" | "Return","routingslip":id,"id":id,"station":id, "returntoclinicstation": id}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Examples:**

```
GET /tscharts/v1/routingslipentry/?routingslip=853 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.1 200 OK
Date: Sun, 22 Oct 2017 05:38:29 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json

10
[43,42,39,40,41]
0
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
   `station` station resource id<br/>

   **Optional:**

   `returntoclinicstation` return to clinic station resource id. If specified, object state will be set to "Return"<br/>

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


{"routingslip": 32475, "station": 342}HTTP/1.0 200 OK
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

   `order` integer - the order of this item in the set of routing slip entries for the specified routingslip<br/>
   `returntoclinicstation` integer - id of a returntoclinicstation record<br/>
   `state` string, one of "New" | "Scheduled" | "Checked In" | "Checked Out" | "Removed" | "Deleted". Note that state "Return" can only be set at creation time. <br/>

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

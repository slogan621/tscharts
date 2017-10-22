**Get Routing Slip Comment Resource**
----
  Returns json data about a single routing slip comment resource. 

* **URL**

  /tscharts/v1/routingslipcomment/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"comment":string,"updatetime":UTC date time string,"routingslip":id,"id":id,"author":id}`

* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/routingslipcomment/4148/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 21:15:11 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS


{"comment":"Comment 0","updatetime":"2017-04-23T21:15:09Z","routingslip":32471,"id":4148,"author":6}
```
  
**Get Multiple Routing Slip Comment Resources**
----
  Returns all matching routingslipcomment resources. 

* **URL**

  /tscharts/v1/routingslipcomment/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   `routingslip` routingslip id.<br/> 

* **Data Params**

    None
 
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[id, id, id, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Examples:**

```
GET /tscharts/v1/routingslipcomment/?routingslip=846 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Sun, 22 Oct 2017 05:38:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


191
[335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,334,333,332,331,330,329,328,327,326,325,324,323,322,321,320,315,316,317,318,319,413,414]
0
```
  
**Create a Routing Slip Comment Resource**
----

* **URL**

  /tscharts/v1/routingslipcomment/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `routingslip` routingslip resource id<br/>
   `author` user id<br/>
   `comment` string<br/>

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
POST /tscharts/v1/routingslipcomment/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 65
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"comment": "Have a nice day", "routingslip": 32472, "author": 6}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 21:15:16 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS


{"id":4248}
```

**Delete a Routing Slip Comment Resource**
----

* **URL**

  /tscharts/v1/routingslipcomment/id

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
DELETE /tscharts/v1/routingslipcomment/140/ HTTP/1.1
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

**Get Routing Slip Comment Resource**
----
  Returns json data about a single routing slip comment resource. 

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

  /tscharts/v1/routingslipentry/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   `routingslip` routingslip id.<br/> 

   **Optional:**

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
GET /tscharts/v1/routingslipcomment/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 22
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"routingslip": 32471}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 21:15:11 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS


[4247,4246,4148,4149,4150,4151,4152,4153,4154,4155,4156,4157,4158,4159,4160,4161,4162,4163,4164,4165,4166,4167,4168,4169,4170,4171,4172,4173,4174,4175,4176,4177,4178,4179,4180,4181,4182,4183,4184,4185,4186,4187,4188,4189,4190,4191,4192,4193,4194,4195,4196,4197,4198,4199,4200,4201,4202,4203,4204,4205,4206,4207,4208,4209,4210,4211,4212,4213,4214,4215,4216,4217,4218,4219,4220,4221,4222,4223,4224,4225,4226,4227,4228,4229,4230,4231,4232,4233,4234,4235,4236,4237,4238,4239,4240,4241,4242,4243,4244,4245]
```
  
**Create a Routing Slip Comment Resource**
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

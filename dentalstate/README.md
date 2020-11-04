**Get Dental State**

----
  Returns json data about a single dental state resource. A dental state resource records
  a tooth, a corresponding CDT code, and its state (treated | untreated), along with comments
  and the id of the patient and clinic for which this data corresponds. An altcode field is 
  used in case there is no matching cdt code in the system for the condition or treatment done.
  

* **URL**

  /tscharts/v1/dentalstate/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

  Response is a JSON object with the following fields:

  "id" : id<br />
  "clinic" : id <br />
  "patient" : id <br />
  "tooth" : integer tooth number (9999 if not related to a specific tooth) <br />
  "code" : id <br />
  "username" : string <br />
  "state" : treated | untreated | none | other<br />
  "time" : last modified datetime string for record<br />
  "comment" : text<br />

* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/dentalstate/2/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Wed, 04 Nov 2020 02:28:46 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

88
{"username":"username","comment":"q","code":1,"patient":1,"state":"other","tooth":15,"clinic":1,"time":"2020-11-03T18:28:46.905","id":2}
0
```
  
**Get Multiple Dental States**
----
  Returns data for all matching dental state resources. 

* **URL**

  /tscharts/v1/dentalstate/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

  "clinic" : id <br />
  "patient" : id <br />
  "tooth" : integer tooth number (9999 if not related to a specific tooth) <br />
  "code" : id <br />
  "state" : treated | untreated | none | other<br />
  "time" : last modified datetime string for record<br />
  "username" : text string<br />
  "comment" : text<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

  "id" : id <br />
  "clinic" : id <br />
  "patient" : id <br />
  "tooth" : integer tooth number (9999 if not related to a specific tooth) <br />
  "code" : id <br />
  "state" : treated | untreated | none | other<br />
  "time" : last modified datetime string for record<br />
  "username" : text string<br />
  "comment" : text<br />

* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/dentalstate/?tooth=15 HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Wed, 04 Nov 2020 02:28:47 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

8e
[{"username":"username","comment":"9","code":1,"patient":1,"state":"untreated","tooth":15,"clinic":1,"time":"2020-11-03T18:28:47.081","id":9}]
0
```
  
**Create a Dental State**
----
  Create a dental state resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/dentalstate/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
  "clinic" : id <br />
  "patient" : id <br />
  "tooth" : integer tooth number (9999 if not related to a specific tooth) <br />
  "username" : string <br />
  "code" : id <br />
  "state" : treated | untreated | none | other<br />
  "comment" : text<br />

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
POST /tscharts/v1/dentalstate/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 112

{"username": "Gomez", "comment": "z", "code": 1, "patient": 1, "clinic": 1, "tooth": -931, "state": "untreated"}HTTP/1.1 200 OK
Date: Wed, 04 Nov 2020 02:28:46 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

8
{"id":1}
0
```

**Update a Dental State**
----
  Update a dental state instance

* **URL**

  /tscharts/v1/dentalstate/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

  "tooth" : integer tooth number (9999 if not related to a specific tooth) <br />
  "code" : id <br />
  "username" : string<br />
  "state" : treated | untreated | none | other<br />
  "comment" : text<br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/dentalstate/30/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 74

{"username": "username", "comment": "x", "state": "treated", "tooth": 980}HTTP/1.1 200 OK
Date: Wed, 04 Nov 2020 02:28:48 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

2
{}
0
```

**Delete a Dental State**
----
  Delete a dental state resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/dentalstate/id

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
DELETE /tscharts/v1/dentalstate/1/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Wed, 04 Nov 2020 02:28:46 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

2
{}
0
```


**Get Surgery Yype by ID**
----
  Returns json data about a single surgery type resource. 

* **URL**

  /tscharts/v1/surgerytype/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":id,"name":string}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/surgerytype/20/ HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Tue, 02 Jan 2018 05:52:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 24
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{"id":20,"name":"ANTHROSCOPY"}
```
  
**Get Multiple Surgery Types**
----
  Returns the entire list of surgery types.

* **URL**

  /tscharts/v1/surgerytype/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   None 

   **Optional:**

   None

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[name1, name2, name3, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/surgerytype/ HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Tue, 26 Dec 2017 20:40:58 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 16
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json


["ARTHROSCOPY","CIRCUMCISION","CAESAREAN"]

```

**Get Surgery type by Name**
----
  Returns json data about a single surgery type resource. 

* **URL**

  /tscharts/v1/surgerytype/?name=string

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   `name` string

   **Optional:**

   None

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":id,"name":string}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/surgerytype/?name=ANTHROSCOPY HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Tue, 26 Dec 2017 20:40:58 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 30
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{"id":188,"name":"ANTHROSCOPY"}

```
  
**Create a Surgery Type**
----
  Create a surgery type instance.

* **URL**

  /tscharts/v1/surgerytype/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `name` string

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR
  `Entering a surgery type that already exists in the system returns a BAD REQUEST error response.
* **Example:**

```
POST /tscharts/v1/surgerytype/ HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
Content-Length: 17

{"name": "ARTHROSCOPY"}HTTP/1.1 200 OK
Date: Tue, 26 Dec 2017 20:40:57 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 10
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{"id":187}
```


**Delete a Surgery type**
----
  Delete a surgery type instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/surgerytype/id

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
DELETE /tscharts/v1/surgerytype/187/ HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Tue, 26 Dec 2017 20:40:58 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 2
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{}
```

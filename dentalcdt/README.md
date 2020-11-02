**Get Dental CDT Code by ID**
----
  Returns json data about a single dental CDT code resource. 

* **URL**

  /tscharts/v1/dentalcdt/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":id,"code":string, "desc":string}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/dentalcdt/185/ HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Tue, 26 Dec 2017 20:40:56 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 25
Allow: GET, POST, DELETE, HEAD, OPTIONS

{"id":185,"code":"D0220","desc":"Intraoral-periapical first radiographic image"}
```
  
**Get Multiple Dental CDT Codes**
----
  Returns multiple CDT Dental Codes.

* **URL**

  /tscharts/v1/dentalcdt/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   None 

   One or more of the following can be specified to filter the search results.

   `code` string<br/>
   `desc` string<br/>

   If no filters are supplied, the entire list of CDT codes is returned.

   **Optional:**

   None

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"id" : 1, "code": "DO220", "desc":"Intraoral-periapical first radiographic image"}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/dentalcdt/ HTTP/1.1
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


[{"id" : 1, "code": "DO220", "desc":"Intraoral-periapical first radiographic image"}, {"id" : 2, "code": "D0230", "desc": "Intraoral-periapical each addition radiographic image"}]`

```

**Create a Dental CDT Code**
----
  Create a Dental CDT code instance.

* **URL**

  /tscharts/v1/dentalcdt/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `code` string<br/>
   `desc` string<br/>

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR
  `Entering a cdt code that already exists in the database returns a 400 BAD REQUEST error response.
* **Example:**

```
POST /tscharts/v1/dentalcdt/ HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
Content-Length: 17

{"code": "D1320", "desc":"Tobacco counseling for control and prevention of oral disease"}HTTP/1.1 200 OK
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

**Delete a CDT Code**
----
  Delete a cdt code instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/dentalcdt/id

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
DELETE /tscharts/v1/dentalcdt/187/ HTTP/1.1
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

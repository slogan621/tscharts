**Get Consent Information by consent ID**
----
  Returns json data about a single consent information resource. 

* **URL**

  /tscharts/v1/consent/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"registration":id,"patient":id,"clinic":id,"general_consent":true|false,"photo_consent":true|false}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/consent/51/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:54 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"registration":125,"clinic":10,"patient":20,"general_consent":true,"photo_consent":false,"id":51}
```
**Get Consent Information by Registration ID**
----
  Returns json data about a single consent information resource. 

* **URL**

  /tscharts/v1/consent/

* **Method:**

  `GET`
  
*  **URL Params**

    **Required**

    `registration` registration id<br />

    **Optional:**
 
    None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"registration":id,"clinic":id,"patient":id,"general_consent":true|false,"photo_consent":true|false}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**
```
GET /tscharts/v1/consent/?registration=28 HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token c418abb265c76faa251c53c7dd152ecf768920f1
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 22 Jun 2018 04:43:42 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 67
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{"general_consent":true,"registration":28,"clinic":30,"patient":5,"id":33,"photo_consent":true}
```
**Get Multiple consent Information**
----
  Returns json data about all matching consent information resources. 

* **URL**

  /tscharts/v1/consent/

* **Method:**

  `GET`
  
*  **URL Params**

    **Required**

    `clinic` clinic id<br />

    **Optional:**
 
    `registration` registration id<br />
    `patient` patient id<br />

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"registration":id,"general_consent":true|false,"photo_consent":true|false}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**
```
GET /tscharts/v1/consent/?clinic=5 HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token c418abb265c76faa251c53c7dd152ecf768920f1
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 22 Jun 2018 04:43:42 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 67
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

[{"general_consent":true,"registration":28,"patient":10,"clinic":5,"id":33,"photo_consent":true},{"general_consent":false, "registration":30,"patient":11,"clinic":5,"id":6,"photo_consent":true}]
```

**Create Consent Information**
----
  Record consent information get from patients.

* **URL**

  /tscharts/v1/consent/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   `registration` registration resource id <br />
   `patient` patient resource id <br />
   `clinic` clinic resource id <br />
   `general_consent` [true|false] whether the patient gives consent to the registration form <br />
   `photo_consent` [true|false] whether the patient gives consent to photograph usage <br />

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "id" : id }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR
  
  `Creating a consent information that has the same registration id as one that already exists in the database returns a BAD REQUEST response.` 
  `Creating a consent information that has clinic id or patient id that doesn't match with the registration returns a BAD REQUEST response.`

* **Example:**

```
POST /tscharts/v1/consent/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 31
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"registration": 1, "patient":3, "clinic": 5, "general_consent": true, "photo_consent": false}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:47 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":141}
```

**Delete a Consent Information**
----
  Delete a consent information. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/consent/id

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

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
DELETE /tscharts/v1/consent/140/ HTTP/1.1
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


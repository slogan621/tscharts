**Get Consent Information**
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
    **Content:** `{"register":id,"general_consent":true|false,"photo_consent":true|false}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

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


{"register":125,"general_consent":true,"photo_consent":false,"id":51}
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
   `register` registration resource id <br />
   `general_consent` [true|false] whether the patient gives consent to the registration form <br />
   `photo_consent` [true|false] whether the patient gives consent to photograph usage <br />

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "id" : id }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

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


{"register": 1, "general_consent": true, "photo_consent": false}HTTP/1.0 200 OK
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

  * **Code:** 404 NOT FOUND

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


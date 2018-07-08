**Get Consent Resource by ID**
----
  Returns json data about a single consent resource. 

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
  
`Attempting to get a consent resource using a consent id that doesn't exist returns a NotFound Error`
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
**Search for Consent Resources**
----
  Return one or more consent resources based on search terms

* **URL**

  /tscharts/v1/consent/

* **Method:**

  `GET`
  
*  **URL Params**

    **Required:**

    See discusson below
 
    **Optional:**

    `clinic` clinic id <br/>
    `patient` patient id <br/>
    `registration` registration id <br/>

The following are valid usages of this API:

GET /tscharts/v1/consent?patient=id - return an array of consents that match the patient <br/>
GET /tscharts/v1/consent?clinic=id - return an array of consents that match the clinic <br/>
GET /tscharts/v1/consent?registration=id - return an array containing a single consent (will only be one found for a registration) <br/>
GET /tscharts/v1/consent?patient=id&clinic=id - return an array containing a single consent resource (will be for the specified patient and clinic) <br/>
GET /tscharts/v1/consent?patient=id&registration=id - return an array containing a single consent resource (will be for the specified patient and registration) <br/>
GET /tscharts/v1/consent?clinic=id&registration=id - return an array containing a single consent resource (will be for the specified clinic and registration) <br/>
GET /tscharts/v1/consent?clinic=id&patient=id&registration=id - return an array containing a single consent resource (will be for the specified clinic and registration) <br/>
 
* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content (array of resources):** `[{"registration":id,"clinic":id,"patient":id,"general_consent":true|false,"photo_consent":true|false}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

`Attempting to get a consent resource with registrationid/patientid/clinicid that doesn't exist returns a notFound error.`

`Attempting to get a consent resource without any URL parameters returns a badRequest error.`

`Getting a consent resource with registrationid/patientid/clinicid that exists but no consent record corresponds to it returns an empty array.`

* **Example1:**
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

[{"general_consent":true,"registration":28,"clinic":30,"patient":5,"id":33,"photo_consent":true}]
```

* **Example2:**
```
GET /tscharts/v1/consent/?registration=36&patient=33 HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token a1c3bd0728e2fc8e0ce83cbbdad016ed4b55ae80
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Thu, 28 Jun 2018 05:06:07 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 97
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

[{"patient":33,"photo_consent":true,"general_consent":false,"clinic":27,"registration":36,"id":37}]

GET /tscharts/v1/consent/?registration=35&clinic=27 HTTP/1.1
Host: 54.193.67.202
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.18.4
Content-Type: application/json
Authorization: Token a1c3bd0728e2fc8e0ce83cbbdad016ed4b55ae80
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Thu, 28 Jun 2018 05:06:07 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 97
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

[{"patient":32,"photo_consent":false,"general_consent":true,"clinic":27,"registration":35,"id":36}]
```
* **Example3:**
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

GET /tscharts/v1/consent/?patient=6 HTTP/1.1
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

[{"general_consent":true,"registration":28,"patient":6,"clinic":5,"id":33,"photo_consent":true},{"general_consent":false, "registration":30,"patient":11,"clinic":7,"id":6,"photo_consent":true}]
```
**Create a Consent Resource**
----
  Create a consent resource using data obtained from a patient at registration.

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
   `general_consent` [true|false] whether the patient gave consent for care at registration time <br />
   `photo_consent` [true|false] whether the patient gives consent for photograph usage at time of registration <br />

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "id" : id }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR
  
  `Attempting to create a consent resource that has the same registration id as one that already exists in the database returns a BadRequest error.` 
  
  `Attempting to create a consent resource that has clinic id or patient id that doesn't match with the registration returns a BadRequest error.`
  
  `Attempting to create a consent resource with missing fields returns a BadRequest error.`
  
  `Attempting to create a consent resource with patient id, clinic id, or registration id that couldn't be found returns a BadRequest error.`

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

**Delete a Consent Resource**
----
  Delete a consent resource. Use is not recommended except for unit test applications.

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



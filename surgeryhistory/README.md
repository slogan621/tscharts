**Get Surgery History**
----
  Returns json data about a single surgeryhistory resource. 

* **URL**

  /tscharts/v1/surgeryhistory/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id": id,"patient":id,"surgery": id,"surgeryyear":integer,"surgerymonth":integer,"surgerylocation": string, "anesthesia_problems":[true|false], "bleeding_problems":[true|false]}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST
  * **Code:** 404 NOT FOUND
  * **Code:** 500 INTERNAL ERROR

* **Example:**

```
GET /tscharts/v1/surgeryhistory/1/ HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Sat, 29 Jul 2017 22:36:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


{"id":3,"patient":1,"surgery":1,"surgeryyear":1999,"surgerymonth":12,"surgerylocation":place1,"anesthesia_problems":true,"bleeding_problems":false}
```
  
**Get Multiple Surgery Histories**
----
  Returns data about all matching surgeryhistory resources.

* **URL**

  /tscharts/v1/surgeryhistory/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
    One or more of the followings are used to filter the result. 
   
   `patient` patient id<br />
   `surgery` surgery id<br />
   
   The result is represented by a JSON array.
 
* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"id":id,"patient":id,"surgery": id,"surgeryyear":integer,"surgerymonth":integer,"surgerylocation": string, "anesthesia_problems":[true|false], "bleeding_problems":[true|false]},...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/surgeryhistory/?patient=5 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Sat, 29 Jul 2017 22:36:22 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


[{"id":3,"patient":5,"surgery":1,"surgeryyear":1999,"surgerymonth":12,"surgerylocation":place1,"anesthesia_problems":true,"bleeding_problems":false}, {"id":6,"patient":5,"surgery":2,"surgeryyear":2005,"surgerymonth":5,"surgerylocation":place2,"anesthesia_problems":false,"bleeding_problems":true}]
```
  
**Create Surgery History**
----
  Create a surgeryhistory instance.

* **URL**

  /tscharts/v1/surgeryhistory/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `patient` patient id<br />
   `surgery` surgery id<br />
   `surgeryyear` integer legal year<br />
   `surgerymonth` integer legal month<br />
   `surgerylocation` string the location where the surgery performed<br />
   `anesthesia_problems` [true|false] whether the patient has problems with the anesthesia<br />
   `bleeding_problems` [true|false] whether the patient has bleeding problems<br />

   **Optional:**
 
   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":id}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR


  A BAD REQUEST ERROR can occur if the data parameter value is not valid. For example, give a surgeryyear that is greater than the current year, or give a surgerymonth that is greater than 12. It can also occur if the parameter name is not valid. The parameter names that are valid are "patient","surgery","surgeryyear","surgerymonth","surgerylocation","anethesia_problems" and "bleeding_problems".

  A NOT FOUND ERROR can occur if the patient id or surgery id cannot be found in the database.

* **Example:**

```
POST /tscharts/v1/surgeryhistory/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 48
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"patient":5,"surgery":1,"surgeryyear":1999,"surgerymonth":12,"surgerylocation":place1,"anesthesia_problems":true,"bleeding_problems":false}HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":12}
```

**Update Surgery History**
----
  Update a surgeryhistory instance.

* **URL**

  /tscharts/v1/surgeryhistory/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following is required. 
 
   `surgery` the surgery id<br />
   `surgeryyear` legal year<br />
   `surgerymonth` legal month<br />
   `surgerylocation` the location where the surgery performed string<br />
   `anesthesia_problems` [true|false] whether the patient has problems with the anesthesia<br />
   `bleeding_problems` [true|false] whether the patient has bleeding problems<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** None
 
* **Error Response:**
  
  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR
  

  A BAD REQUEST ERROR can occur if the data parameter if not valid. For example, surgeryyear and surgerymonth to update are not legal, or the surgery to update cannot be found in the database. It can also occur if the parameter name is not valid. The parameter names that are valid are "surgery","surgeryyear","surgerymonth","surgerylocation","anethesia_problems" and "bleeding_problems". "patient" cannot be updated here.

  A NOT FOUND ERROR can occur if the id  cannot be found.

* **Example:**

```
PUT /tscharts/v1/surgeryhistory/30/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 33
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"surgeryyear": 2012, "surgerymonth":8}HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:17 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete Surgery History**
----
  Delete a surgeryhistory instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/surgeryhistory/id

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
DELETE /tscharts/v1/surgeryhistory/200/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 20:17:14 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```


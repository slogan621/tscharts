**Get State Change**
----
  Returns json data about a single statechange resource. 

* **URL**

  /tscharts/v1/statechange/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"state":"in" | "out","time":UTC time string, "patient":id, "clinicstation":id}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/statechange/119/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 15:33:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"state":"in","time":"2017-04-21T15:33:15Z","patient":363,"id":119,"clinicstation":139}
```
  
**Get Multiple State Changes**
----
  Returns data about all matching state change resources.

* **URL**

  /tscharts/v1/statechange/

* **Method:**

  `GET`
  
*  **Data Params**

   None

* **URL Params**

   **Required:**

   None
 

   **Optional:**
 
   One or more of the following can be used to filter the results. 

   `patient` patient id<br />
   `clinic` clinic id<br />
   `clinicstation` clinicstation id<br />

    The following combinations are legal, others result in a 400 error:

    * patient & clinicstation
    * patient & clinic
    * clinicstation
    * clinic

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"state":"in" | "out","time":UTC time string,"patient":id,"id":id,"clinicstation":id}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/statechange?patient=378&clinicstation=157 HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 0
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 23:22:19 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, DELETE, HEAD, OPTIONS


[{"state":"in","time":"2017-04-21T23:22:19Z","patient":378,"id":140,"clinicstation":157}]
```
  
**Create a State Change Resource**
----
  Create a state change object. One such object is created for each state
  change that occurs (check in or check out from a clinicstation). Combined
  with a register resource, statechange resources provide a history of the
  patient as he or she flows through one of the clinics.

* **URL**

  /tscharts/v1/statechange/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinicstation` clinicstation resource id<br />
   `patient` patient resource id<br />
   `state` 'in' or 'out', case-sensitive<br />

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
POST /tscharts/v1/statechange/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 53
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"state": "in", "patient": 363, "clinicstation": 139}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 15:33:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":119}
```

**Delete a State Change**
----
  Delete a state change resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/statechange/id

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
DELETE /tscharts/v1/statechange/119/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 15:33:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```


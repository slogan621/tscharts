**Get Patient**
----
  Returns json data about a single patient resource. 

* **URL**

  /tscharts/v1/patient/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"city":string,"colonia":string,"suffix":string,"dob":"mm/dd/YYYY,"gender":"Female"|"Male","maternal_last":string,"phone1":string,"state":URF-8 Mexican state name,"email":string,"middle":string,"prefix":string,"emergencyphone":string,"emergencyfullname":string,"emergencyemail":string,"street1":string,"street2":string,"paternal_last":string,"phone2":string,"id":integer,"curp":string,"first":string, "oldid":string}

    Note that unspecified values are represented by the empty string "". Also note that no validation was performed on phone number or e-mail address formats at the time the data was stored by the database.
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/patient/27/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae

{}HTTP/1.0 200 OK
Date: Sat, 29 Apr 2017 20:36:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS

{"city":"Ensenada","colonia":"","suffix":"Jr.","dob":"04/01/1962","gender":"Female","maternal_last":"yyyyyy","phone1":"1-111-111-1111","state":"Baja California","email":"patient@example.com","middle":"","prefix":"","emergencyphone":"1-222-222-2222","emergencyfullname":"Maria Sanchez","emergencyemail":"maria.sanchez@example.com","street1":"1234 First Ave","street2":"","paternal_last":"abcd1234","phone2":"","id":27,"curp":"abcdefg","first":"zzzzzzz", "oldid": ""}
```
  
**Get Multiple Patients**
----
  Returns all matching patient resources.

* **URL**

  /tscharts/v1/patient/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   None 

   **Optional:**

   One or more of the following can be specified to filter the search results.
 
   `paternal_last` string<br/>
   `maternal_last` string<br/>
   `first` string<br/>
   `dob` date string mm/dd/YYYY<br/>
   `gender` "Female" | "Male"<br/>
   `name` string<br/>
   `curp` string<br/>
   `oldid` string<br/>
   `clinic` integer clinic ID that patient must have been registered for<br/>

   If name is specified, all other search terms are ignored, and name is
   used to search for a match against each of paternal_last, maternal_last, 
   and first. If any one (or more) match, that patient is returned. curp 
   corresponds to CURP, a national ID assigned to each person in Mexico and a 
   required part of their medical records. oldid is used as a cross-reference
   to the patient in a previous system/database.

   Note that all name searches are case insensitive.

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[id, id, id, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/patient/?paternal_last=test5 HTTP/1.1
Host: 192.168.0.110
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Mon, 24 Jul 2017 03:51:58 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


4
[11]
0

```
  
**Create Patient**
----
  Create a patient instance.

* **URL**

  /tscharts/v1/patient/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   In the following, all fields with no value are specified with an empty string, i.e., "", except for `state`, `gender`, and `dob`, which must have a valid value.
 
   `paternal_last` string<br/>
   `maternal_last` string<br/>
   `first` string<br/>
   `middle` string<br/>
   `suffix` string<br/>
   `prefix` string<br/>
   `street1` string<br/>
   `street2` string <br/>
   `colonia` string <br/>
   `city` string<br/>
   `state` UTF-8 Mexican state name.<br/>
   `dob` date string mm/dd/YYYY<br/>
   `gender` "Female" | "Male"<br/>
   `phone1` string <br/>
   `phone2` string <br/>
   `email` string<br/>
   `emergencyfullname` string<br/>
   `emergencyphone` string<br/>
   `emergencyemail` string<br/>
   `curp` string<br/>

   **Optional:**

   `oldid` string<br/>

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/patient/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 464
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae

{"city": "Ensenada", "colonia": "", "suffix": "Jr.", "dob": "04/01/1962", "gender": "Female", "maternal_last": "yyyyyy", "phone1": "1-111-111-1111", "state": "Baja California", "email": "patient@example.com", "middle": "", "prefix": "", "emergencyphone": "1-222-222-2222", "emergencyfullname": "Maria Sanchez", "emergencyemail": "maria.sanchez@example.com", "street1": "1234 First Ave", "paternal_last": "abcd1234", "phone2": "", "street2": "", "first": "zzzzzzz", "curp": "45ju4"}HTTP/1.0 200 OK
Date: Sat, 29 Apr 2017 20:36:20 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS

{"id":27}
```

**Update Patient**
----
  Update a patient instance.

* **URL**

  /tscharts/v1/patient/

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One of the following is required. 
 
   `paternal_last` string<br/>
   `maternal_last` string<br/>
   `first` string<br/>
   `middle` string<br/>
   `suffix` string<br/>
   `prefix` string<br/>
   `street1` string<br/>
   `street2` string <br/>
   `colonia` string <br/>
   `city` string<br/>
   `state` UTF-8 Mexican state name.<br/>
   `dob` date string mm/dd/YYYY<br/>
   `gender` "Female" | "Male"<br/>
   `phone1` string <br/>
   `phone2` string <br/>
   `email` string<br/>
   `emergencyfullname` string<br/>
   `emergencyphone` string<br/>
   `emergencyemail` string<br/>
   `curp` string<br/>
   `oldid` string<br/>

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** None
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/patient/39/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 461
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae

{"city": "Ensenada", "colonia": "", "suffix": "Jr.", "dob": "04/01/1962", "gender": "Male", "maternal_last": "yyyyyy", "phone1": "1-111-111-1111", "state": "Baja California", "email": "patient@example.com", "middle": "", "prefix": "", "emergencyphone": "1-222-222-2222", "emergencyfullname": "Maria Sanchez", "emergencyemail": "maria.sanchez@example.com", "street1": "1234 First Ave", "paternal_last": "abcdefg", "phone2": "", "street2": "", "first": "zzzzzzz", "curp": "1234"}HTTP/1.0 200 OK
Date: Sat, 29 Apr 2017 20:36:22 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS

{}
```

**Delete Patient**
----
  Delete a patient instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/patient/id

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
DELETE /tscharts/v1/patient/122/ HTTP/1.1
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

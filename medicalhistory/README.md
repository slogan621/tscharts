**Get Medical History**

In the following, content returned by GET (both forms), and accepted as
request data for both PUT and POST will be identify by the string "MEDICAL_HISTORY_DATA, which consists of the following:

   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `tuberculosis` true | false<br/>
   `pregnancy_duration` integer</br>
   `epilepsy` true | false<br/>
   `recentcold` true | false<br/>
   `pain` true | false<br/>
   `pregnancy_complications` true | false<br/>
   `allergymeds` string <br/>
   `cancer` true | false<br/>
   `relative_cleft` true | false<br/>
   `meds` string<br/>
   `parents_cleft` true | false<br/>
   `athsma` true | false<br/>
   `mother_alcohol` true | false<br/>
   `troublespeaking` true | false<br/>
   `diabetes` true | false<br/>
   `congenitalheartdefect` true | false<br/>
   `pregnancy_smoke` true | false<br/>
   `troublehearing` true | false<br/>
   `troubleeating` true | false<br/> 
   `birth_complications` true | false<br/>
   `hivaids` true | false<br/>
   `hepititis` true | false<br/>
   `siblings_cleft` true | false<br/>
   `anemia` true | false<br/>
   `hemophilia` true | false<br/>

----
  Returns json data about a single medicalhistory resource. 

* **URL**

  /tscharts/v1/medicalhistory/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, `MEDICAL_HISTORY_DATA`}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/medicalhistory/13/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:19 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"hepititis":false,"cancer":false,"epilepsy":false,"clinic":12,"recentcold":false,"pain":false,"pregnancy_complications":false,"id":13,"allergymeds":"","pregnancy_duration":9,"relative_cleft":false,"meds":"","athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":14,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"parents_cleft":false,"siblings_cleft":false,"diabetes":false,"hemophilia":false,"time":"2017-04-23T01:19:19Z"}
```
  
**Get Multiple Medical Histories**
----
  Returns data about all matching medicalhistory resources.

* **URL**

  /tscharts/v1/medicalhistory/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

   `patient` patient id<br />
   `clinic` clinic id<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
   [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, `MEDICAL_HISTORY_DATA`}, ...]
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/medicalhistory/?clinic=15 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.1 200 OK
Date: Thu, 07 Dec 2017 03:20:43 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json

6e8
[{"hepititis":false,"cancer":false,"epilepsy":false,"clinic":15,"recentcold":false,"pain":false,"pregnancy_complications":false,"id":27,"allergymeds":"","pregnancy_duration":9,"relative_cleft":false,"meds":"","athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":15,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"parents_cleft":false,"siblings_cleft":false,"diabetes":false,"hemophilia":false,"time":"2017-12-07T03:20:43"},{"hepititis":false,"cancer":false,"epilepsy":false,"clinic":15,"recentcold":false,"pain":false,"pregnancy_complications":false,"id":28,"allergymeds":"","pregnancy_duration":9,"relative_cleft":false,"meds":"","athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":16,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"parents_cleft":false,"siblings_cleft":false,"diabetes":false,"hemophilia":false,"time":"2017-12-07T03:20:43"},{"hepititis":false,"cancer":false,"epilepsy":false,"clinic":15,"recentcold":false,"pain":false,"pregnancy_complications":false,"id":29,"allergymeds":"","pregnancy_duration":9,"relative_cleft":false,"meds":"","athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":17,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"parents_cleft":false,"siblings_cleft":false,"diabetes":false,"hemophilia":false,"time":"2017-12-07T03:20:43"}]
0
```
  
**Create a Medical History**
----
  Create a medical history resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/medicalhistory/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `MEDICAL_HISTORY_DATA`

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
POST /tscharts/v1/medicalhistory/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 606
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"tuberculosis": false, "pregnancy_duration": 9, "epilepsy": false, "clinic": 12, "recentcold": false, "pain": false, "pregnancy_complications": false, "allergymeds": "", "cancer": false, "relative_cleft": false, "meds": "", "parents_cleft": false, "athsma": false, "mother_alcohol": false, "troublespeaking": false, "diabetes": false, "congenitalheartdefect": false, "pregnancy_smoke": false, "troublehearing": false, "patient": 14, "troubleeating": false, "birth_complications": false, "hivaids": false, "hepititis": false, "siblings_cleft": false, "anemia": false, "hemophilia": false}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:19 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":13}
```

**Update a Medical History**
----
  Update a medicalhistory instance

* **URL**

  /tscharts/v1/medicalhistory/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the field/value pairs in `MEDICAL_HISTORY_DATA`

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/medicalhistory/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"relative_cleft": true}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete a Medical History**
----
  Delete a registration. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/medicalhistory/id

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
DELETE /tscharts/v1/medicalhistory/140/ HTTP/1.1
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


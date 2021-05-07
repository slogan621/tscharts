**Get Vaccine**

In the following, content returned by GET (both forms), and accepted as
request data for both PUT and POST will be identified by the following 
strings. Each virus has a name field, and a date field. The name of the
date field is the name of the vaccine concatenated with the string _date.
For sake of brevity, in the remainder of this document, VACCINE_DATA 
is used to represent the following:

   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `covid19` COVID-19<br />
   `covid19_doses` 0, 1 or 2<br />
   `covid_date` <br />
   `covid19_booster` COVID-19 booster<br />
   `covid19_booster_date` <br />
   `dtap` Diphtheria, tetanus, and acellular pertussis vaccine <br />
   `dtap_date` <br />
   `dt` Diphtheria, tetanus vaccine<br />
   `dt_date` <br />
   `hib` Haemophilus influenzae type B vaccine<br />
   `hib_date`<br />
   `hepa` Hepatitis A vaccine<br />
   `hepa_date` <br />
   `hepb` Hepatitis B vaccine<br />
   `hepb_date` <br />
   `hpv` Human papillomavirus vaccine<br />
   `hpv_date` <br />
   `iiv` Influenza vaccine (inactivated)<br />
   `iiv_date` <br />
   `laiv4` Influenza vaccine (live, attenuated)<br />
   `laiv4_date` <br />
   `mmr` Measles, mumps, and rubella vaccine<br />
   `mmr_date` <br />
   `menacwy` Meningococcal serogroups A, C, W, Y vaccine<br />
   `menacwy_date` <br />
   `menb` Meningococcal serogroup B vaccine<br />
   `menb_date` <br />
   `pcv13` Pneumococcal 13-valent conjugate vaccine<br />
   `pcv13_date` <br />
   `ppsv23` Pneumococcal 23-valent polysaccharide vaccine<br />
   `ppsv23_date` <br />
   `ipv` Poliovirus vaccine (inactivated)<br />
   `ipv_date` <br />
   `rv` Rotavirus vaccine<br />
   `rv_date` <br />
   `tap` Tetanus, diphtheria, and acellular pertussis vaccine<br />
   `tap_date` <br />
   `td` Tetanus and diphtheria vaccine<br />
   `td_date` <br />
   `var` Varicella vaccine<br />
   `var_date`<br />
   `dtap_hepb_ipv` DTaP, hepatitis B, and inactivated poliovirus vaccine<br />
   `dtap_hepb_ipv_date` <br />
   `dtap_ipv_hib` DTaP, inactivated poliovirus, and Haemophilus influenzae type B vaccine<br />
   `dtap_ipv_hib_date` <br />
   `dtap_ipv` DTaP and inactivated poliovirus vaccine<br />
   `dtap_ipv_date` <br />
   `dtap_ipv_hib_hepb` DTaP, inactivated poliovirus, Haemophilus influenzae type b, and hepatitis B vaccine<br />
   `dtap_ipv_hib_hepb_date` <br />
   `mmvr` Measles, mumps, rubella, and varicella vaccines<br />
   `mmvr_date` <br />

----
  Returns json data about a single vaccine resource. 

* **URL**

  /tscharts/v1/vaccine/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, `VACCINE_DATA`}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/vaccine/12/ HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json

2c5
{"first_walk":13,"birth_weight_metric":true, "height_metric":true, "weight_metric":true, "hepititis":true,"bleeding_problems":false,"first_crawl":8,"epilepsy":false,"clinic":6,"pregnancy_complications":false,"pregnancy_duration":8,"congenitalheartdefect_planforcare":false,"allergymeds":"","cancer":false,"first_sit":7,"relative_cleft":false,"id":12,"meds":"","parents_cleft":true,"athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":6,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"siblings_cleft":true,"diabetes":false,"cold_cough_fever":false,"congenitalheartdefect_workup":false,"first_words":11,"time":"2017-12-11T01:02:24"}
0
```
  
**Get Multiple Medical Histories**
----
  Returns data about all matching vaccine resources.

* **URL**

  /tscharts/v1/vaccine/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

   `patient` patient id<br />
   `clinic` clinic id<br />

   If both patient and clinic are specified, and the result of the query 
   is a single object (which should be the case), then it is returned as
   a JSON object. Otherwise, the result is returned as a JSON array.

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
   [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, `VACCINE_DATA`}, ...]
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/vaccine/?clinic=3 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


859
[{"birth_weight_metric":true, "height_metric":true, "weight_metric":true, "first_walk":13,"hepititis":false,"bleeding_problems":false,"first_crawl":8,"epilepsy":false,"clinic":3,"pregnancy_complications":false,"pregnancy_duration":9,"congenitalheartdefect_planforcare":false,"allergymeds":"","cancer":false,"first_sit":7,"relative_cleft":false,"id":3,"meds":"","parents_cleft":false,"athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":3,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"siblings_cleft":false,"diabetes":false,"cold_cough_fever":false,"congenitalheartdefect_workup":false,"first_words":11,"time":"2017-12-11T01:02:24"},{"birth_weight_metric":true, "height_metric":true, "weight_metric":true, "first_walk":13,"hepititis":false,"bleeding_problems":false,"first_crawl":8,"epilepsy":false,"clinic":3,"pregnancy_complications":false,"pregnancy_duration":9,"congenitalheartdefect_planforcare":false,"allergymeds":"","cancer":false,"first_sit":7,"relative_cleft":false,"id":4,"meds":"","parents_cleft":false,"athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":4,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"siblings_cleft":false,"diabetes":false,"cold_cough_fever":false,"congenitalheartdefect_workup":false,"first_words":11,"time":"2017-12-11T01:02:24"},{"birth_weight_metric":true, "height_metric":true, "weight_metric":true, "first_walk":13,"hepititis":false,"bleeding_problems":false,"first_crawl":8,"epilepsy":false,"clinic":3,"pregnancy_complications":false,"pregnancy_duration":9,"congenitalheartdefect_planforcare":false,"allergymeds":"","cancer":false,"first_sit":7,"relative_cleft":false,"id":5,"meds":"","parents_cleft":false,"athsma":false,"mother_alcohol":false,"troublespeaking":false,"anemia":false,"congenitalheartdefect":false,"pregnancy_smoke":false,"troublehearing":false,"patient":5,"troubleeating":false,"birth_complications":false,"hivaids":false,"tuberculosis":false,"siblings_cleft":false,"diabetes":false,"cold_cough_fever":false,"congenitalheartdefect_workup":false,"first_words":11,"time":"2017-12-11T01:02:24"}]
0
```
  
**Create a Vaccine**
----
  Create a vaccine resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/vaccine/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `VACCINE_DATA`

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
POST /tscharts/v1/vaccine/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"birth_weight_metric":true, "height_metric":true, "weight_metric":true, "first_walk": 13, "tuberculosis": false, "pregnancy_duration": 9, "troublehearing": false, "epilepsy": false, "clinic": 2, "pregnancy_complications": false, "congenitalheartdefect_planforcare": false, "allergymeds": "", "bleeding_problems": false, "first_sit": 7, "relative_cleft": false, "meds": "", "parents_cleft": false, "athsma": false, "siblings_cleft": false, "mother_alcohol": false, "troublespeaking": false, "diabetes": false, "congenitalheartdefect": false, "pregnancy_smoke": false, "first_crawl": 8, "patient": 2, "troubleeating": false, "birth_complications": false, "hivaids": false, "hepititis": false, "cancer": false, "anemia": false, "cold_cough_fever": false, "congenitalheartdefect_workup": false, "first_words": 11}HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:23 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


8
{"id":2}
0
```

**Update a Vaccine**
----
  Update a vaccine instance

* **URL**

  /tscharts/v1/vaccine/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the field/value pairs in `VACCINE_DATA`

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/vaccine/24/ HTTP/1.1
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

**Delete a Vaccine**
----
  Delete a vaccine resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/vaccine/id

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
DELETE /tscharts/v1/vaccine/140/ HTTP/1.1
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


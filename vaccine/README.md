**Get Vaccine**

In the following, content returned by GET (both forms), and accepted as
request data for both PUT and POST will be identified by the following 
strings. Each vaccination has a name field, and a date field. The name of the
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
GET /tscharts/v1/vaccine/3/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 07 May 2021 04:44:29 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

481
{"ppsv23_date":"01/01/1915","tap":"false","hib_date":"01/01/1905","dtap_ipv_hib_hepb_date":"01/01/1924","dtap_date":"01/01/1903","dtap":"true","clinic":3,"iiv_date":"01/01/1909","ipv":"false","mmvr":"true","hepb_date":"01/01/1907","menb_date":"01/01/1913","id":3,"hepa_date":"01/01/1906","rv":"true","pcv13_date":"01/01/1914","hpv":"false","covid19":"true","var_date":"01/01/1920","var":"false","dt_date":"01/01/1904","td":"true","rv_date":"01/01/1917","menb":"true","hpv_date":"01/01/1908","pcv13":"false","iiv":"true","patient":3,"covid19_doses":1,"dtap_ipv_hib_hepb":"false","mmr":"true","hepa":"false","hib":"true","hepb":"true","ipv_date":"01/01/1916","dtap_ipv_hib_date":"01/01/1922","dtap_ipv_date":"01/01/1923","dt":"false","laiv4":"false","mmvr_date":"01/01/1925","covid19_booster_date":"01/01/1902","dtap_ipv":"true","tap_date":"01/01/1918","mmr_date":"01/01/1911","ppsv23":"true","td_date":"01/01/1919","dtap_hepb_ipv_date":"01/01/1921","menacwy":"false","covid19_date":"01/01/1901","dtap_ipv_hib":"false","dtap_hepb_ipv":"true","time":"2021-05-06T21:44:29.949","laiv4_date":"01/01/1910","covid19_booster":"false","menacwy_date":"01/01/1912"}
0
```
  
**Get Multiple Vaccines**
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
GET /tscharts/v1/vaccine/?patient=11 HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 07 May 2021 15:43:42 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

d8f
[{"ppsv23_date":"01/01/1915","tap":"false","hib_date":"01/01/1905","dtap_ipv_hib_hepb_date":"01/01/1924","dtap_date":"01/01/1903","dtap":"true","clinic":11,"iiv_date":"01/01/1909","ipv":"false","mmvr":"true","hepb_date":"01/01/1907","menb_date":"01/01/1913","id":23,"hepa_date":"01/01/1906","rv":"true","pcv13_date":"01/01/1914","hpv":"false","covid19":"true","var_date":"01/01/1920","var":"false","dt_date":"01/01/1904","td":"true","rv_date":"01/01/1917","menb":"true","hpv_date":"01/01/1908","pcv13":"false","iiv":"true","patient":11,"covid19_doses":1,"dtap_ipv_hib_hepb":"false","mmr":"true","hepa":"false","hib":"true","hepb":"true","ipv_date":"01/01/1916","dtap_ipv_hib_date":"01/01/1922","dtap_ipv_date":"01/01/1923","dt":"false","laiv4":"false","mmvr_date":"01/01/1925","covid19_booster_date":"01/01/1902","dtap_ipv":"true","tap_date":"01/01/1918","mmr_date":"01/01/1911","ppsv23":"true","td_date":"01/01/1919","dtap_hepb_ipv_date":"01/01/1921","menacwy":"false","covid19_date":"01/01/1901","dtap_ipv_hib":"false","dtap_hepb_ipv":"true","time":"2021-05-07T08:43:42.432","laiv4_date":"01/01/1910","covid19_booster":"false","menacwy_date":"01/01/1912"},{"ppsv23_date":"01/01/1915","tap":"false","hib_date":"01/01/1905","dtap_ipv_hib_hepb_date":"01/01/1924","dtap_date":"01/01/1903","dtap":"true","clinic":10,"iiv_date":"01/01/1909","ipv":"false","mmvr":"true","hepb_date":"01/01/1907","menb_date":"01/01/1913","id":20,"hepa_date":"01/01/1906","rv":"true","pcv13_date":"01/01/1914","hpv":"false","covid19":"true","var_date":"01/01/1920","var":"false","dt_date":"01/01/1904","td":"true","rv_date":"01/01/1917","menb":"true","hpv_date":"01/01/1908","pcv13":"false","iiv":"true","patient":11,"covid19_doses":1,"dtap_ipv_hib_hepb":"false","mmr":"true","hepa":"false","hib":"true","hepb":"true","ipv_date":"01/01/1916","dtap_ipv_hib_date":"01/01/1922","dtap_ipv_date":"01/01/1923","dt":"false","laiv4":"false","mmvr_date":"01/01/1925","covid19_booster_date":"01/01/1902","dtap_ipv":"true","tap_date":"01/01/1918","mmr_date":"01/01/1911","ppsv23":"true","td_date":"01/01/1919","dtap_hepb_ipv_date":"01/01/1921","menacwy":"false","covid19_date":"01/01/1901","dtap_ipv_hib":"false","dtap_hepb_ipv":"true","time":"2021-05-07T08:43:42.394","laiv4_date":"01/01/1910","covid19_booster":"false","menacwy_date":"01/01/1912"},{"ppsv23_date":"01/01/1915","tap":"false","hib_date":"01/01/1905","dtap_ipv_hib_hepb_date":"01/01/1924","dtap_date":"01/01/1903","dtap":"true","clinic":9,"iiv_date":"01/01/1909","ipv":"false","mmvr":"true","hepb_date":"01/01/1907","menb_date":"01/01/1913","id":17,"hepa_date":"01/01/1906","rv":"true","pcv13_date":"01/01/1914","hpv":"false","covid19":"true","var_date":"01/01/1920","var":"false","dt_date":"01/01/1904","td":"true","rv_date":"01/01/1917","menb":"true","hpv_date":"01/01/1908","pcv13":"false","iiv":"true","patient":11,"covid19_doses":1,"dtap_ipv_hib_hepb":"false","mmr":"true","hepa":"false","hib":"true","hepb":"true","ipv_date":"01/01/1916","dtap_ipv_hib_date":"01/01/1922","dtap_ipv_date":"01/01/1923","dt":"false","laiv4":"false","mmvr_date":"01/01/1925","covid19_booster_date":"01/01/1902","dtap_ipv":"true","tap_date":"01/01/1918","mmr_date":"01/01/1911","ppsv23":"true","td_date":"01/01/1919","dtap_hepb_ipv_date":"01/01/1921","menacwy":"false","covid19_date":"01/01/1901","dtap_ipv_hib":"false","dtap_hepb_ipv":"true","time":"2021-05-07T08:43:42.358","laiv4_date":"01/01/1910","covid19_booster":"false","menacwy_date":"01/01/1912"}]
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
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 1218

{"ppsv23_date": "01/01/1915", "tap": "false", "hib_date": "01/01/1905", "menb_date": "01/01/1913", "dtap": "true", "clinic": 3, "iiv_date": "01/01/1909", "ipv": "false", "covid19": "true", "hepb_date": "01/01/1907", "dtap_ipv_hib_hepb_date": "01/01/1924", "hepa_date": "01/01/1906", "rv": "true", "pcv13_date": "01/01/1914", "hpv": "false", "mmvr": "true", "var_date": "01/01/1920", "var": "false", "dtap_ipv_date": "01/01/1923", "td": "true", "rv_date": "01/01/1917", "menb": "true", "hpv_date": "01/01/1908", "pcv13": "false", "iiv": "true", "patient": 3, "covid19_doses": 1, "dtap_ipv_hib_hepb": "false", "mmr": "true", "hepa": "false", "hib": "true", "hepb": "true", "ipv_date": "01/01/1916", "laiv4_date": "01/01/1910", "dt": "false", "laiv4": "false", "mmvr_date": "01/01/1925", "dtap_date": "01/01/1903", "dtap_ipv": "true", "tap_date": "01/01/1918", "mmr_date": "01/01/1911", "ppsv23": "true", "td_date": "01/01/1919", "covid19_booster_date": "01/01/1902", "dtap_hepb_ipv_date": "01/01/1921", "menacwy": "false", "dt_date": "01/01/1904", "dtap_ipv_hib": "false", "dtap_hepb_ipv": "true", "dtap_ipv_hib_date": "01/01/1922", "covid19_booster": "false", "covid19_date": "01/01/1901", "menacwy_date": "01/01/1912"}HTTP/1.1 200 OK
Date: Fri, 07 May 2021 04:44:29 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

8
{"id":3}
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
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 1192

{"ppsv23_date": "01/01/1915", "tap": "false", "hib_date": "01/01/1905", "dtap": "true", "iiv_date": "01/01/1909", "ipv": "false", "covid19": "true", "hepb_date": "01/01/1907", "dtap_ipv_hib_hepb_date": "01/01/1924", "hepa_date": "01/01/1906", "rv": "true", "pcv13_date": "01/01/1914", "hpv": "false", "mmvr": "false", "var_date": "01/01/1920", "var": "false", "dtap_ipv_date": "01/01/1923", "td": "true", "rv_date": "01/01/1917", "menb": "true", "hpv_date": "01/01/1908", "pcv13": "false", "iiv": "true", "menb_date": "01/01/1913", "covid19_doses": 1, "dtap_ipv_hib_hepb": "false", "mmr": "true", "hepa": "false", "hib": "true", "hepb": "true", "ipv_date": "01/01/1916", "laiv4_date": "01/01/1910", "dt": "false", "laiv4": "false", "mmvr_date": "01/01/1934", "dtap_date": "01/01/1903", "dtap_ipv": "true", "tap_date": "01/01/1918", "mmr_date": "01/01/1911", "ppsv23": "true", "td_date": "01/01/1919", "covid19_booster_date": "01/01/1902", "dtap_hepb_ipv_date": "01/01/1921", "menacwy": "false", "dt_date": "01/01/1904", "dtap_ipv_hib": "false", "dtap_hepb_ipv": "true", "dtap_ipv_hib_date": "01/01/1922", "covid19_booster": "false", "covid19_date": "01/01/1901", "menacwy_date": "01/01/1912"}HTTP/1.1 200 OK
Date: Fri, 07 May 2021 15:43:43 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

2
{}
0
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
DELETE /tscharts/v1/patient/12/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 07 May 2021 15:43:43 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

2
{}
0
```


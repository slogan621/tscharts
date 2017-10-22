**Get Routing Slip Resource**
----
  Returns json data about a single routing slip resource. Includes all 
  associated routingslipentry and routingslipcomment resources associated
  with the routingslip.

* **URL**

  /tscharts/v1/routingslip/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"category":"New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other","patient":id,"comments":[id, id, id, ...],"clinic":id,"routing":[id, id, id,...],"id":id}`

* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/routingslip/26693/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 04:13:28 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"category":"New Cleft","patient":32,"comments":[],"clinic":47,"routing":[],"id":26693}
```
  
**Get Multiple Routing Slip Resources**
----
  Returns all matching routingslip resources. 
  None: return format based on search parameters. See below for details.

* **URL**

  /tscharts/v1/routingslip/

* **Method:**

  `GET`
  
* **Data Params**

   **Required:**

   One or more of the following must be used to filter the results. 

   `patient` patient id. If specified with a clinic, a single routing slip is returned. Otherwise, all routing slips for the patient are returned in an array.<br />
   `clinic` clinic id. If specified alone, routing slips for all patients are returned for the clinic. If specified with patient, then a single routing slip is returned. <br />

*  **URL Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content (patient & clinic):** `{"category":"New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other","patient":id,"comments":[id, id, id, ...],"clinic":id,"routing":[id, id, id,...],"id":id}`<br/>
    **Content (patient | clinic):** `[{"category":"New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other","patient":id,"comments":[id, id, id, ...],"clinic":id,"routing":[id, id, id,...],"id":id}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Examples:**

```
GET /tscharts/v1/routingslip/?patient=812&clinic=55 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.1 200 OK
Date: Sun, 22 Oct 2017 05:38:19 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json

56
{"category":"New Cleft","patient":812,"comments":[],"clinic":55,"routing":[],"id":795}
0
```
  
```
GET /tscharts/v1/routingslip/?clinic=55 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.1 200 OK
Date: Sun, 22 Oct 2017 05:38:19 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json

21fd

[{"category":"New Cleft","patient":859,"comments":[],"clinic":55,"routing":[],"id":842},{"category":"New Cleft","patient":858,"comments":[],"clinic":55,"routing":[],"id":841},{"category":"New Cleft","patient":857,"comments":[],"clinic":55,"routing":[],"id":840},{"category":"New Cleft","patient":856,"comments":[],"clinic":55,"routing":[],"id":839},{"category":"New Cleft","patient":855,"comments":[],"clinic":55,"routing":[],"id":838},{"category":"New Cleft","patient":854,"comments":[],"clinic":55,"routing":[],"id":837},{"category":"New Cleft","patient":853,"comments":[],"clinic":55,"routing":[],"id":836},{"category":"New Cleft","patient":852,"comments":[],"clinic":55,"routing":[],"id":835},{"category":"New Cleft","patient":851,"comments":[],"clinic":55,"routing":[],"id":834},{"category":"New Cleft","patient":850,"comments":[],"clinic":55,"routing":[],"id":833},{"category":"New Cleft","patient":849,"comments":[],"clinic":55,"routing":[],"id":832},{"category":"New Cleft","patient":848,"comments":[],"clinic":55,"routing":[],"id":831},{"category":"New Cleft","patient":847,"comments":[],"clinic":55,"routing":[],"id":830},{"category":"New Cleft","patient":846,"comments":[],"clinic":55,"routing":[],"id":829},{"category":"New Cleft","patient":845,"comments":[],"clinic":55,"routing":[],"id":828},{"category":"New Cleft","patient":844,"comments":[],"clinic":55,"routing":[],"id":827},{"category":"New Cleft","patient":843,"comments":[],"clinic":55,"routing":[],"id":826},{"category":"New Cleft","patient":842,"comments":[],"clinic":55,"routing":[],"id":825},{"category":"New Cleft","patient":841,"comments":[],"clinic":55,"routing":[],"id":824},{"category":"New Cleft","patient":840,"comments":[],"clinic":55,"routing":[],"id":823},{"category":"New Cleft","patient":839,"comments":[],"clinic":55,"routing":[],"id":822},{"category":"New Cleft","patient":838,"comments":[],"clinic":55,"routing":[],"id":821},{"category":"New Cleft","patient":837,"comments":[],"clinic":55,"routing":[],"id":820},{"category":"New Cleft","patient":836,"comments":[],"clinic":55,"routing":[],"id":819},{"category":"New Cleft","patient":835,"comments":[],"clinic":55,"routing":[],"id":818},{"category":"New Cleft","patient":834,"comments":[],"clinic":55,"routing":[],"id":817},{"category":"New Cleft","patient":833,"comments":[],"clinic":55,"routing":[],"id":816},{"category":"New Cleft","patient":832,"comments":[],"clinic":55,"routing":[],"id":815},{"category":"New Cleft","patient":831,"comments":[],"clinic":55,"routing":[],"id":814},{"category":"New Cleft","patient":830,"comments":[],"clinic":55,"routing":[],"id":813},{"category":"New Cleft","patient":829,"comments":[],"clinic":55,"routing":[],"id":812},{"category":"New Cleft","patient":828,"comments":[],"clinic":55,"routing":[],"id":811},{"category":"New Cleft","patient":827,"comments":[],"clinic":55,"routing":[],"id":810},{"category":"New Cleft","patient":826,"comments":[],"clinic":55,"routing":[],"id":809},{"category":"New Cleft","patient":825,"comments":[],"clinic":55,"routing":[],"id":808},{"category":"New Cleft","patient":824,"comments":[],"clinic":55,"routing":[],"id":807},{"category":"New Cleft","patient":823,"comments":[],"clinic":55,"routing":[],"id":806},{"category":"New Cleft","patient":822,"comments":[],"clinic":55,"routing":[],"id":805},{"category":"New Cleft","patient":821,"comments":[],"clinic":55,"routing":[],"id":804},{"category":"New Cleft","patient":820,"comments":[],"clinic":55,"routing":[],"id":803},{"category":"New Cleft","patient":819,"comments":[],"clinic":55,"routing":[],"id":802},{"category":"New Cleft","patient":818,"comments":[],"clinic":55,"routing":[],"id":801},{"category":"New Cleft","patient":817,"comments":[],"clinic":55,"routing":[],"id":800},{"category":"New Cleft","patient":816,"comments":[],"clinic":55,"routing":[],"id":799},{"category":"New Cleft","patient":815,"comments":[],"clinic":55,"routing":[],"id":798},{"category":"New Cleft","patient":814,"comments":[],"clinic":55,"routing":[],"id":797},{"category":"New Cleft","patient":813,"comments":[],"clinic":55,"routing":[],"id":796},{"category":"New Cleft","patient":812,"comments":[],"clinic":55,"routing":[],"id":795},{"category":"New Cleft","patient":811,"comments":[],"clinic":55,"routing":[],"id":794},{"category":"New Cleft","patient":810,"comments":[],"clinic":55,"routing":[],"id":793},{"category":"New Cleft","patient":809,"comments":[],"clinic":55,"routing":[],"id":792},{"category":"New Cleft","patient":808,"comments":[],"clinic":55,"routing":[],"id":791},{"category":"New Cleft","patient":807,"comments":[],"clinic":55,"routing":[],"id":790},{"category":"New Cleft","patient":806,"comments":[],"clinic":55,"routing":[],"id":789},{"category":"New Cleft","patient":805,"comments":[],"clinic":55,"routing":[],"id":788},{"category":"New Cleft","patient":804,"comments":[],"clinic":55,"routing":[],"id":787},{"category":"New Cleft","patient":803,"comments":[],"clinic":55,"routing":[],"id":786},{"category":"New Cleft","patient":802,"comments":[],"clinic":55,"routing":[],"id":785},{"category":"New Cleft","patient":801,"comments":[],"clinic":55,"routing":[],"id":784},{"category":"New Cleft","patient":800,"comments":[],"clinic":55,"routing":[],"id":783},{"category":"New Cleft","patient":799,"comments":[],"clinic":55,"routing":[],"id":782},{"category":"New Cleft","patient":798,"comments":[],"clinic":55,"routing":[],"id":781},{"category":"New Cleft","patient":797,"comments":[],"clinic":55,"routing":[],"id":780},{"category":"New Cleft","patient":796,"comments":[],"clinic":55,"routing":[],"id":779},{"category":"New Cleft","patient":795,"comments":[],"clinic":55,"routing":[],"id":778},{"category":"New Cleft","patient":794,"comments":[],"clinic":55,"routing":[],"id":777},{"category":"New Cleft","patient":793,"comments":[],"clinic":55,"routing":[],"id":776},{"category":"New Cleft","patient":792,"comments":[],"clinic":55,"routing":[],"id":775},{"category":"New Cleft","patient":791,"comments":[],"clinic":55,"routing":[],"id":774},{"category":"New Cleft","patient":790,"comments":[],"clinic":55,"routing":[],"id":773},{"category":"New Cleft","patient":789,"comments":[],"clinic":55,"routing":[],"id":772},{"category":"New Cleft","patient":788,"comments":[],"clinic":55,"routing":[],"id":771},{"category":"New Cleft","patient":787,"comments":[],"clinic":55,"routing":[],"id":770},{"category":"New Cleft","patient":786,"comments":[],"clinic":55,"routing":[],"id":769},{"category":"New Cleft","patient":785,"comments":[],"clinic":55,"routing":[],"id":768},{"category":"New Cleft","patient":784,"comments":[],"clinic":55,"routing":[],"id":767},{"category":"New Cleft","patient":783,"comments":[],"clinic":55,"routing":[],"id":766},{"category":"New Cleft","patient":782,"comments":[],"clinic":55,"routing":[],"id":765},{"category":"New Cleft","patient":781,"comments":[],"clinic":55,"routing":[],"id":764},{"category":"New Cleft","patient":780,"comments":[],"clinic":55,"routing":[],"id":763},{"category":"New Cleft","patient":779,"comments":[],"clinic":55,"routing":[],"id":762},{"category":"New Cleft","patient":778,"comments":[],"clinic":55,"routing":[],"id":761},{"category":"New Cleft","patient":777,"comments":[],"clinic":55,"routing":[],"id":760},{"category":"New Cleft","patient":776,"comments":[],"clinic":55,"routing":[],"id":759},{"category":"New Cleft","patient":775,"comments":[],"clinic":55,"routing":[],"id":758},{"category":"New Cleft","patient":774,"comments":[],"clinic":55,"routing":[],"id":757},{"category":"New Cleft","patient":773,"comments":[],"clinic":55,"routing":[],"id":756},{"category":"New Cleft","patient":772,"comments":[],"clinic":55,"routing":[],"id":755},{"category":"New Cleft","patient":771,"comments":[],"clinic":55,"routing":[],"id":754},{"category":"New Cleft","patient":770,"comments":[],"clinic":55,"routing":[],"id":753},{"category":"New Cleft","patient":769,"comments":[],"clinic":55,"routing":[],"id":752},{"category":"New Cleft","patient":768,"comments":[],"clinic":55,"routing":[],"id":751},{"category":"New Cleft","patient":767,"comments":[],"clinic":55,"routing":[],"id":750},{"category":"New Cleft","patient":766,"comments":[],"clinic":55,"routing":[],"id":749},{"category":"New Cleft","patient":764,"comments":[],"clinic":55,"routing":[],"id":747},{"category":"New Cleft","patient":765,"comments":[],"clinic":55,"routing":[],"id":748},{"category":"New Cleft","patient":763,"comments":[],"clinic":55,"routing":[],"id":746},{"category":"New Cleft","patient":762,"comments":[],"clinic":55,"routing":[],"id":745},{"category":"New Cleft","patient":860,"comments":[],"clinic":55,"routing":[],"id":843},{"category":"New Cleft","patient":861,"comments":[],"clinic":55,"routing":[],"id":844}]

0
```

**Create a Routing Slip Resource**
----

* **URL**

  /tscharts/v1/routingslip/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br/>
   `patient` patient resource id<br/>
   `category` string one of "New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other"<br/>

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
POST /tscharts/v1/routingslip/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 54
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"category": "New Cleft", "clinic": 47, "patient": 32}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 04:13:24 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":26693}
```

**Update a Routing Slip Resource**
----
  Update a routingslip instance.

* **URL**

  /tscharts/v1/routingslip/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   `category` string one of "New Cleft" | "Dental" | "Returning Cleft" | "Ortho" | "Other"<br/>

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/routingslip/32040/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 21
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"category": "Ortho"}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 06:57:08 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete a Routing Slip Resource**
----
  Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/routingslip/id

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
DELETE /tscharts/v1/routingslip/140/ HTTP/1.1
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

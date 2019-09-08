**Get ENT Treatment**

----
  Returns json data about a single ENT treatment resource. 

* **URL**

  /tscharts/v1/enttreatment/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "treatment": treatment_name, "side" : "right" | "left" | "both", "username" : text, "comment": text, "future": true | false}

Value for treatment_name, above, can be one of the following:

"cleaned"<br/>
"audiogram"<br/>
"tympanogram"<br/>
"mastoid debrided"<br/>
"hearing aid eval"<br/>
"antibiotic drops"<br/>
"antibiotic orally"<br/>
"antibiotic acute"<br/>
"antibiotic water"<br/>
"boric acid today"<br/>
"boric acid home"<br/>
"tube removed"<br/>
"foreign body removed"<br/>
"referred ensenada"<br/>
"referred childrens tijuana"<br/>
"surgery tubs"<br/>
"surgery tplasty"<br/>
"surgery eua"<br/>
"surgery fb"<br/>
"surgery myringotomy"<br/>
"surgery cerumen removal"<br/>
"surgery granuloma removal"<br/>
"surgery septorhinoplasty"<br/>
"surgery scar revision cleft"<br/>
"surgery frenulectomy"<br/>
"other"<br/>
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/enttreatment/12/ HTTP/1.1
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
{"id":27,"treatment":"boric acid today","side":"left","future":"false","clinic":9,"patient":6,"time":"2017-12-11T01:02:24","username":"xxyyzz","comment":"Some comment here"}

```
  
**Get Multiple ENT Histories**
----
  Returns data for all matching ENT treatment resources. A given patient 
may have multiple treatments depending on his or her condition for a given
clinic.

* **URL**

  /tscharts/v1/enttreatment/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

   `patient` patient id<br />
   `clinic` clinic id<br />
   `treatment` 
   `name` text string<br />
   `side` "left", "right", or "both"<br />
   `duration` "days", "weeks", "months", or "intermittent"<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

    [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "treatment": treatment_name, "side" : "right" | "left" | "both", "username" : text, "comment": text, "future": true | false}, ...]

See above for definition of treatment_name
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/enttreatment/?clinic=3 HTTP/1.1
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
[{"id":27,"treatment":"boric acid today","side":"left","future":"false","clinic":9,"patient":6,"time":"2017-12-11T01:02:24","username":"xxyyzz","comment":"Some comment here"}, ...]
0
```
  
**Create an ENT Treatment**
----
  Create an ENT treatment resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/enttreatment/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   `treatment` see treatment_name, above, for possible values
   `side` one of the following: "left", "right", "both"<br />
   `future` false or true<br />
   `comment` comment supplied by the user for this treatment item. If treatment is "other", defines the treatment given<br />
   `username` name of logged in user making this change <br />

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
POST /tscharts/v1/enttreatment/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"treatment":"boric acid today","side":"left","future":"false","clinic":9,"patient":6,"username":"xxyyzz","comment":"Some comment here"}HTTP/1.1 200 OK
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

**Update an ENT Treatment**
----
  Update an ENT treatment instance

* **URL**

  /tscharts/v1/enttreatment/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

   `treatment` see treatment_values, above for list of possible treatment strings<br />
   `future` true or false<br />
   `side` one of the following: "right, "left", "both"<br />
   `comment` optional comment supplied by the user for this treatment item<br />
   `username` name of logged in user making this change <br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/enttreatment/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"side": "both"}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete an ENT Treatment**
----
  Delete an ENT treatment resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/enttreatment/id

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
DELETE /tscharts/v1/enttreatment/140/ HTTP/1.1
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


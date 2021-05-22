**Get ENT Exam**

----
  Returns json data about a single ENT exam resource. 

* **URL**

  /tscharts/v1/entexam/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

   {"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "normal": "left" | "right" | "both" | "none", "microtia":  "left" | "right" | "both" | "none", "wax":  "left" | "right" | "both" | "none", "drainage":  "left" | "right" | "both" | "none", "externalOtitis":  "left" | "right" | "both" | "none", "fb":  "left" | "right" | "both" | "none", "effusion":  "left" | "right" | "both" | "none", "middle_ear_infection":  "left" | "right" | "both" | "none", "tubeRight": "in place" | "extruding" | "in canal" | "none", "tubeLeft": "in place" | "extruding" | "in canal" | "none", "tympanoLeft": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tympanoRight": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tmGranulations":  "left" | "right" | "both" | "none", "tmRetraction":  "left" | "right" | "both" | "none", "tmAtelectasis":  "left" | "right" | "both" | "none", "perfLeft": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "perfRight": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "voiceTest" : "normal" | "abnormal" | "none", "forkAD": "a greater b" | "b greater a" | "a equal b" | "none", "forkAS": "a greater b" | "b greater a" | "a equal b" | "none", "bc": "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as", "fork": "256" | "512" | "none", "username" : text, "comment": text, "cleft_lip": "true | false", "cleft_palate": "true | false", "repaired_lip": "yes | no | na", "repaired_palate": "yes | no | na"}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/entexam/1/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Sat, 22 May 2021 20:30:22 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

28e
{"comment":"A comment","fork":"512","tmAtelectasis":"both","voiceTest":"normal","clinic":1,"repaired_palate":"no","microtia":"right","id":1,"cleft_palate":"false","perfRight":"50 percent","forkAD":"a greater b","bc":"ad lat ad","repaired_lip":"yes","forkAS":"a equal b","cleft_lip":"true","tubeLeft":"in place","wax":"both","externalOtitis":"left","username":"Gomez","patient":1,"normal":"left","time":"2021-05-22T13:30:22.314","tubeRight":"extruding","fb":"none","effusion":"left","tmGranulations":"left","tympanoLeft":"posterior","perfLeft":"posterior","tmRetraction":"right","tympanoRight":"50 percent","drainage":"none","middle_ear_infection":"both"}
0
```
  
**Get Multiple ENT Exams**
----
  Returns data about all matching ENT exam resources.

* **URL**

  /tscharts/v1/entexam/

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
   [{"id" : id, "clinic" : id, "patient" : id, "time" : UTC date time string, "normal": "left" | "right" | "both" | "none", "microtia":  "left" | "right" | "both" | "none", "wax":  "left" | "right" | "both" | "none", "effusion":  "left" | "right" | "both" | "none", "middle_ear_infection":  "left" | "right" | "both" | "none", "drainage":  "left" | "right" | "both" | "none", "externalOtitis":  "left" | "right" | "both" | "none", "fb":  "left" | "right" | "both" | "none", "tubeRight": "in place" | "extruding" | "in canal" | "none", "tubeLeft": "in place" | "extruding" | "in canal" | "none", "tympanoLeft": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tympanoRight": "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "tmGranulations":  "left" | "right" | "both" | "none", "tmRetraction":  "left" | "right" | "both" | "none", "tmAtelectasis":  "left" | "right" | "both" | "none", "perfLeft": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "perfRight": "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none", "voiceTest" : "normal" | "abnormal" | "none", "forkAD": "a greater b" | "b greater a" | "a equal b" | "none", "forkAS": "a greater b" | "b greater a" | "a equal b" | "none", "bc": "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as", "fork": "256" | "512" | "none", "username" : text, "comment": text, "cleft_lip": "true | false", "cleft_palate": "true | false", "repaired_lip": "yes | no | na", "repaired_palate": "yes | no | na"}, ...]
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/entexam/?clinic=3 HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Sat, 22 May 2021 20:30:23 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

7ac
[{"comment":"A comment","fork":"512","tmAtelectasis":"both","voiceTest":"normal","clinic":3,"repaired_palate":"na","microtia":"right","id":4,"cleft_palate":"true","perfRight":"50 percent","forkAD":"a greater b","bc":"ad lat ad","repaired_lip":"no","forkAS":"a equal b","cleft_lip":"false","tubeLeft":"in place","wax":"both","externalOtitis":"left","username":"Gomez","patient":3,"normal":"left","time":"2021-05-22T13:30:23.343","tubeRight":"extruding","fb":"none","effusion":"none","tmGranulations":"left","tympanoLeft":"posterior","perfLeft":"posterior","tmRetraction":"right","tympanoRight":"50 percent","drainage":"none","middle_ear_infection":"left"},{"comment":"A comment","fork":"512","tmAtelectasis":"both","voiceTest":"normal","clinic":3,"repaired_palate":"na","microtia":"right","id":5,"cleft_palate":"true","perfRight":"50 percent","forkAD":"a greater b","bc":"ad lat ad","repaired_lip":"no","forkAS":"a equal b","cleft_lip":"false","tubeLeft":"in place","wax":"both","externalOtitis":"left","username":"Gomez","patient":4,"normal":"left","time":"2021-05-22T13:30:23.355","tubeRight":"extruding","fb":"none","effusion":"left","tmGranulations":"left","tympanoLeft":"posterior","perfLeft":"posterior","tmRetraction":"right","tympanoRight":"50 percent","drainage":"none","middle_ear_infection":"right"},{"comment":"A comment","fork":"512","tmAtelectasis":"both","voiceTest":"normal","clinic":3,"repaired_palate":"na","microtia":"right","id":6,"cleft_palate":"true","perfRight":"50 percent","forkAD":"a greater b","bc":"ad lat ad","repaired_lip":"no","forkAS":"a equal b","cleft_lip":"false","tubeLeft":"in place","wax":"both","externalOtitis":"left","username":"Gomez","patient":5,"normal":"left","time":"2021-05-22T13:30:23.365","tubeRight":"extruding","fb":"none","effusion":"both","tmGranulations":"left","tympanoLeft":"posterior","perfLeft":"posterior","tmRetraction":"right","tympanoRight":"50 percent","drainage":"none","middle_ear_infection":"none"}]
0

```
  
**Create an ENT Exam**
----
  Create an ENT exam resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/entexam/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   'normal' one of the following:  "left" | "right" | "both" | "none" <br/>
   `microtia` one of the following:  "left" | "right" | "both" | "none"<br/>
   `wax` one of the following:  "left" | "right" | "both" | "none"<br/>
   `effusion` one of the following:  "left" | "right" | "both" | "none"<br/>
   `middle_ear_infection` one of the following:  "left" | "right" | "both" | "none"<br/>
   `drainage` one of the following:  "left" | "right" | "both" | "none"<br/>
   `externalOtitis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `fb` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tubeRight` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tubeLeft` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tympanoLeft` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tympanoRight` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tmGranulations` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmRetraction` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmAtelectasis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `perfLeft` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `perfRight` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `voiceTest`  one of the following: "normal" | "abnormal" | "none"<br/>
   `forkAD` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `forkAS` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `bc` one of the following: "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as"<br/>
   `fork` one of the following: "256" | "512" | "none"<br/>
   `comment` comment supplied by the user for this exam item<br />
   `username` name of logged in user making this change <br />
   `cleft_lip` one of the following: "true" | "false"<br />
   `cleft_palate` one of the following: "true" | "false" <br />
   `repaired_lip` one of the following: "yes" | "no" | "na" <br />
   `repaired_palate` one of the following: "yes" | "no" | "na" <br />

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
POST /tscharts/v1/entexam/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 673

{"comment": "A comment", "username": "Gomez", "tmAtelectasis": "both", "voiceTest": "normal", "clinic": 1, "repaired_palate": "no", "microtia": "right", "cleft_palate": "false", "perfRight": "50 percent", "forkAD": "a greater b", "bc": "ad lat ad", "repaired_lip": "yes", "forkAS": "a equal b", "cleft_lip": "true", "tubeLeft": "in place", "wax": "both", "externalOtitis": "left", "fork": "512", "patient": 1, "normal": "left", "tubeRight": "extruding", "fb": "none", "effusion": "left", "tmGranulations": "left", "tympanoLeft": "posterior", "perfLeft": "posterior", "tmRetraction": "right", "tympanoRight": "50 percent", "drainage": "none", "middle_ear_infection": "both"}HTTP/1.1 200 OK
Date: Sat, 22 May 2021 20:30:22 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

8
{"id":1}
0
```

**Update an ENT Exam**
----
  Update an ENT exam instance

* **URL**

  /tscharts/v1/entexam/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

   `clinic` clinic resource id<br />
   `patient` patient resource id<br />
   'normal' one of the following:  "left" | "right" | "both" | "none" <br/>
   `microtia` one of the following:  "left" | "right" | "both" | "none"<br/>
   `wax` one of the following:  "left" | "right" | "both" | "none"<br/>
   `effusion` one of the following:  "left" | "right" | "both" | "none"<br/>
   `middle_ear_infection` one of the following:  "left" | "right" | "both" | "none"<br/>
   `drainage` one of the following:  "left" | "right" | "both" | "none"<br/>
   `externalOtitis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `fb` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tubeRight` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tubeLeft` one of the following: "in place" | "extruding" | "in canal" | "none"<br/>
   `tympanoLeft` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tympanoRight` one of the following: "anterior" | "posterior" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `tmGranulations` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmRetraction` one of the following:  "left" | "right" | "both" | "none"<br/>
   `tmAtelectasis` one of the following:  "left" | "right" | "both" | "none"<br/>
   `perfLeft` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `perfRight` one of the following: "anterior" | "posterior" | "marginal" | "25 percent" | "50 percent" | "75 percent" | "total" | "none"<br/>
   `voiceTest`  one of the following: "normal" | "abnormal" | "none"<br/>
   `forkAD` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `forkAS` one of the following: "a greater b" | "b greater a" | "a equal b" | "none"<br/>
   `bc` one of the following: "ad lat ad" | "ad lat as" | "as lat ad" | "as lat as"<br/>
   `fork` one of the following: "256" | "512" | "none"<br/>
   `comment` comment supplied by the user for this exam item<br />
   `username` name of logged in user making this change <br />
   `cleft_lip` one of the following: "true" | "false"<br />
   `cleft_palate` one of the following: "true" | "false" <br />
   `repaired_lip` one of the following: "yes" | "no" | "na" <br />
   `repaired_palate` one of the following: "yes" | "no" | "na" <br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/entexam/13/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 19

{"bc": "ad lat as"}HTTP/1.1 200 OK
Date: Sat, 22 May 2021 20:30:23 GMT
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

**Delete an ENT Exam**
----
  Delete an ENT exam resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/entexam/id

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
DELETE /tscharts/v1/entexam/1/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Sat, 22 May 2021 20:30:22 GMT
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


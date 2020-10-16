**Get Dental Treatment**

----
  Returns json data about a single dental treatment resource. 

* **URL**

  /tscharts/v1/dentaltreatment/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

  Response is a JSON object with the following fields:

  "id" : id,<br />
  "clinic" : id, <br />
  "patient" : id, <br />
  "time" : UTC date time string, <br />
  "exam" : true | false<br />
  "examComment" : text<br />
  "prophy" : true | false<br />
  "prophyComment" : text<br />
  "srpUR" : true | false<br />
  "srpLR" : true | false<br />
  "srpUL" : true | false<br />
  "srpLL" : true | false<br />
  "srpComment" : text<br />
  "xraysViewed" : true | false<br />
  "xraysViewedComment" : text<br />
  "headNeckOralCancerExam" : true | false<br />
  "headNeckOralCancerExamComment" : text<br />
  "oralHygieneInstruction" : true | false<br />
  "oralHygieneInstructionComment" : text<br />
  "flourideTxVarnish" : true | false<br />
  "flourideTxVarnishComment" : text<br />
  "nutritionalCounseling" : true | false<br />
  "nutritionalCounselingComment" : text<br />
  "orthoEvaluation" : true | false<br />
  "orthoEvaluationComment" : text<br />
  "orthoTx" : true | false<br />
  "orthoTxComment" : text<br />
  "oralSurgeryEvaluation" : true | false<br />
  "oralSurgeryEvaluationComment" : text<br />
  "oralSurgeryTx" : true | false<br />
  "oralSurgeryTxComment" : text<br />
  "localAnesthetic" : 'none' | 'benzocaine' | 'lidocaine' | 'septocaine' | 'other'<br />
  "localAnestheticNumberOfCarps" : integer <br />
  "localAnestheticComment" : text<br />
  "comment" : text<br />

* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/dentaltreatment/49/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 16 Oct 2020 18:17:25 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

3a0
{"comment":"JcOftkzh8smwa","oralSurgeryTxComment":"QuNhXvEbipit","srpUR":"true","srpLR":"true","xraysViewed":"true","clinic":25,"srpLL":"true","localAnestheticComment":"","prophy":"false","srpUL":"true","flourideTxVarnish":"false","id":49,"oralHygieneInstruction":"false","prophyComment":"eu","orthoEvaluation":"false","headNeckOralCancerExam":"false","xraysViewedComment":"BhU3","localAnestheticNumberCarps":23,"flourideTxVarnishComment":"zwbOrp5","oralSurgeryTx":"true","localAnesthetic":"none","username":"Gomez","patient":25,"exam":"false","examComment":"C","oralSurgeryEvaluation":"true","orthoEvaluationComment":"N1aQ7WP9u","oralHygieneInstructionComment":"XGj5zW","orthoTx":"true","oralSurgeryEvaluationComment":"T1VbX5eBwlr","orthoTxComment":"uUH9zq1rTU","nutritionalCounselingComment":"tCRBWNDy","headNeckOralCancerExamComment":"8Wp4j","srpComment":"Hqy","time":"2020-10-16T11:17:25.035","nutritionalCounseling":"true"}
0
```
  
**Get Multiple Dental Treatments**
----
  Returns data for all matching dental treatment resources. 

* **URL**

  /tscharts/v1/dentaltreatment/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

  "clinic" : id, <br />
  "patient" : id, <br />
  "exam" : true | false<br />
  "examComment" : text<br />
  "prophy" : true | false<br />
  "prophyComment" : text<br />
  "srpUR" : true | false<br />
  "srpLR" : true | false<br />
  "srpUL" : true | false<br />
  "srpLL" : true | false<br />
  "srpComment" : text<br />
  "xraysViewed" : true | false<br />
  "xraysViewedComment" : text<br />
  "headNeckOralCancerExam" : true | false<br />
  "headNeckOralCancerExamComment" : text<br />
  "oralHygieneInstruction" : true | false<br />
  "oralHygieneInstructionComment" : text<br />
  "flourideTxVarnish" : true | false<br />
  "flourideTxVarnishComment" : text<br />
  "nutritionalCounseling" : true | false<br />
  "nutritionalCounselingComment" : text<br />
  "orthoEvaluation" : true | false<br />
  "orthoEvaluationComment" : text<br />
  "orthoTx" : true | false<br />
  "orthoTxComment" : text<br />
  "oralSurgeryEvaluation" : true | false<br />
  "oralSurgeryEvaluationComment" : text<br />
  "oralSurgeryTx" : true | false<br />
  "oralSurgeryTxComment" : text<br />
  "localAnesthetic" : 'none' | 'benzocaine' | 'lidocaine' | 'septocaine' | 'other'<br />
  "localAnestheticNumberOfCarps" : integer <br />
  "localAnestheticComment" : text<br />
  "comment" : text<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    [{"comment":"GKMFolMzGN6i4","oralSurgeryTxComment":"BkXzPmHjOflU","srpUR":"false","srpLR":"true","xraysViewed":"false","clinic":28,"srpLL":"false","localAnestheticComment":"","prophy":"true","srpUL":"false","flourideTxVarnish":"false","id":54,"oralHygieneInstruction":"true","prophyComment":"IX","orthoEvaluation":"false","headNeckOralCancerExam":"true","xraysViewedComment":"8l28","localAnestheticNumberCarps":799,"flourideTxVarnishComment":"Jd2wvm1","oralSurgeryTx":"false","localAnesthetic":"lidocaine","username":"Gomez","patient":27,"exam":"false","examComment":"Y","oralSurgeryEvaluation":"true","orthoEvaluationComment":"qkRSIPV1g","oralHygieneInstructionComment":"kbKFtQ","orthoTx":"true","oralSurgeryEvaluationComment":"3EEcNdNlKZR","orthoTxComment":"24x1rXAAj3","nutritionalCounselingComment":"G974w63p","headNeckOralCancerExamComment":"MqKaU","srpComment":"HkL","time":"2020-10-16T11:17:25.422","nutritionalCounseling":"true"},{"comment":"sTVkdSU1sHgxe","oralSurgeryTxComment":"mq3ouDCvSFe6","srpUR":"true","srpLR":"false","xraysViewed":"false","clinic":28,"srpLL":"true","localAnestheticComment":"","prophy":"false","srpUL":"false","flourideTxVarnish":"true","id":55,"oralHygieneInstruction":"false","prophyComment":"DA","orthoEvaluation":"true","headNeckOralCancerExam":"true","xraysViewedComment":"qOcq","localAnestheticNumberCarps":19,"flourideTxVarnishComment":"SCutrSS","oralSurgeryTx":"true","localAnesthetic":"septocaine","username":"Gomez","patient":28,"exam":"true","examComment":"7","oralSurgeryEvaluation":"true","orthoEvaluationComment":"zyhjp770U","oralHygieneInstructionComment":"irhkWm","orthoTx":"true","oralSurgeryEvaluationComment":"dQ2eCpvJmVE","orthoTxComment":"thtLgc0MSF","nutritionalCounselingComment":"V3naVM1K","headNeckOralCancerExamComment":"mYxHH","srpComment":"Ou6","time":"2020-10-16T11:17:25.431","nutritionalCounseling":"true"},{"comment":"25sH6VnGDP3j3","oralSurgeryTxComment":"WZBiYHDG1HGz","srpUR":"false","srpLR":"true","xraysViewed":"true","clinic":28,"srpLL":"true","localAnestheticComment":"","prophy":"false","srpUL":"true","flourideTxVarnish":"true","id":56,"oralHygieneInstruction":"true","prophyComment":"gx","orthoEvaluation":"true","headNeckOralCancerExam":"false","xraysViewedComment":"nU8x","localAnestheticNumberCarps":-194,"flourideTxVarnishComment":"achuBBH","oralSurgeryTx":"false","localAnesthetic":"lidocaine","username":"Gomez","patient":29,"exam":"true","examComment":"h","oralSurgeryEvaluation":"false","orthoEvaluationComment":"ZLaINc2xY","oralHygieneInstructionComment":"W8iiYE","orthoTx":"true","oralSurgeryEvaluationComment":"X6ZOSD6Ju5O","orthoTxComment":"We8KmlkeQc","nutritionalCounselingComment":"agpPFTF2","headNeckOralCancerExamComment":"wBxf3","srpComment":"zZo","time":"2020-10-16T11:17:25.439","nutritionalCounseling":"true"}]

* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/dentaltreatment/?clinic=28 HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 16 Oct 2020 18:17:25 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

af7
[{"comment":"GKMFolMzGN6i4","oralSurgeryTxComment":"BkXzPmHjOflU","srpUR":"false","srpLR":"true","xraysViewed":"false","clinic":28,"srpLL":"false","localAnestheticComment":"","prophy":"true","srpUL":"false","flourideTxVarnish":"false","id":54,"oralHygieneInstruction":"true","prophyComment":"IX","orthoEvaluation":"false","headNeckOralCancerExam":"true","xraysViewedComment":"8l28","localAnestheticNumberCarps":799,"flourideTxVarnishComment":"Jd2wvm1","oralSurgeryTx":"false","localAnesthetic":"lidocaine","username":"Gomez","patient":27,"exam":"false","examComment":"Y","oralSurgeryEvaluation":"true","orthoEvaluationComment":"qkRSIPV1g","oralHygieneInstructionComment":"kbKFtQ","orthoTx":"true","oralSurgeryEvaluationComment":"3EEcNdNlKZR","orthoTxComment":"24x1rXAAj3","nutritionalCounselingComment":"G974w63p","headNeckOralCancerExamComment":"MqKaU","srpComment":"HkL","time":"2020-10-16T11:17:25.422","nutritionalCounseling":"true"},{"comment":"sTVkdSU1sHgxe","oralSurgeryTxComment":"mq3ouDCvSFe6","srpUR":"true","srpLR":"false","xraysViewed":"false","clinic":28,"srpLL":"true","localAnestheticComment":"","prophy":"false","srpUL":"false","flourideTxVarnish":"true","id":55,"oralHygieneInstruction":"false","prophyComment":"DA","orthoEvaluation":"true","headNeckOralCancerExam":"true","xraysViewedComment":"qOcq","localAnestheticNumberCarps":19,"flourideTxVarnishComment":"SCutrSS","oralSurgeryTx":"true","localAnesthetic":"septocaine","username":"Gomez","patient":28,"exam":"true","examComment":"7","oralSurgeryEvaluation":"true","orthoEvaluationComment":"zyhjp770U","oralHygieneInstructionComment":"irhkWm","orthoTx":"true","oralSurgeryEvaluationComment":"dQ2eCpvJmVE","orthoTxComment":"thtLgc0MSF","nutritionalCounselingComment":"V3naVM1K","headNeckOralCancerExamComment":"mYxHH","srpComment":"Ou6","time":"2020-10-16T11:17:25.431","nutritionalCounseling":"true"},{"comment":"25sH6VnGDP3j3","oralSurgeryTxComment":"WZBiYHDG1HGz","srpUR":"false","srpLR":"true","xraysViewed":"true","clinic":28,"srpLL":"true","localAnestheticComment":"","prophy":"false","srpUL":"true","flourideTxVarnish":"true","id":56,"oralHygieneInstruction":"true","prophyComment":"gx","orthoEvaluation":"true","headNeckOralCancerExam":"false","xraysViewedComment":"nU8x","localAnestheticNumberCarps":-194,"flourideTxVarnishComment":"achuBBH","oralSurgeryTx":"false","localAnesthetic":"lidocaine","username":"Gomez","patient":29,"exam":"true","examComment":"h","oralSurgeryEvaluation":"false","orthoEvaluationComment":"ZLaINc2xY","oralHygieneInstructionComment":"W8iiYE","orthoTx":"true","oralSurgeryEvaluationComment":"X6ZOSD6Ju5O","orthoTxComment":"We8KmlkeQc","nutritionalCounselingComment":"agpPFTF2","headNeckOralCancerExamComment":"wBxf3","srpComment":"zZo","time":"2020-10-16T11:17:25.439","nutritionalCounseling":"true"}]
0
```
  
**Create a Dental Treatment**
----
  Create a dental treatment resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/dentaltreatment/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
  "clinic" : id, <br />
  "patient" : id, <br />
  "exam" : true | false<br />
  "examComment" : text<br />
  "prophy" : true | false<br />
  "prophyComment" : text<br />
  "srpUR" : true | false<br />
  "srpLR" : true | false<br />
  "srpUL" : true | false<br />
  "srpLL" : true | false<br />
  "srpComment" : text<br />
  "xraysViewed" : true | false<br />
  "xraysViewedComment" : text<br />
  "headNeckOralCancerExam" : true | false<br />
  "headNeckOralCancerExamComment" : text<br />
  "oralHygieneInstruction" : true | false<br />
  "oralHygieneInstructionComment" : text<br />
  "flourideTxVarnish" : true | false<br />
  "flourideTxVarnishComment" : text<br />
  "nutritionalCounseling" : true | false<br />
  "nutritionalCounselingComment" : text<br />
  "orthoEvaluation" : true | false<br />
  "orthoEvaluationComment" : text<br />
  "orthoTx" : true | false<br />
  "orthoTxComment" : text<br />
  "oralSurgeryEvaluation" : true | false<br />
  "oralSurgeryEvaluationComment" : text<br />
  "oralSurgeryTx" : true | false<br />
  "oralSurgeryTxComment" : text<br />
  "localAnesthetic" : 'none' | 'benzocaine' | 'lidocaine' | 'septocaine' | 'other'<br />
  "localAnestheticNumberOfCarps" : integer <br />
  "localAnestheticComment" : text<br />
  "comment" : text<br />

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
POST /tscharts/v1/dentaltreatment/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 932

{"comment": "cZ7b3WziJBw7O", "oralSurgeryTxComment": "Us6vdlj7eF0A", "srpUR": "false", "srpLR": "false", "xraysViewed": "true", "clinic": 30, "srpLL": "true", "patient": 30, "srpUL": "false", "flourideTxVarnish": "true", "oralHygieneInstruction": "false", "prophyComment": "my", "orthoEvaluation": "false", "headNeckOralCancerExam": "true", "xraysViewedComment": "MMH2", "localAnestheticNumberCarps": 690, "flourideTxVarnishComment": "Q5Q8uel", "oralSurgeryTx": "false", "localAnesthetic": "benzocaine", "username": "Gomez", "prophy": "true", "exam": "true", "examComment": "M", "oralSurgeryEvaluation": "true", "orthoEvaluationComment": "DsKfpiVUV", "oralHygieneInstructionComment": "cXi9bj", "orthoTx": "false", "oralSurgeryEvaluationComment": "tuM29mZIMRn", "orthoTxComment": "ecVMvDeGab", "nutritionalCounselingComment": "TVEqrNJ7", "headNeckOralCancerExamComment": "HeBUP", "srpComment": "qgh", "nutritionalCounseling": "true"}HTTP/1.1 200 OK
Date: Fri, 16 Oct 2020 18:17:25 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

9
{"id":60}
0
```

**Update a Dental Treatment**
----
  Update a dental treatment instance

* **URL**

  /tscharts/v1/dentaltreatment/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

  "clinic" : id, <br />
  "patient" : id, <br />
  "exam" : true | false<br />
  "examComment" : text<br />
  "prophy" : true | false<br />
  "prophyComment" : text<br />
  "srpUR" : true | false<br />
  "srpLR" : true | false<br />
  "srpUL" : true | false<br />
  "srpLL" : true | false<br />
  "srpComment" : text<br />
  "xraysViewed" : true | false<br />
  "xraysViewedComment" : text<br />
  "headNeckOralCancerExam" : true | false<br />
  "headNeckOralCancerExamComment" : text<br />
  "oralHygieneInstruction" : true | false<br />
  "oralHygieneInstructionComment" : text<br />
  "flourideTxVarnish" : true | false<br />
  "flourideTxVarnishComment" : text<br />
  "nutritionalCounseling" : true | false<br />
  "nutritionalCounselingComment" : text<br />
  "orthoEvaluation" : true | false<br />
  "orthoEvaluationComment" : text<br />
  "orthoTx" : true | false<br />
  "orthoTxComment" : text<br />
  "oralSurgeryEvaluation" : true | false<br />
  "oralSurgeryEvaluationComment" : text<br />
  "oralSurgeryTx" : true | false<br />
  "oralSurgeryTxComment" : text<br />
  "localAnesthetic" : 'none' | 'benzocaine' | 'lidocaine' | 'septocaine' | 'other'<br />
  "localAnestheticNumberOfCarps" : integer <br />
  "localAnestheticComment" : text<br />
  "comment" : text<br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/dentaltreatment/60/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 905

{"comment": "DpfDoaIzJEVrg", "oralSurgeryTxComment": "gm0Dw05BOcKT", "srpUR": "false", "srpLR": "false", "xraysViewed": "false", "srpLL": "true", "srpUL": "false", "flourideTxVarnish": "false", "oralHygieneInstruction": "true", "prophyComment": "Zk", "orthoEvaluation": "false", "headNeckOralCancerExam": "false", "xraysViewedComment": "CoDF", "localAnestheticNumberCarps": -67, "flourideTxVarnishComment": "e0WTaUR", "oralSurgeryTx": "false", "localAnesthetic": "none", "username": "username", "prophy": "true", "exam": "false", "examComment": "7", "oralSurgeryEvaluation": "false", "orthoEvaluationComment": "jhLh8xebG", "oralHygieneInstructionComment": "bvdNLm", "orthoTx": "false", "oralSurgeryEvaluationComment": "WFdn7YfzzoB", "orthoTxComment": "p0Ay7ovBk9", "nutritionalCounselingComment": "4s4BrhCz", "headNeckOralCancerExamComment": "2jp3i", "srpComment": "OkX", "nutritionalCounseling": "false"}HTTP/1.1 200 OK
Date: Fri, 16 Oct 2020 18:17:26 GMT
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

**Delete a Dental Treatment**
----
  Delete a dental treatment resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/dentaltreatment/id

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
DELETE /tscharts/v1/dentaltreatment/60/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token adf8e350d1c01f22d2ea5d70f2599b40160fc473
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Fri, 16 Oct 2020 18:17:55 GMT
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


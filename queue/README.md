**Get Multiple Queues**
----
  Returns all the queues established for the clinic

* **URL**

  /tscharts/v1/queue/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `clinic` clinic id<br />

   **Optional:**
 
   `station` station id<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"status":{"avgwait":"hh:mm:ss","maxwait":"hh:mm:ss","maxq":integer,"numwaiting":integer,"minwait":"hh:mm:ss","minq":integer,"avgq":integer},"queues":[{"avgservicetime":"hh:mm:ss","entries":[{"timein":"YYYY-MM-DD HH:MM:SS","waittime":"hh:mm:ss","estwaittime":"hh:mm:ss","patient":integer,"routingslipentry":integer}, ...],"name":string,"name_es":string,"clinicstation":integer}, ...]}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/queue/?clinic=1 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Tue, 18 Jul 2017 05:09:30 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


825
{"status":{"avgwait":"00:01:37","maxwait":"00:02:24","maxq":2,"numwaiting":8,"minwait":"00:00:31","minq":1,"avgq":1},"queues":[{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:08:05","waittime":"00:00:52","estwaittime":"00:00:52","patient":7,"routingslipentry":18}],"name":"Dental1","clinicstation":1},{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:08:26","waittime":"00:00:31","estwaittime":"00:00:31","patient":9,"routingslipentry":28}],"name":"Dental2","clinicstation":2},{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:08:58","waittime":"00:00:00","estwaittime":"00:00:00","patient":10,"routingslipentry":31}],"name":"Dental3","clinicstation":3},{"avgservicetime":"00:00:00","entries":[],"name":"Dental4","clinicstation":4},{"avgservicetime":"00:00:00","entries":[],"name":"Dental5","clinicstation":5},{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:06:33","waittime":"00:02:24","estwaittime":"00:02:24","patient":1,"routingslipentry":1},{"timein":"2017-07-18 05:06:38","waittime":"00:02:19","estwaittime":"00:02:19","patient":2,"routingslipentry":5}],"name":"ENT","clinicstation":6},{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:06:43","waittime":"00:02:14","estwaittime":"00:02:14","patient":3,"routingslipentry":6}],"name":"Ortho1","clinicstation":7},{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:07:14","waittime":"00:01:43","estwaittime":"00:01:43","patient":5,"routingslipentry":13}],"name":"Ortho2","clinicstation":8},{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:08:11","waittime":"00:00:47","estwaittime":"00:00:47","patient":8,"routingslipentry":25}],"name":"X-Ray","clinicstation":9},{"avgservicetime":"00:00:00","entries":[{"timein":"2017-07-18 05:06:48","waittime":"00:02:09","estwaittime":"00:02:09","patient":4,"routingslipentry":9}],"name":"Surgery Screening","clinicstation":10},{"avgservicetime":"00:00:00","entries":[],"name":"Speech","clinicstation":11},{"avgservicetime":"00:00:00","entries":[],"name":"Audiology","clinicstation":12}]}
```

**Get Multiple Queues**
----
  Returns all the queues established for the clinic

* **URL**

  /tscharts/v1/queue/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `clinic` clinic id<br />

   **Optional:**
 
   `station` station id<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"status":{"avgwait":"hh:mm:ss","maxwait":"hh:mm:ss","maxq":integer,"numwaiting":integer,"minwait":"hh:mm:ss","minq":integer,"avgq":integer},"queues":[{"avgservicetime":"hh:mm:ss","entries":[{"timein":"YYYY-MM-DD HH:MM:SS","waittime":"hh:mm:ss","estwaittime":"hh:mm:ss","patient":integer,"routingslipentry":integer}, ...],"name":string,"clinicstation":integer}, ...]}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/queue/ HTTP/1.1
Host: localhost:8000
Content-Length: 13
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"clinic": 1}HTTP/1.0 200 OK
Date: Tue, 11 Jul 2017 00:04:50 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, HEAD, OPTIONS


{"status":{"avgwait":"00:00:57","maxwait":"00:01:49","maxq":2,"numwaiting":7,"minwait":"00:00:10","minq":1,"avgq":1},"queues":[{"averageservicetime:"00:00:00","entries":[{"timein":"2017-07-11 00:04:11","waittime":"00:00:37","estwaittime":"00:00:37","patient":5,"routingslipentry":11}],"name":"Dental1","clinicstation":1},{"averageservicetime:"00:00:00","entries":[],"name":"Dental2","clinicstation":2},{"averageservicetime:"00:00:00","entries":[],"name":"Dental3","clinicstation":3},{"averageservicetime:"00:00:00","entries":[],"name":"Dental4","clinicstation":4},{"averageservicetime:"00:00:00","entries":[],"name":"Dental5","clinicstation":5},{"averageservicetime:"00:00:00","entries":[{"timein":"2017-07-11 00:03:19","waittime":"00:01:29","estwaittime":"00:01:29","patient":2,"routingslipentry":3},{"timein":"2017-07-11 00:03:34","waittime":"00:01:14","estwaittime":"00:01:14","patient":3,"routingslipentry":6}],"name":"ENT","clinicstation":6},{"averageservicetime:"00:00:00","entries":[],"name":"Ortho1","clinicstation":7},{"averageservicetime:"00:00:00","entries":[],"name":"Ortho2","clinicstation":8},{"averageservicetime:"00:00:00","entries":[{"timein":"2017-07-11 00:03:55","waittime":"00:00:53","estwaittime":"00:00:53","patient":4,"routingslipentry":8}],"name":"X-Ray","clinicstation":9},{"averageservicetime:"00:00:00","entries":[{"timein":"2017-07-11 00:02:58","waittime":"00:01:50","estwaittime":"00:01:50","patient":1,"routingslipentry":1}],"name":"Surgery Screening","clinicstation":10},{"averageservicetime:"00:00:00","entries":[{"timein":"2017-07-11 00:04:16","waittime":"00:00:32","estwaittime":"00:00:32","patient":6,"routingslipentry":16}],"name":"Speech","clinicstation":11},{"averageservicetime:"00:00:00","entries":[{"timein":"2017-07-11 00:04:37","waittime":"00:00:11","estwaittime":"00:00:11","patient":7,"routingslipentry":19}],"name":"Audiology","clinicstation":12}]}
```

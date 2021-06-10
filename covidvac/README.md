**Get COVID Vaccination by ID**
----
  Returns json data about a single COVID vaccination resource. 

* **URL**

  /tscharts/v1/covidvac/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":id,"name":string}
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/covidvac/49/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token 45bab35dca6c336fe1aa0be65526c7b436cdb6cd
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Thu, 10 Jun 2021 13:23:05 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

18
{"id":49,"name":"D0419"}
0
```
  
**Get Multiple COVID Vaccinations**
----
  Returns multiple COVID Vaccinations 

* **URL**

  /tscharts/v1/covidvac/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   None 

   One or more of the following can be specified to filter the search results.

   `name` string<br/>

   If no filters are supplied, the entire list of COVID vaccinations is returned.
   Note, a case sensitive exact match is performed on each of these search strings.

   **Optional:**

   None

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"id" : 1, "name": "name1"}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/covidvac/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token 45bab35dca6c336fe1aa0be65526c7b436cdb6cd
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Thu, 10 Jun 2021 13:23:06 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

4c
[{"id":56,"name":"BBBBB"},{"id":55,"name":"AAAAA"},{"id":54,"name":"CCCCC"}]
0
```

**Create a COVID Vaccination record**
----
  Create a COVID vaccination instance.

* **URL**

  /tscharts/v1/covidvac/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `name` string<br/>

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR
  `Entering a COVID vaccination that already exists in the database returns a 400 BAD REQUEST error response.
* **Example:**

```
POST /tscharts/v1/covidvac/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token 45bab35dca6c336fe1aa0be65526c7b436cdb6cd
Content-Length: 17

{"name": "D0419"}HTTP/1.1 200 OK
Date: Thu, 10 Jun 2021 13:23:05 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

9
{"id":49}
0

```

**Delete a COVID vaccination**
----
  Delete a COVID vaccination instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/covidvac/id

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
DELETE /tscharts/v1/covidvac/50/ HTTP/1.1
Host: localhost
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.24.0
Content-Type: application/json
Authorization: Token 45bab35dca6c336fe1aa0be65526c7b436cdb6cd
Content-Length: 2

{}HTTP/1.1 200 OK
Date: Thu, 10 Jun 2021 13:23:05 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, DELETE, HEAD, OPTIONS
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/json

2
{}
0
```

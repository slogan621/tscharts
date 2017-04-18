**Login**
----
  Login to the API service.  

* **URL**

  /tscharts/v1/login/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `username` name of the user<br />
   `password` password<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "token" : string, "id" : integer }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/login/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 48
Content-Type: application/json
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic


{"username": "**REMOVED**", "password": "**REMOVED**"}HTTP/1.0 200 OK
Date: Mon, 17 Apr 2017 05:36:24 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: POST, OPTIONS
Set-Cookie:  csrftoken=95wEL3Gj1yjRQVvjZ0coZSTpy0QrKrB7; expires=Mon, 16-Apr-2018 05:36:24 GMT; Max-Age=31449600; Path=/
Set-Cookie:  sessionid=93ld9694gslzb1tn8zjwh6hnjcgj0ff3; expires=Mon, 01-May-2017 05:36:24 GMT; httponly; Max-Age=1209600; Path=/


{"token": "b4e9102f85686ffffffffffffff7d377348hj8l", "id": "6"}
```

**Logout**
----
  Logout of the API service.  

* **URL**

  /tscharts/v1/logout/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

* **Example:**

```
POST /tscharts/v1/logout/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Content-Type: application/json
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic


{}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 07:31:57 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN
Content-Type: text/html; charset=utf-8
Allow: POST, OPTIONS
```

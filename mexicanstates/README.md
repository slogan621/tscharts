  
**Get Multiple Mexican States**
----
  Returns list of all Mexican states (unicode)

* **URL**

  /tscharts/v1/mexicanstates/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `["Aguascalientes",
                   "Baja California",
                   "Baja California Sur",
                   "Chihuahua",
                   "Colima", ...]`
 
* **Error Response:**

  * None

* **Example:**

```
GET /tscharts/v1/mexicanstates/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101

{}HTTP/1.0 200 OK
Date: Tue, 16 May 2017 01:40:05 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, HEAD, OPTIONS

["Aguascalientes","Baja California","Baja California Sur","Chihuahua","Colima","Campeche","Coahuila","Chiapas","Federal District","Durango","Guerrero","Guanajuato","Hidalgo","Jalisco","M..xico State","Michoac..n","Morelos","Nayarit","Nuevo Le..n","Oaxaca","Puebla","Quer..taro","Quintana Roo","Sinaloa","San Luis Potos..","Sonora","Tabasco","Tlaxcala","Tamaulipas","Veracruz","Yucat..n","Zacatecas"]
```
  

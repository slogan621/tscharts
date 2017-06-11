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
    **Content:** `[{"name":string,"awaytime":integer,"willreturn":UTC time string,"away":[true|false],"active":[true|false],"clinic":id,"station":id,"id":id,"level":integer}, ...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
```

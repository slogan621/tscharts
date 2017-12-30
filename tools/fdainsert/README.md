   **Update FDA Drug List**
----
  Update the current drug list in the database.

* **Get @FDA Data Files:**

  Go to the website https://www.fda.gov/Drugs/InformationOnDrugs/ucm079750.htm and download the last updated Drugs@FDA zip file. 
  Unzip the zip file. The Products.txt file contains all the FDA certified drugnames. 

* **Setup:**

  Open the terminal window, go to the tscharts file directory and use the command "typeset -x PYTHONPATH=pwd" to setup Python path.
  For example: ~/tscharts$ typeset -x PYTHONPATH=pwd 

  Copy the Products.txt file downloaded from FDA website to the fdainsert directory under tools directory.

* **Login:**
  
  Go to the /tscharts/tools/fdainsert directory and use following command to login and run the program: python fdainsert.py -u 'username' -w 'password' -h 'host' -p 'port' -f 'filename'

  Filename is the name of the FDA data file stored under the fdainsert directory.

  For example: ~/tscharts/tools/fdainsert$ python fdainsert.py -u myname -w mypassword -h 53.193.98.902 -p 80 -f Products.txt
  
*  **APIs**
   
   * The medications APIs are used here to add new drugs and return current drug list.

   * The POST method adds new drug into the database. The drugs stored in the database will not be deleted. No duplicate drugs in the database.

   * **Example:**
   ```
   POST /tscharts/v1/medications/ HTTP/1.1
   Host: 54.193.67.202
   Connection: keep-alive
   Accept-Encoding: gzip, deflate
   Accept: */*
   User-Agent: python-requests/2.18.4
   Content-Type: application/json
   Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
   Content-Length: 17

   {"name": "Advil"}HTTP/1.1 200 OK
   Date: Tue, 26 Dec 2017 20:40:57 GMT
   Server: Apache/2.4.7 (Ubuntu)
   Vary: Accept
   X-Frame-Options: SAMEORIGIN
   Content-Length: 10
   Allow: GET, POST, DELETE, HEAD, OPTIONS
   Keep-Alive: timeout=5, max=100
   Connection: Keep-Alive
   Content-Type: application/json

   {"id":187}
   ```
   * The GET method retrieves the entire drug list stored in the database. 

   * **Example:**
   ```
   GET /tscharts/v1/medications/ HTTP/1.1
   Host: 54.193.67.202
   Connection: keep-alive
   Accept-Encoding: gzip, deflate
   Accept: */*
   User-Agent: python-requests/2.18.4
   Content-Type: application/json
   Authorization: Token f029f2e53dd2c0ef685dcfd1ab8f53e410ccfede
   Content-Length: 2

   {}HTTP/1.1 200 OK
   Date: Tue, 26 Dec 2017 20:40:58 GMT
   Server: Apache/2.4.7 (Ubuntu)
   Vary: Accept
   X-Frame-Options: SAMEORIGIN
   Content-Length: 16
   Allow: GET, POST, DELETE, HEAD, OPTIONS
   Keep-Alive: timeout=5, max=100
   Connection: Keep-Alive
   Content-Type: application/json

   ["b","bc","bbc"]
   ```
   For information about medications APIs, please check the followings:
   * [API](../master/medications/README.md)
   * [Unit Tests](../master/test/medications/medications.py)

* **Success Output Examples:**

  * The success output prints out:
    1)The current number of drugs in the FDA file. 
    2)The number of added new drugs and their names.
    3)The number of drugs in the current druglist.

  * The number of drugs in the current druglist maybe bigger than the number of drugs in the FDA file because the drugs deleted from the FDA file will not be deleted from our database.

  * **No New Drugs Inserted** 
  ```
  Current fda file(fdaproducts12:26:2017.txt) contains 7007 drugs.
  Updating drug list...
  No new added drugs.
  Current drug list contains 7014 drugs.
  ```
  * **New Drugs Inserted**
  ```
  Current fda file(fdaproducts12:26:2017.txt) contains 7007 drugs.
  Updating drug list...
  There are 3 added new drugs: ADVIL, LIQUAEMIN SODIUM, HISTAMINE.
  Current drug list contains 7014 drugs. 
  ```

**Purpose**
----
This script is used to truncate database tables prior to unit tests being
run. DO NOT USE THIS SCRIPT on a production system with actual patient data.

**Usage**

$ mysql -u root -p < cleardb.txt

You will be prompted for the database password. 


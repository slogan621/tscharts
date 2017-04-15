Patient service

patient
   get 
/tscharts/v1/patient/id/
   returns patient with given ID
/tscharts/v1/patient/
   {search terms (clinic id, patient id, name, gender, DOB, etc.)}
   above parameters filter if present
   returns array of patient ids
   post
/tscharts/v1/patient/
   {...}
   returns array of patient ids (same as above but with empty search terms)
   put
/tscharts/v1/patient/id/
   {...}
   delete
/tscharts/v1/patient/id/

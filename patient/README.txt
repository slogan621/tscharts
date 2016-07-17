Patient service

patient
   get 
/tscharts/patient/id
   returns patient with given ID
/tscharts/patient
   {search terms (clinic id, patient id, name, gender, DOB, etc.)}
   above parameters filter if present
   returns array of patient ids
   post
/tscharts/patient 
   {...}
   returns array of patient ids (same as above but with empty search terms)
   put
/tscharts/patient/id
   {...}
   delete
/tscharts/patient/id

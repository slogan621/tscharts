Patient service

patient
   get 
/tscharts/patient/id
   returns patient with given ID
   post
/tscharts/patient 
   {...}
   returns patient id 
   put
/tscharts/patient/id
   {...}
   delete
/tscharts/patient/id
patients
   get
/tscharts/patients
   {search terms (clinic id, patient id, name, gender, DOB, etc.)}
   above parameters filter if present
   returns array of patient ids

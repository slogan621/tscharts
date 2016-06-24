Registration service

registration
   get 
/tscharts/registration/id
   returns registration with given ID
/tscharts/registration
   {patient_id:id, clinic_id:id}
   above parameters filter if present
   returns array of registration ids
   post
/tscharts/registration 
   {patient_id:id, clinic_id:id}
   returns registration id 
   delete
/tscharts/registration/id

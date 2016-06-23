Registration service

registration
   get 
/tscharts/registration/id
   returns registration with given ID
   post
/tscharts/registration 
   {patient_id:id, clinic_id:id, ....}
   returns registration id 
   put
/tscharts/registration/id
   {....}
   delete
/tscharts/registration/id
registrations
   get
/tscharts/registrations
   {patient_id:id, clinic_id:id}
   above parameters filter if present
   returns array of registration ids


Medical history service

medicalhistory
   get 
/tscharts/medicalhistory/id
   returns medical history with given ID
/tscharts/medicalhistory
   {patient_id:id, clinic_id:id}
   above parameters filter if present
   returns array of medical history ids
   post
/tscharts/medicalhistory 
   {patient_id:id, clinic_id:id, ...}
   returns medical history id 
   put
/tscharts/medicalhistory/id
   {...}
   delete
/tscharts/medicalhistory/id

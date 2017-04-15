Medical history service

medicalhistory
   get 
/tscharts/v1/medicalhistory/id/
   returns medical history with given ID
/tscharts/v1/medicalhistory/
   {patient_id:id, clinic_id:id}
   above parameters filter if present
   returns array of medical history ids
   post
/tscharts/v1/medicalhistory/
   {patient_id:id, clinic_id:id, ...}
   returns medical history id 
   put
/tscharts/v1/medicalhistory/id/
   {...}
   delete
/tscharts/v1/medicalhistory/id/

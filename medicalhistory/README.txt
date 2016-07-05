Medical history service

medhist
   get 
/tscharts/medhist/id
   returns medical history with given ID
/tscharts/medhist
   {patient_id:id, clinic_id:id}
   above parameters filter if present
   returns array of medical history ids
   post
/tscharts/medhist 
   {patient_id:id, clinic_id:id, ...}
   returns medical history id 
   put
/tscharts/medhist/id
   {...}
   delete
/tscharts/medhist/id

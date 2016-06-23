Return to clinic service

returntoclinic
   get 
/tscharts/returntoclinic/id
   returns returntoclinic with given ID
   post
/tscharts/returntoclinic 
   {patient_id:id, current_clinic_id:id, [return_date:date | interval:number_of_months]}
   returns returntoclinic id 
   put
/tscharts/returntoclinic/id
   {....}
   delete
/tscharts/returntoclinic/id
returntoclinics
   get
/tscharts/returntoclinics
   {patient_id:id, clinic_id:id}
   above parameters filter if present
   returns array of return to clinic ids


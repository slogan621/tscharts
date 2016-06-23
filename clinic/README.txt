Clinic service

clinic
   get 
/tscharts/clinic/id
   returns clinic with given ID
   post
/tscharts/clinic 
   {location:location, start:date, end:date}
   returns clinic id 
   delete
/tscharts/clinic/id
clinics
   get
/tscharts/clinic
   {year:id, location:id}
   above parameters filter if present
   returns array of clinic ids


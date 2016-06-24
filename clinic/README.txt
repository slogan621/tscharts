Clinic service

clinic
   get 
/tscharts/clinic/id
   returns clinic with given ID
/tscharts/clinic
   {year:year, location:id}
   above parameters filter if present
   returns array of clinic ids
   post
/tscharts/clinic 
   {location:location, start:date, end:date}
   returns clinic id 
   delete
/tscharts/clinic/id

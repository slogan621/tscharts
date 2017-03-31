Return to clinic service

returntoclinic
   get 
/tscharts/returntoclinic/id
   returns returntoclinic with given ID
   {patient:id, clinic:id, interval:number_of_months, month:integer, year:integer}
   In above, month is in range [1-12], year is 4 digit e.g., 2017
/tscharts/returntoclinic
   {patient:id, clinic:id}
   above parameters filter if present
   returns array of return to clinic ids
   post
/tscharts/returntoclinic 
   {patient:id, clinic:id, interval:number_of_months}
   returns returntoclinic id 
   put
/tscharts/returntoclinic/id
   {....}
   delete
/tscharts/returntoclinic/id


Routing slip service

routingslip
   get 
/tscharts/routinglslip/id
   returns routing slip with given ID
   post
/tscharts/routingslip 
   {patient_id:id, clinic_id:id, ....}
   returns routing slip id 
   put
/tscharts/routingslip/id
   delete
/tscharts/routingslip/id
routingslips
   get
/tscharts/routingslips
   {patient_id:id, clinic_id:id}
   above parameters filter if present
   returns array of routing slip ids

Registration service

register
   get 
/tscharts/v1/register/id/
   returns registration with given ID
   includes state and timestamps
/tscharts/v1/register/
   {patient:id, clinic:id, state:state}
   above parameters filter if present
   returns array of registration objects
   post
/tscharts/v1/register/
   {patient_id:id, clinic_id:id}
   sets state to "Checked In"
   returns registration id 
   put
/tscharts/v1/register/id/
   {state:state}
   delete                    # should not be used in normal circumstances
/tscharts/v1/register/id/

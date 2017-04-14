Registration service

registration
   get 
/tscharts/registration/id
   returns registration with given ID
   includes state and timestamps
/tscharts/registration
   {patient:id, clinic:id, state:state}
   above parameters filter if present
   returns array of registration objects
   post
/tscharts/registration 
   {patient_id:id, clinic_id:id}
   sets state to "Checked In"
   returns registration id 
   put
/tscharts/registration/id 
   {state:state}
   delete                    # should not be used in normal circumstances
/tscharts/registration/id

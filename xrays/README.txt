xrays service

xray
   get 
/tscharts/v1/xray/id/
   returns xray with given ID
/tscharts/v1/xray/
   {patient_id:id, clinic_id:id, sort:[true|false]}
   above parameters filter if present
   returns base64 content
   post
/tscharts/v1/xray/
   {patient_id:id, clinic_id:id, xray:base64}
   returns xray id 
   put
/tscharts/v1/xray/id/
   {xray:base64}
   delete
/tscharts/v1/xray/id/

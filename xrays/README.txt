xrays service

xray
   get 
/tscharts/xray/id
   returns xray with given ID
   post
/tscharts/xray 
   {patient_id:id, clinic_id:id, xray:base64}
   returns xray id 
   put
/tscharts/xray/id
   {xray:base64}
   delete
/tscharts/xray/id
xrays
   get
/tscharts/xrays
   {patient_id:id, clinic_id:id, sort:[true|false]}
   above parameters filter if present
   returns base64 content

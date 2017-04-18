image service

image
   get 
/tscharts/v1/image/id/
   returns base64 image with given ID
/tscharts/v1/image/
   {patient:id, type:type, clinic:id, station:id}
   above parameters filter if present
   see below for definition of "type"
   returns list of image ids
   post
/tscharts/v1/image/
   {patient:id, clinic:id, type:type, station:id, data:base64}
   type must be one of the following strings:
   "Xray" - image is an xray
   "Headshot" - image is a headshot taken at registration
   "Surgery" - image is from a surgery
   File a bug if additional image types are needed.
   returns image id 
   delete
/tscharts/v1/image/id/

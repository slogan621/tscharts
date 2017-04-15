StateChange service

statechange
   get 
/tscharts/v1/statechange/id/
   returns statechange object with given ID
/tscharts/v1/statechange/
   optional search terms: 
   {patient:id, clinicstation:id, clinic:id}
   legal combination of search terms:
   patient and clinicstation -- patient activity for a specific clinicstation
   patient and clinic -- patient activity for a specific clinic, all stations
   clinicstation - activity for a specific clinicstation, all patients
   clinic - activity at a specific clinic, all stations, all patients
   returns array of statechange objects
   post
/tscharts/v1/statechange/
   {patient:id, clinicstation:id, state:["in" | "out"]}
   returns statechange id 
   put
/tscharts/v1/statechange/id/
   {state:["in" | "out"]}
   delete // normally applications should not delete statechange objects
/tscharts/v1/statechange/id/

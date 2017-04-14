ClinicStation service

clinicstation
   get 
/tscharts/clinicstation/id
   returns clinicstation with given ID
   {clinic:clinic_id, station:station_id, active:[true|false], level:integer}
/tscharts/clinicstation
   returns array of clinicstations
   post
/tscharts/clinicstation 
   Payload contains one or more of the following:
   clinic:clinic_id  -- required
   station:station_id  -- required
   active:[true|false]  -- make the clinicstation active or not. Might set
                           this to false when station takes a lunch break
   level:integer -- scheduling priority of station. clinicstations with same 
                    level can be scheduled equally, those with lower
                    levels must be scheduled before those with higher levels.
   Example:
   {clinic:clinic_id, station:station_id, active:[true|false], level:integer}
   returns clinicstation id 
   put
/tscharts/clinicstation/id 
   Payload is one or more of the following:
   active:[true|false]  -- make the clinicstation active or not. Might set
                           this to false when station takes a lunch break
   level:integer -- scheduling priority of station. clinicstations with same 
                    level can be scheduled equally, those with lower
                    levels must be scheduled before those with higher levels.
   Example:
   {active:true, level:5}
   returns clinicstation id 
   delete
/tscharts/clinicstation/id

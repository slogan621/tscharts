Routing slip service

Routing slip is a list of station IDs associated with a clinic and patient.

routingslip
   get 
/tscharts/routingslip
   {clinic_id:id}
   returns array of routing slip ids
/tscharts/routingslip/id
   returns routing slip with given ID (see blow)
/tscharts/routingslip
   {patient_id:id, clinic_id:id}
   both clinic_id and patient_id are required

The last two of the above return data as following:
   { 
     -- routing slip id
     id: id
     -- how patient was categorized at registration (or later)
     category: category,   
     -- array of routing slip entries in order of visitation
     routing: [                  
                 {
                  station: id,
                  state: state
                 },
                 ...
              ],

      -- array of comments in timestamp order
      comments: [ 
                    {
                     author: id,
                     timestamp: datetime,
                     comment: comment_text
                    },
                    ...
                ]
    }
   post
/tscharts/routingslip 
   {
    patient_id: id, -- required
    clinic_id: id,  -- required
    category: categoryid,  -- optional, but typically supplied
    routing: [ordered array of clinicstation ids] -- optional
   }
   returns routing slip id 
   put
/tscharts/routingslip/id
   -- at least one of the fields in below payload must be present or param error
   {
    category: category,    -- change category of patient
    routing: [ordered array of clinicstation ids],  -- change routing order
    state: {clinicstation:id, state:state} -- change state of an entry
    comment: {author:id, comment:text} -- add a comment
   }
   delete
/tscharts/routingslip/id

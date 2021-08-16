#!/bin/bash

#(C) Copyright Syd Logan 2021
#(C) Copyright Thousand Smiles Foundation 2021
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

dbpass=$1

target=./tscharts-output
sqlfiles=/var/lib/mysql-files
db=tscharts

DBS=(
"audiogram_audiogram"
"category_category"
"clinic_clinic"
"clinicstation_clinicstation"
"consent_consent"
"dentalcdt_dentalcdt"
"dentalstate_dentalstate"
"dentaltreatment_dentaltreatment"
"entdiagnosis_entdiagnosis"
"entdiagnosisextra_entdiagnosisextra"
"entexam_entexam"
"enthistory_enthistory"
"enthistoryextra_enthistoryextra"
"entsurgicalhistory_entsurgicalhistory"
"enttreatment_enttreatment"
"image_image"
"medicalhistory_medicalhistory"
"medications_medications"
"patient_patient"
"queue_queue"
"queue_queueentry"
"queue_queuestatus"
"register_register"
"registration_registrationprofile"
"returntoclinic_returntoclinic"
"returntoclinicstation_returntoclinicstation"
"routingslip_routingslip"
"routingslip_routingslipcomment"
"routingslip_routingslipentry"
"statechange_statechange"
"station_station"
"surgeryhistory_surgeryhistory"
"surgerytype_surgerytype"
"xray_xray")

sudo mkdir -p $target
sudo chmod 777 $target
for x in ${DBS[@]}
do
    sudo mysqldump -u root -p$dbpass -t -T$sqlfiles $db $x --fields-terminated-by=__
    mysql -u root -p$dbpass -e "use $db; describe $x;" > $target/$x-schema.txt
    python headers.py $target/$x-schema.txt > $target/$x-headers.txt
    sudo cat $target/$x-headers.txt $sqlfiles/$x.txt > $target/$x-final.txt
done

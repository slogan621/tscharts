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

import pandas as pd

df = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/register_register-final.txt', encoding="latin-1", sep="__")

clinicdf = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/clinic_clinic-final.txt', encoding="latin-1", sep="__")

patientdf = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/patient_patient-final.txt', encoding="latin-1", sep="__")

routingslipdf = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/routingslip_routingslip-final.txt', encoding="latin-1", sep="__")

patientdf = patientdf.rename(columns={"id": "patient_id"})
clinicdf = clinicdf.rename(columns={"id": "clinic_id"})

# drop the first 11 rows, these were earlier clinics with restarts and
# not worth processing

N = 11

clinicdf = clinicdf.iloc[N: , :]

result = pd.merge(df, patientdf, on="patient_id")

result = pd.merge(result, routingslipdf, on=["clinic_id", "patient_id"])

di = {'d': "Dental", 'r': "Returning Cleft", 'n': "New Cleft", 'o': "Ortho", 't': "Other", 'u': "Unknown", 'h': "Hearing Aids", 'e': "Ears"}

result = result.replace({"category": di})

result.to_csv('registrations.csv', encoding='utf-8')

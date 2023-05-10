#(C) Copyright Thousand Smiles Foundation 2023
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


#DataFrames begin with prefix "df_" and can be found easily with Auto Complete
#FileLocations bigeing with prefix "file_loc_"

import pandas as pd

#from os import listdir
#from os.path import isfile, join
#This could be improved as a way of locating the original data files
#mypath = '../../../../../1000_Smiles/Data/'
#print(listdir(mypath))

#centralized location for file paths
file_prefix = '../../../../../1000_Smiles/Data/tscharts-output/'
file_loc_clinic = file_prefix+'clinic_clinic-final.txt'
file_loc_register = file_prefix+'register_register-final.txt'
file_loc_patient = file_prefix+'patient_massaged-final.txt'
file_loc_images = file_prefix+'image_image-final.txt'
file_loc_history = file_prefix+'medicalhistory_medicalhistory-final.txt'
file_loc_routing = file_prefix+'routingslip_routingslip-final.txt'

df_clinic = pd.read_csv(file_loc_clinic, encoding="latin-1", sep="__", engine ='python')
N = 11 
# drop the first 11 rows, these were earlier clinics with restarts and
# not worth displaying
df_clinic = df_clinic.iloc[N: , :]

#merged dataframes - patients
df_register = pd.read_csv(file_loc_register, encoding="latin-1", sep="__", engine ='python')
df_merged = pd.merge(df_register, df_clinic, left_on="clinic_id", right_on="id")
df_patient = pd.read_csv(file_loc_patient, encoding="latin-1", sep="__", engine="python")
df_merged = pd.merge(df_patient, df_merged, left_on="id", right_on="patient_id")


#clinic dataframes
df_images = pd.read_csv(file_loc_images, encoding="latin-1", sep="__", engine="python")
df_headshot = df_images.copy(deep=True)
df_headshot = df_headshot[df_headshot['imagetype'] == 'h']
df_headshot['clinic_id'] = df_headshot['clinic_id'].map(df_clinic.set_index('id')['start'])

df_xray = df_images.copy(deep=True)
df_xray = df_xray[df_xray['imagetype'] == 'x']
df_xray['clinic_id'] = df_xray['clinic_id'].map(df_clinic.set_index('id')['start'])




df_routing = pd.read_csv(file_loc_routing, encoding="latin-1", sep="__", engine="python")
di = {'d': "Dental", 'r': "Returning Cleft", 'n': "New Cleft", 'o': "Ortho", 't': "Other", 'u': "Unknown", 'h': "Hearing Aids", 'e': "Ears"}
df_routing = df_routing.replace({"category": di})
df_routing['clinic_id'] = df_routing['clinic_id'].map(df_clinic.set_index('id')['start'])


#medical history
df_medical = pd.read_csv(file_loc_history, encoding="latin-1", sep="__", engine="python")
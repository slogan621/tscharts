import pandas as pd

#from os import listdir
#from os.path import isfile, join
#This could be improved as a way of locating the original data files
#mypath = '../../../../../1000_Smiles/Data/'
#print(listdir(mypath))

#centralized location for file paths
file_prefix = '../../../../../1000_Smiles/Data/'
file_loc = file_prefix+'tscharts-output/clinic_clinic-final.txt'
file_loc2 = file_prefix+'tscharts-output/register_register-final.txt'
file_loc3 = file_prefix+'tscharts-output/patient_massaged-final.txt'
file_loc4 = file_prefix+'tscharts-output/image_image-final.txt'
file_loc5 = file_prefix+'tscharts-output/medicalhistory_medicalhistory-final.txt'

clinic_df = pd.read_csv(file_loc, encoding="latin-1", sep="__", engine ='python')
N = 11 
# drop the first 11 rows, these were earlier clinics with restarts and
# not worth displaying
clinic_df = clinic_df.iloc[N: , :]

#merged dataframes - patients
register_df = pd.read_csv(file_loc2, encoding="latin-1", sep="__", engine ='python')
merged_df = pd.merge(register_df, clinic_df, left_on="clinic_id", right_on="id")
patient_df = pd.read_csv(file_loc3, encoding="latin-1", sep="__", engine="python")
merged_df = pd.merge(patient_df, merged_df, left_on="id", right_on="patient_id")


#clinic dataframes
headshot_df = pd.read_csv(file_loc4, encoding="latin-1", sep="__", engine="python")
headshot_df = headshot_df[headshot_df['imagetype'] == 'h']
headshot_df['clinic_id'] = headshot_df['clinic_id'].map(clinic_df.set_index('id')['start'])

#medical history
medical_df = pd.read_csv(file_loc5, encoding="latin-1", sep="__", engine="python")
#(C) Copyright Syd Logan 2023
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

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

def compute_age(row):
    d1 = datetime.strptime(row["start"], "%Y-%m-%d")
    d2 = datetime.strptime(row["dob"], "%Y-%m-%d")
    diff_in_years = relativedelta(d1, d2)
    return diff_in_years.years

# drop the first 11 rows, these were earlier clinics with restarts and
# not worth displaying

N = 11

clinicdf = pd.read_csv('tscharts-output/clinic_clinic-final.txt', encoding="latin-1", sep="__")
clinicdf = clinicdf.iloc[N: , :]

registerdf = pd.read_csv('tscharts-output/register_register-final.txt', encoding="latin-1", sep="__")

merged_df = pd.merge(registerdf, clinicdf, left_on="clinic_id", right_on="id")

patientdf = pd.read_csv('tscharts-output/patient_massaged-final.txt', encoding="latin-1", sep="__")

merged_df = pd.merge(patientdf, merged_df, left_on="id", right_on="patient_id")

# use a lambda to create a new row, which is age in years of patient

merged_df["age_in_years"] = merged_df.apply(lambda row: compute_age(row), axis=1)

print(merged_df)

merged_df['age_in_years'].value_counts().plot(kind='bar', alpha=0.75, rot=0)
plt.title("Number of Registrations By Age (freq)")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

merged_df['age_in_years'].value_counts().sort_index().plot(kind='bar', alpha=0.75, rot=0)
plt.title("Number of Registrations By Age (age)")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()


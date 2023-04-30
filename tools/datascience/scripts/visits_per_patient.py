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

# drop the first 11 rows, these were earlier clinics with restarts and
# not worth displaying

N = 11

clinicdf = pd.read_csv('tscharts-output/clinic_clinic-final.txt', encoding="latin-1", sep="__")
clinicdf = clinicdf.iloc[N: , :]

patientdf = pd.read_csv('tscharts-output/patient_massaged-final.txt', encoding="latin-1", sep="__")
registerdf = pd.read_csv('tscharts-output/register_register-final.txt', encoding="latin-1", sep="__")

merged_df = pd.merge(registerdf, clinicdf, left_on="clinic_id", right_on="id").drop_duplicates(subset=["clinic_id", "patient_id"])

merged_df = pd.merge(patientdf, merged_df, left_on="id", right_on="patient_id")

count_df = merged_df.groupby("patient_id").count();

count_df["id"].plot(kind='hist', edgecolor='k', color='c', alpha=0.75, rot=0)
plt.title("Number of Clinic Visits Per Patient")
plt.xlabel("Count")
plt.ylabel("Visits")
plt.show()

# TODO correlate this to reason for visit, e.g., dental, cleft, etc. Bet most return patients are cleft.


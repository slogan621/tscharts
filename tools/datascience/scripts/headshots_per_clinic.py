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

df = pd.read_csv('tscharts-output/image_image-final.txt', encoding="latin-1", sep="__")

df = df[df['imagetype'] == 'h']

# drop the first 11 rows, these were earlier clinics with restarts and
# not worth displaying

clinicdf = pd.read_csv('tscharts-output/clinic_clinic-final.txt', encoding="latin-1", sep="__")

N = 11
clinicdf = clinicdf.iloc[N: , :]

df['clinic_id'] = df['clinic_id'].map(clinicdf.set_index('id')['start'])

df['clinic_id'].value_counts().sort_index().plot(kind='bar', alpha=0.75, rot=0)
plt.title("Headshots taken per Clinic")
plt.xlabel("Clinic ID")
plt.ylabel("Count")
plt.show()


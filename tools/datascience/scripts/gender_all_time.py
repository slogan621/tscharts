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
import matplotlib.pyplot as plt

df = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/patient_patient-final.txt', encoding="latin-1", sep="__")

di = {'m': "Male", 'f': "Female"}
df = df.replace({"gender": di})

df['gender'].value_counts().plot(kind='bar', alpha=0.75, rot=0)
plt.title("Patients by Gender (All Time)")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()


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

df = pd.read_csv('tscharts-output/routingslip_routingslip-final.txt', encoding="latin-1", sep="__")

clinicdf = pd.read_csv('tscharts-output/clinic_clinic-final.txt', encoding="latin-1", sep="__")

di = {'d': "Dental", 'r': "Returning Cleft", 'n': "New Cleft", 'o': "Ortho", 't': "Other", 'u': "Unknown", 'h': "Hearing Aids", 'e': "Ears"}
df = df.replace({"category": di})

df['category'].value_counts().sort_index().plot(kind='bar', alpha=0.75, rot=0)
plt.title("Routing Slips by Patient Category (All Time)")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()

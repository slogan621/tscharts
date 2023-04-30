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

df = pd.read_csv('tscharts-output/medicalhistory_medicalhistory-final.txt', encoding="latin-1", sep="__")

df = df[["cold_cough_fever", "hivaids", "anemia", "athsma", "cancer", "congenitalheartdefect", "diabetes", "epilepsy", "bleeding_problems", "hepititis", "tuberculosis", "troublespeaking", "troublehearing", "troubleeating", "born_with_cleft_lip", "born_with_cleft_palate"]].sum()

print(df)

df.plot(kind='bar', alpha=0.75, colormap="Paired", stacked=True) 
#plt.legend(["cold_cough_fever", "hivaids", "anemia", "athsma", "cancer", "congenitalheartdefect", "diabetes", "epilepsy", "bleeding_problems", "hepititis", "tuberculosis", "troublespeaking", "troublehearing", "troubleeating", "born_with_cleft_lip", "born_with_cleft_palate"])
plt.title("Medical Conditions (All Time)")
plt.show()


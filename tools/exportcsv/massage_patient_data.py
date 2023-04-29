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

import pandas
import numpy as np

# read in exported data

df = pandas.read_csv("patient_patient-final.txt", sep="__", engine="python")

# remove personal identifying info from dataframe

massaged = df.drop(['paternal_last', 'maternal_last', 'first', 'middle', 'suffix', 'prefix', 'street1', 'street2', 'phone1', 'phone2', 'email', 'emergencyfullname', 'emergencyphone', 'emergencyemail', 'curp', 'oldid'], axis=1)

# pandas does not support export with multi-char delimiters, but numpy
# does so convert to numpy and save

np_data = massaged.to_numpy()
np.savetxt("patient_massaged.txt", np_data, fmt="%s", delimiter="__")


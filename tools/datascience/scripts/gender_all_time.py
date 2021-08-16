import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/patient_patient-final.txt', encoding="latin-1", sep="__")

di = {'m': "male", 'f': "female"}
df = df.replace({"gender": di})

df['gender'].value_counts().plot(kind='bar')
plt.title("Patients by Gender (All Time)")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()

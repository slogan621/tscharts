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


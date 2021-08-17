import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/register_register-final.txt', encoding="latin-1", sep="__")

# drop the first 11 rows, these were earlier clinics with restarts and
# not worth displaying

N = 11
df = df.iloc[N: , :]

clinicdf = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/clinic_clinic-final.txt', encoding="latin-1", sep="__")

clinicdf = clinicdf.iloc[N: , :]

df['clinic_id'] = df['clinic_id'].map(clinicdf.set_index('id')['start'])

df['clinic_id'].value_counts().sort_index().plot(kind='bar', alpha=0.75, rot=0)
plt.title("Registrations per Clinic")
plt.xlabel("Clinic ID")
plt.ylabel("Count")
plt.show()


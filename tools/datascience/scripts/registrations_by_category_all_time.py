import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/routingslip_routingslip-final.txt', encoding="latin-1", sep="__")

clinicdf = pd.read_csv('~/thousandsmiles/analysis/08-2021/tscharts-output/clinic_clinic-final.txt', encoding="latin-1", sep="__")

di = {'d': "Dental", 'r': "Returning Cleft", 'n': "New Cleft", 'o': "Ortho", 't': "Other", 'u': "Unknown", 'h': "Hearing Aids", 'e': "Ears"}
df = df.replace({"category": di})

df['category'].value_counts().sort_index().plot(kind='bar', alpha=0.75, rot=0)
plt.title("Routing Slips by Patient Category (All Time)")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()

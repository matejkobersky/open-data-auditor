import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = {
    'Město/Země': ['Praha', 'Brno', 'Ostrava', 'Liberec', 'Jihlava', 'Paříž (FR)', 'Británie (UK)', 'USA', 'Estonsko', 'Slovensko', 'Polsko'],
    'Chybějící data (%)': [7.7, 0.0, 54.8, 26.2, 2.8, 12.3, 0.5, 3.3, 23.6, 15.8, 6.3],
    'Oddělovač': ['Středník', 'Čárka', 'Čárka', 'Čárka', 'Čárka', 'Středník', 'Čárka', 'Čárka', 'Středník', 'Středník', 'Čárka'],
    'Kódování': ['UTF-8', 'UTF-8', 'UTF-8', 'UTF-8', 'UTF-8', 'UTF-8', 'CP1250/Win', 'UTF-8', 'UTF-8', 'CP1250/Win', 'UTF-8']
}
df = pd.DataFrame(data)

plt.style.use('ggplot')

plt.figure(figsize=(12, 6))
df_sorted = df.sort_values('Chybějící data (%)', ascending=False)
bars = plt.bar(df_sorted['Město/Země'], df_sorted['Chybějící data (%)'], color='steelblue')

for i, val in enumerate(df_sorted['Chybějící data (%)']):
    if val > 20:
        bars[i].set_color('firebrick')

plt.title('Kvalita otevřených dat: Podíl chybějících hodnot', fontsize=14)
plt.ylabel('Chybějící data (%)', fontsize=12)
plt.xlabel('Subjekt', fontsize=12)

plt.axhline(y=20, color='red', linestyle='--', label='Limit kritické kvality (20%)')
plt.legend()
plt.tight_layout()
plt.savefig('graf_kvalita.png', dpi=300)
print("Graf 1 uložen: graf_kvalita.png")

plt.figure(figsize=(8, 6))
counts = df['Oddělovač'].value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999'])
plt.title('Interoperabilita: Používané oddělovače v CSV', fontsize=14)
plt.tight_layout()
plt.savefig('graf_oddelovace.png', dpi=300)
print("Graf 2 uložen: graf_oddelovace.png")

plt.figure(figsize=(8, 6))
counts_enc = df['Kódování'].value_counts()
plt.pie(counts_enc, labels=counts_enc.index, autopct='%1.1f%%', startangle=140, colors=['mediumseagreen', 'lightcoral'])
plt.title('Standardizace: Kódování znaků', fontsize=14)
plt.tight_layout()
plt.savefig('graf_kodovani.png', dpi=300)
print("Graf 3 uložen: graf_kodovani.png")

print("\nHotovo! Ve složce projektu máte 3 nové obrázky v profesionálním rozlišení.")
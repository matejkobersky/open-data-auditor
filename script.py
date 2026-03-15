import pandas as pd
import os

datasets = [
    ("Praha (CZ)", "Praha.csv"),
    ("Brno (CZ)", "Brno.csv"),
    ("Ostrava (CZ)", "Ostrava.csv"),
    ("Liberec (CZ)", "Liberec.csv"),
    ("Jihlava (CZ)", "Jihlava.csv"),

    # SVĚT
    ("Paříž (FR)", "Pariz.csv"),
    ("Británie (UK)", "Britanie.csv"),
    ("USA (US)", "USA.csv"),
    ("Estonsko (EE)", "Estonsko.csv"),
    ("Slovensko (SK)", "Slovensko.csv"),
    ("Polsko (PL)", "Polsko.csv")
]


def analyze_dataset(filename, name):
    print(f"Analyzuji: {name}...")

    res = {
        "Subjekt": name,
        "Dostupnost": "ANO",
        "Kódování": "Neznámé",
        "Oddělovač": "?",
        "Validní CSV": "NE",
        "Kvalita (Missing)": "-",
        "Poznámka": ""
    }

    if not os.path.exists(filename):
        res["Dostupnost"] = "NE (Chybí)"
        res["Poznámka"] = "Soubor nenalezen"
        return res

    configs = [
        ('utf-8', ','), ('utf-8', ';'),
        ('cp1250', ';'), ('cp1250', ','),
        ('latin1', ','), ('latin1', ';'),
        ('cp1252', ','), ('cp1252', ';')
    ]

    df = None

    for enc, sep in configs:
        try:
            test = pd.read_csv(filename, sep=sep, encoding=enc, nrows=2)
            if len(test.columns) > 1:
                df = pd.read_csv(filename, sep=sep, encoding=enc, on_bad_lines='skip')
                res["Kódování"] = enc.upper()
                res["Oddělovač"] = "Středník (;)" if sep == ';' else "Čárka (,)"
                res["Validní CSV"] = "ANO"
                break
        except:
            continue

    if df is not None:
        missing = df.isnull().sum().sum()
        total = df.size
        if total > 0:
            res["Kvalita (Missing)"] = f"{(missing / total) * 100:.1f} %"

        ukazka = str(df.head(3))
        if '£' in ukazka: res["Poznámka"] += "Měna v textu (£). "
        if '€' in ukazka: res["Poznámka"] += "Měna v textu (€). "

    return res

final_results = []
print("--- SPUŠTĚNÍ MASIVNÍ ANALÝZY PRO BAKALÁŘSKOU PRÁCI ---")

for name, file in datasets:
    vysledek = analyze_dataset(file, name)
    final_results.append(vysledek)

df_final = pd.DataFrame(final_results)
print("\n" + "=" * 130)
print("VÝSLEDKY MEZINÁRODNÍHO SROVNÁNÍ")
print("=" * 130)
print(df_final.to_string(index=False))
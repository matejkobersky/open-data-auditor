# Open Data Auditor & Analytics

Tento repozitář obsahuje softwarové nástroje a analytické skripty vyvinuté v rámci bakalářské práce na **Provozno ekonomické fakultě ČZU**. Projekt se zaměřuje na audit kvality otevřených dat (formát CSV) a jejich srovnání v mezinárodním kontextu.

---

## 📁 Struktura projektu

Projekt je rozdělen do dvou hlavních částí:

1.  **Praktická aplikace (Auditor):** Nástroj pro úředníky a kurátory dat k rychlé kontrole souborů před publikací.
    - `main.py`: Hlavní spouštěcí soubor aplikace.
    - `graphs.py`: Modul pro generování dashboardu v rámci GUI.
    - `translations.py`: Lokalizace rozhraní (CZ/EN).
2.  **Analytická část (Výzkum):** Skripty použité pro hloubkové srovnání 11 subjektů (Praha, Brno, Estonsko, USA atd.).
    - `script.py`: Výpočetní logika a statistické srovnání.
    - `grafy.py`: Generování grafů v tiskové kvalitě pro text práce.

---

## 🚀 Open Data Auditor (Aplikace)

Desktopová aplikace s moderním grafickým rozhraním (CustomTkinter) pro automatizovaný audit CSV datasetů.

### Klíčové funkce:
- **Missing Data Ratio (MDR):** Výpočet podílu chybějících hodnot se sjednocenou kritickou hranicí **20 %**.
- **Audit kódování a standardů:** Detekce UTF-8 (včetně BOM "Excel Trap"), detekce oddělovačů a plnění standardů OFN (IČO, částka, název).
- **Detekce "špinavých dat":** Identifikace textových řetězců v číselných sloupcích (např. u datasetu Estonska).
- **Export:** Možnost uložení auditního reportu do HTML nebo TXT.

---

## 🛠️ Instalace a spuštění

### Pro uživatele (Windows):
Nejjednodušší cesta je stáhnout si hotový program **OpenDataAuditor.exe** ze sekce **[Releases](https://github.com/TVOJE-JMENO/open-data-auditor/releases)** v pravém panelu tohoto repozitáře. Program nevyžaduje instalaci Pythonu.

### Pro vývojáře (Zdrojový kód):
1. Ujistěte se, že máte nainstalován Python 3.10+.
2. Nainstalujte potřebné knihovny:
   ```bash
   pip install -r requirements.txt
3. Spusťte aplikaci:
   ```bash
   python main.py

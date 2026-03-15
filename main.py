import pandas as pd
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import translations as tr
import graphs

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

selected_files = []
global_report_text = ""
global_report_html = ""


def change_language(choice):
    tr.set_language(choice)
    lbl_title.configure(text=tr.t("title"))
    lbl_subtitle.configure(text=tr.t("subtitle"))
    btn_select.configure(text=tr.t("btn_select"))
    btn_analyze.configure(text=tr.t("btn_analyze"))
    switch_detail.configure(text=tr.t("switch_detail"))
    btn_export.configure(text=tr.t("btn_export"))
    lbl_graph_settings.configure(text=tr.t("lbl_graph_settings"))

    if not selected_files:
        lbl_selected_files.configure(text=tr.t("lbl_no_files"))
    else:
        filenames = [os.path.basename(p) for p in selected_files]
        lbl_selected_files.configure(text=f"{tr.t('lbl_files_selected')} ({len(filenames)}): {', '.join(filenames)}")
    if lbl_status.cget("text") != "":
        lbl_status.configure(text=tr.t("status_ready"))


def check_bom(filepath):
    try:
        with open(filepath, 'rb') as f:
            return f.read(3) == b'\xef\xbb\xbf'
    except:
        return False


def select_files_action():
    global selected_files
    filepaths = filedialog.askopenfilenames(
        title="Vyberte CSV soubory / Select CSV files",
        filetypes=[("CSV", "*.csv"), ("All files", "*.*")]
    )
    if filepaths:
        selected_files = list(filepaths)
        filenames = [os.path.basename(p) for p in selected_files]
        lbl_selected_files.configure(text=f"{tr.t('lbl_files_selected')} ({len(filenames)}): {', '.join(filenames)}")
        btn_analyze.configure(state="normal")
        btn_export.configure(state="disabled")
        lbl_status.configure(text=tr.t("status_ready"), text_color="gray")


def run_analysis_action():
    global selected_files, global_report_text, global_report_html
    if not selected_files: return

    for w in scrollable_frame.winfo_children(): w.destroy()
    for w in scrollable_graph_frame.winfo_children(): w.destroy()

    lbl_status.configure(text=tr.t("status_working"), text_color="#ffc107")
    app.update()

    g_miss, g_enc, g_sep, g_ofn, g_dup = [], [], [], [], []

    global_report_text = f"{tr.t('report_title')}\n\n"
    global_report_html = f"<html><head><meta charset='utf-8'><title>{tr.t('report_title')}</title><style>body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 900px; margin: 40px auto; }} h1 {{ border-bottom: 2px solid #0056b3; padding-bottom: 10px; color: #0056b3; }} .card {{ background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin-bottom: 20px; }} .card h2 {{ margin-top: 0; color: #495057; font-size: 1.2em; }} ul {{ padding-left: 20px; }} li {{ margin-bottom: 5px; }}</style></head><body><h1>{tr.t('report_title')}</h1>"

    configs = [('utf-8', ','), ('utf-8', ';'), ('cp1250', ';'), ('cp1250', ','), ('latin1', ','), ('latin1', ';'),
               ('cp1252', ','), ('cp1252', ';')]
    is_detailed = (detail_switch_var.get() == "on")
    ofn_cols = ['ičo', 'ico', 'název', 'nazev', 'částka', 'castka', 'id', 'name', 'amount']

    for filepath in selected_files:
        filename = os.path.basename(filepath)
        has_bom = check_bom(filepath)
        file_size_kb = os.path.getsize(filepath) / 1024
        df, detected_enc, detected_sep = None, "Neznámé", "?"

        for enc, sep in configs:
            try:
                test = pd.read_csv(filepath, sep=sep, encoding=enc, nrows=2)
                if len(test.columns) > 1:
                    df = pd.read_csv(filepath, sep=sep, encoding=enc, on_bad_lines='skip')
                    detected_enc, detected_sep = enc.upper(), (";" if sep == ';' else ",")
                    break
            except:
                continue

        card = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color=("gray85", "gray20"))
        card.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(card, text=f"📄 {filename}", font=("Roboto", 16, "bold"), wraplength=650, justify="left").pack(
            anchor="w", padx=15, pady=(15, 5))

        global_report_text += f"File: {filename}\n"
        global_report_html += f"<div class='card'><h2>📄 {filename}</h2><ul>"

        if df is not None:
            lower_cols = [c.lower() for c in df.columns]
            found_ofn = [c for c in ofn_cols if any(c in lc for lc in lower_cols)]
            is_ofn_compliant = len(found_ofn) > 0
            dupes = df.duplicated().sum()

            enc_text = f"{tr.t('enc')}: {detected_enc}"
            enc_color = "#28a745" if detected_enc == 'UTF-8' and has_bom else (
                "#e67e22" if detected_enc in ['UTF-8', 'CP1250'] else "white")

            if detected_enc == 'UTF-8':
                enc_text += f"  {tr.t('excel_ok') if has_bom else tr.t('excel_trap')}"
            elif detected_enc == 'CP1250':
                enc_text += f"  {tr.t('win1250')}"

            ctk.CTkLabel(card, text=enc_text, font=("Roboto", 14), text_color=enc_color).pack(anchor="w", padx=30,
                                                                                              pady=2)
            global_report_text += f"- {enc_text}\n"
            global_report_html += f"<li><b>{enc_text}</b></li>"

            ctk.CTkLabel(card, text=f"{tr.t('sep')}: {detected_sep}", font=("Roboto", 14)).pack(anchor="w", padx=30,
                                                                                                pady=2)
            global_report_text += f"- {tr.t('sep')}: {detected_sep}\n"
            global_report_html += f"<li>{tr.t('sep')}: {detected_sep}</li>"

            missing = df.isnull().sum().sum()
            total = df.size
            missing_pct = (missing / total) * 100 if total > 0 else 0
            qual_text = f"{tr.t('miss')}: {missing_pct:.1f} %"

            qual_color = "#28a745" if missing_pct < 5 else ("#dc3545" if missing_pct > 20 else "#e67e22")
            status_key = 'excellent' if missing_pct < 5 else ('critical' if missing_pct > 20 else 'normal')
            qual_text += f"  {tr.t(status_key)}"

            ctk.CTkLabel(card, text=qual_text, font=("Roboto", 14, "bold"), text_color=qual_color).pack(anchor="w",
                                                                                                        padx=30, pady=2)
            global_report_text += f"- {qual_text}\n"
            global_report_html += f"<li>{qual_text}</li>"

            if dupes > 0:
                dupe_text = tr.t('dupes').format(dupes)
                ctk.CTkLabel(card, text=dupe_text, font=("Roboto", 13, "bold"), text_color="#dc3545").pack(anchor="w",
                                                                                                           padx=30,
                                                                                                           pady=2)
                global_report_text += f"- {dupe_text}\n"
                global_report_html += f"<li style='color:red;'><b>{dupe_text}</b></li>"

            if is_detailed:
                detail_frame = ctk.CTkFrame(card, fg_color="transparent")
                detail_frame.pack(fill="x", padx=30, pady=(10, 15))

                tech_info = f"⚙️ {tr.t('size')}: {file_size_kb:.1f} KB | {tr.t('rows')}: {df.shape[0]} | {tr.t('cols')}: {df.shape[1]}"
                ctk.CTkLabel(detail_frame, text=tech_info, font=("Roboto", 12, "italic"), text_color="gray",
                             wraplength=650, justify="left").pack(anchor="w")
                global_report_text += f"  (Details: {tech_info})\n"
                global_report_html += f"<li><i>{tech_info}</i></li>"

                if is_ofn_compliant:
                    ofn_msg = f"{tr.t('ofn_ok')} ({', '.join(set(found_ofn))})"
                    ctk.CTkLabel(detail_frame, text=ofn_msg, font=("Roboto", 12), text_color="#28a745", wraplength=650,
                                 justify="left").pack(anchor="w")
                else:
                    ofn_msg = tr.t('ofn_err')
                    ctk.CTkLabel(detail_frame, text=ofn_msg, font=("Roboto", 12), text_color="#e67e22", wraplength=650,
                                 justify="left").pack(anchor="w")
                global_report_text += f"  - {ofn_msg}\n"
                global_report_html += f"<li>{ofn_msg}</li>"

                dirty_cols = []
                for col in df.columns:
                    if df[col].dtype == 'object':
                        sample = df[col].dropna().astype(str).str.lower()
                        if sample.str.contains(r'\d', regex=True).any() and sample.str.contains(
                                r'kč|czk|eur|€|£|usd|\$', regex=True).any():
                            dirty_cols.append(col)

                if dirty_cols:
                    dirty_msg = tr.t('dirty').format(dirty_cols)
                    ctk.CTkLabel(detail_frame, text=dirty_msg, font=("Roboto", 12, "bold"), text_color="#dc3545",
                                 wraplength=650, justify="left").pack(anchor="w")
                    global_report_text += f"  - {dirty_msg}\n"
                    global_report_html += f"<li style='color:red;'><b>{dirty_msg}</b></li>"
            else:
                ctk.CTkFrame(card, height=10, fg_color="transparent").pack()

            g_miss.append((filename, missing_pct))
            g_enc.append(detected_enc)
            g_sep.append(detected_sep)
            g_ofn.append(is_ofn_compliant)
            g_dup.append((filename, dupes))
        else:
            err_msg = tr.t('err_load')
            ctk.CTkLabel(card, text=err_msg, text_color="#dc3545", font=("Roboto", 14, "bold"), wraplength=650,
                         justify="left").pack(anchor="w", padx=30, pady=(2, 15))
            global_report_text += f"- {err_msg}\n"
            global_report_html += f"<li style='color:red;'><b>{err_msg}</b></li>"

        global_report_text += "\n" + ("-" * 50) + "\n\n"
        global_report_html += "</ul></div>"

    global_report_html += "</body></html>"
    lbl_status.configure(text=tr.t("status_done"), text_color="#28a745")
    btn_export.configure(state="normal")

    if g_miss:
        graph_flags = {'miss': cb_miss_var.get(), 'enc': cb_enc_var.get(), 'sep': cb_sep_var.get(),
                       'ofn': cb_ofn_var.get(), 'dup': cb_dup_var.get()}
        graphs.generate_dashboard(scrollable_graph_frame, g_miss, g_enc, g_sep, g_ofn, g_dup, graph_flags)


def export_report_action():
    if not global_report_text: return
    filepath = filedialog.asksaveasfilename(title="Uložit report...", defaultextension=".html",
                                            filetypes=[("HTML Report", "*.html"), ("Obyčejný text", "*.txt")],
                                            initialfile="OpenData_Audit_Report")
    if filepath:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(global_report_html if filepath.lower().endswith(".html") else global_report_text)
            messagebox.showinfo("Úspěch", f"Report byl uložen do:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se uložit soubor:\n{str(e)}")


app = ctk.CTk()
app.title("Open Data Auditor - NKOD")
app.geometry("1000x900")

header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(fill="x", padx=20, pady=20)
lbl_title = ctk.CTkLabel(header_frame, text=tr.t("title"), font=("Roboto", 28, "bold"))
lbl_title.pack(side="left", anchor="w")
lang_menu = ctk.CTkOptionMenu(header_frame, values=["Čeština", "English"], command=change_language, width=100)
lang_menu.pack(side="right", anchor="e")
lbl_subtitle = ctk.CTkLabel(app, text=tr.t("subtitle"), font=("Roboto", 14), text_color="gray")
lbl_subtitle.pack(padx=20, anchor="w")

control_frame = ctk.CTkFrame(app, corner_radius=10)
control_frame.pack(fill="x", padx=20, pady=(15, 10))

btn_select = ctk.CTkButton(control_frame, text=tr.t("btn_select"), font=("Roboto", 14, "bold"),
                           command=select_files_action, width=150)
btn_select.grid(row=0, column=0, padx=20, pady=15)
lbl_selected_files = ctk.CTkLabel(control_frame, text=tr.t("lbl_no_files"), font=("Roboto", 12), text_color="gray")
lbl_selected_files.grid(row=0, column=1, padx=(0, 20), sticky="w")

btn_analyze = ctk.CTkButton(control_frame, text=tr.t("btn_analyze"), font=("Roboto", 14, "bold"), fg_color="#28a745",
                            hover_color="#218838", command=run_analysis_action, state="disabled", width=150)
btn_analyze.grid(row=1, column=0, padx=20, pady=(0, 15))

detail_switch_var = ctk.StringVar(value="on")
switch_detail = ctk.CTkSwitch(control_frame, text=tr.t("switch_detail"), variable=detail_switch_var, onvalue="on",
                              offvalue="off", font=("Roboto", 12))
switch_detail.grid(row=1, column=1, sticky="w")

btn_export = ctk.CTkButton(control_frame, text=tr.t("btn_export"), font=("Roboto", 13, "bold"), fg_color="#17a2b8",
                           hover_color="#138496", command=export_report_action, state="disabled")
btn_export.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="w")

graph_options_frame = ctk.CTkFrame(app, fg_color="transparent")
graph_options_frame.pack(fill="x", padx=20, pady=(0, 10))
lbl_graph_settings = ctk.CTkLabel(graph_options_frame, text=tr.t("lbl_graph_settings"), font=("Roboto", 13, "bold"))
lbl_graph_settings.pack(side="left", padx=(0, 15))

cb_miss_var, cb_enc_var, cb_sep_var, cb_ofn_var, cb_dup_var = ctk.StringVar(value="on"), ctk.StringVar(
    value="on"), ctk.StringVar(value="on"), ctk.StringVar(value="on"), ctk.StringVar(value="on")
ctk.CTkCheckBox(graph_options_frame, text="📊 Chybějící data", variable=cb_miss_var, onvalue="on", offvalue="off").pack(
    side="left", padx=5)
ctk.CTkCheckBox(graph_options_frame, text="🥧 Kódování", variable=cb_enc_var, onvalue="on", offvalue="off").pack(
    side="left", padx=5)
ctk.CTkCheckBox(graph_options_frame, text="🥧 Oddělovače", variable=cb_sep_var, onvalue="on", offvalue="off").pack(
    side="left", padx=5)
ctk.CTkCheckBox(graph_options_frame, text="🥧 OFN Standard", variable=cb_ofn_var, onvalue="on", offvalue="off").pack(
    side="left", padx=5)
ctk.CTkCheckBox(graph_options_frame, text="📊 Duplicity", variable=cb_dup_var, onvalue="on", offvalue="off").pack(
    side="left", padx=5)

lbl_status = ctk.CTkLabel(app, text="", font=("Roboto", 14, "bold"))
lbl_status.pack(pady=(0, 5))

tabview = ctk.CTkTabview(app, corner_radius=10)
tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
tab_text = tabview.add("Data")
tab_graph = tabview.add("Dashboard")

scrollable_frame = ctk.CTkScrollableFrame(tab_text, fg_color="transparent")
scrollable_frame.pack(fill="both", expand=True)
scrollable_graph_frame = ctk.CTkScrollableFrame(tab_graph, fg_color="transparent")
scrollable_graph_frame.pack(fill="both", expand=True)

app.mainloop()
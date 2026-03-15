import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from collections import Counter
import translations as tr
import customtkinter as ctk

def add_graph_to_scroll(fig, scroll_frame):
    fig.tight_layout(pad=3.0)
    wrapper = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    wrapper.pack(fill="x", expand=True, padx=20, pady=15)
    canvas = FigureCanvasTkAgg(fig, master=wrapper)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="x", expand=True)
    toolbar = NavigationToolbar2Tk(canvas, wrapper, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(fill="x", pady=(0, 10))

    plt.close(fig)

def generate_dashboard(scroll_frame, missing, enc, sep, ofn, dupes, flags):
    filenames = [item[0][:15] + "..." if len(item[0]) > 15 else item[0] for item in missing]
    plt.style.use('ggplot')

    if flags.get('miss') == "on":
        missing_pcts = [item[1] for item in missing]
        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(filenames, missing_pcts, color='steelblue')

        for i, pct in enumerate(missing_pcts):
            if pct > 20:
                bars[i].set_color('firebrick')

        ax.set_title(tr.t('graph_title'), fontsize=13, pad=10)
        ax.set_ylabel(f"{tr.t('miss')} (%)", fontsize=11)

        ax.axhline(y=20, color='red', linestyle='--', label=f"{tr.t('critical')} (20%)")

        ax.set_xticks(range(len(filenames)))
        ax.set_xticklabels(filenames, rotation=30, ha='right')
        ax.legend()
        add_graph_to_scroll(fig, scroll_frame)

    if flags.get('enc') == "on":
        enc_counts = Counter(enc)
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(enc_counts.values(), labels=enc_counts.keys(), autopct='%1.1f%%', startangle=140,
               colors=['mediumseagreen', 'lightcoral', 'lightskyblue'])
        ax.set_title(tr.t('graph_enc'), fontsize=12, pad=10)
        add_graph_to_scroll(fig, scroll_frame)

    if flags.get('sep') == "on":
        sep_counts = Counter(sep)
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(sep_counts.values(), labels=sep_counts.keys(), autopct='%1.1f%%', startangle=90,
               colors=['#ff9999', '#66b3ff'])
        ax.set_title(tr.t('graph_sep'), fontsize=12, pad=10)
        add_graph_to_scroll(fig, scroll_frame)

    if flags.get('ofn') == "on":
        ofn_counts = Counter(ofn)
        ofn_labels = [tr.t('ofn_pass') if k else tr.t('ofn_fail') for k in ofn_counts.keys()]
        ofn_colors = ['mediumseagreen' if k else 'lightcoral' for k in ofn_counts.keys()]
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(ofn_counts.values(), labels=ofn_labels, autopct='%1.1f%%', startangle=90, colors=ofn_colors)
        ax.set_title(tr.t('graph_ofn'), fontsize=12, pad=10)
        add_graph_to_scroll(fig, scroll_frame)

    if flags.get('dup') == "on":
        dupes_counts = [item[1] for item in dupes]
        fig, ax = plt.subplots(figsize=(9, 5))
        bars_dupes = ax.bar(filenames, dupes_counts, color='orange')
        for i, d in enumerate(dupes_counts):
            if d > 0:
                bars_dupes[i].set_color('firebrick')
        ax.set_title(tr.t('graph_dupes'), fontsize=13, pad=10)
        ax.set_ylabel(tr.t('dupes_count'), fontsize=11)
        ax.set_xticks(range(len(filenames)))
        ax.set_xticklabels(filenames, rotation=30, ha='right')
        add_graph_to_scroll(fig, scroll_frame)
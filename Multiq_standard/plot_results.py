#Grafici giusti, sempre la questione del 0.5
# import sys
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap, BoundaryNorm

# # --- Configurazione File di Input --------------------------------------

# #controllo lattice
# LATTICE = sys.argv[2]

# #Commento


# #SC
# INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "results_SC.csv"

# #FCC
# #INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "results_FCC.csv"

# CATEGORY_ORDER = ["L > T (Sempre)", "T < L < T (Sempre)", "L < T (Sempre)",
#                   "Altro", "Sopra-mezzo", "Tutto"]
# COLORS = ['#4477AA', '#228833', '#EE6677', '#CCBB44', '#AA3377', '#66CCEE']

# # Categorie in cui mettere i riquadri
# CAT_BLU = 0     # area blu
# CAT_VIOLA = 4   # area viola
# CAT_AZZURRO = 5 #area azzurra
# epsilon = 1 / 72

# # Passo dei tick
# STEP_X = 0.25
# STEP_Y = 0.25

# # --- Caricamento dati ---------------------------------------------------
# try:
#     df = pd.read_csv(INPUT_FILE, sep=r'\s+', names=['gamma2', 'gamma3', 'cmp_T_L', 'frac','frac1','fracgen','fracgen1'])
# except FileNotFoundError:
#     print(f"Errore: Il file {INPUT_FILE} non esiste. Controlla il percorso.")
#     sys.exit(1)

# # Conversione numerica (righe non numeriche, es. intestazione, diventano NaN e vengono scartate)
# for col in ['gamma2', 'gamma3', 'cmp_T_L']:
#     df[col] = pd.to_numeric(df[col], errors='coerce')
# df = df.dropna(subset=['gamma2', 'gamma3', 'cmp_T_L'])
# df['cmp_T_L'] = df['cmp_T_L'].astype(int)

# # --- Classificazione dei codici C++ nelle macro-categorie --------------
# def map_code_to_category(code):
#     if code == 0:
#         return 0  # L > T (Sempre)
#     elif code == 1:
#         return 1  # T < L < T (Sempre)
#     elif code == 2:
#         return 2  # L < T (Sempre)
#     elif code in [3, 5]:
#         return 3  # Altro
#     elif code == 4:
#         return 4  # sopra-mezzo
#     elif code == 6:
#         return 5  # tutto almeno una volta
#     else:
#         return -1

# df['cat_code'] = df['cmp_T_L'].apply(map_code_to_category)
# df = df[df['cat_code'] != -1]

# # --- Pivot dei dati per la mappa 2D -------------------------------------
# pivot = df.pivot(index='gamma3', columns='gamma2', values='cat_code')

# # --- Generazione del Grafico (Plot) --------------------------------------
# cmap = ListedColormap(COLORS)
# bounds = [i - 0.5 for i in range(len(CATEGORY_ORDER) + 1)]
# norm = BoundaryNorm(bounds, cmap.N)

# fig, ax = plt.subplots(figsize=(8, 6.5))

# mesh = ax.pcolormesh(
#     pivot.columns, pivot.index, pivot.values,
#     cmap=cmap, norm=norm, shading='nearest'
# )

# #Commento
# #SC 
# ax.set_xlabel(r"$(\gamma_1 + \gamma_5)/2$", fontsize=14)
# #FCC
# #ax.set_xlabel(r"$(\gamma_2 + \gamma_4)/2$", fontsize=14)

# ax.set_ylabel(r"$\gamma_3$", fontsize=14)

# # --- Tick asse x: passo STEP_X ------------------------------------------
# xmin, xmax = float(pivot.columns.min()), float(pivot.columns.max())
# xticks = np.arange(np.ceil(xmin / STEP_X) * STEP_X, xmax + 1e-9, STEP_X)
# ax.set_xticks(xticks)
# ax.set_xticklabels([f"{t:.2f}" for t in xticks])
# ax.set_xlim(xmin, xmax)

# # --- Tick asse y: passo STEP_Y, con 0.25 etichettato "18ε = 0.25" -------
# ymin, ymax = float(pivot.index.min()), float(pivot.index.max())
# yticks = np.arange(np.ceil(ymin / STEP_Y) * STEP_Y, ymax + 1e-9, STEP_Y)
# ax.set_yticks(yticks)
# ylabels = []
# for t in yticks:
#     if np.isclose(t, 18 * epsilon):
#         ylabels.append(r"$18\,\varepsilon\ =\ 0.25$")
#     else:
#         ylabels.append(f"{t:.2f}")
# ax.set_yticklabels(ylabels)
# ax.set_ylim(ymin, ymax)

# # Nessuna griglia, solo tacche sugli assi
# ax.grid(False)

# # --- Riquadri di testo dentro le aree -----------------------------------
# def centro_area(cat):
#     """Baricentro delle celle appartenenti alla categoria cat."""
#     sub = df[df['cat_code'] == cat]
#     if sub.empty:
#         return None
#     return sub['gamma2'].mean(), sub['gamma3'].mean()

# box_style = dict(boxstyle="round,pad=0.4", facecolor="white",
#                  edgecolor="black", alpha=0.9)

# # Riquadro nell'area blu
# c = centro_area(CAT_BLU)
# if c is not None:
#     ax.text(c[0], c[1], "L > $T_1$,$T_2$ everywere", ha="center", va="center",
#             fontsize=14, bbox=box_style)

# # Riquadro nell'area viola
# c = centro_area(CAT_VIOLA)
# if c is not None:
#     ax.text(c[0], c[1], r"$L < T_1,T_2$ or L > $T_1$,$T_2$", ha="center", va="center",
#             fontsize=14, bbox=box_style) 
#     ax.text(0.1,1.85, "SC",fontsize=15,bbox=box_style)

# # Riquadro nell'area viola
# c = centro_area(CAT_AZZURRO)
# if c is not None:
#     ax.text(c[0], c[1], r" L < $T_1$,$T_2$ or $T_1 < L < T_2$ or L > $T_1$,$T_2$", ha="center", va="center",
#             fontsize=14, bbox=box_style)
#     ax.text(0.1,1.85, "FCC",fontsize=15,bbox=box_style)

# plt.tight_layout()
# #Commento
# #SC
# plt.savefig("map_gamma_SC_TL.png", dpi=150, bbox_inches='tight')
# #FCC
# #plt.savefig("map_gamma_FCC_TL.png", dpi=150, bbox_inches='tight')

# #print("Grafico generato e salvato con successo.")
# plt.show()



import argparse
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# --- Argomenti da riga di comando ---------------------------------------
parser = argparse.ArgumentParser(description="Mappa (gamma_x, gamma3) per reticolo SC o FCC")
parser.add_argument("lattice", choices=["SC", "FCC"], help="reticolo da usare")
parser.add_argument("--input", default=None,
                    help="file csv di input (default: results_<lattice>.csv)")
args = parser.parse_args()

LATTICE = args.lattice

# --- Configurazione dipendente dal reticolo -----------------------------
CONFIG = {
    "SC": {
        "input":  "results_SC.csv",
        "output": "map_gamma_SC_TL.png",
        "xlabel": r"$(\gamma_1 + \gamma_5)/2$",
    },
    "FCC": {
        "input":  "results_FCC.csv",
        "output": "map_gamma_FCC_TL.png",
        "xlabel": r"$(\gamma_2 + \gamma_4)/2$",
    },
}
cfg = CONFIG[LATTICE]
INPUT_FILE = args.input if args.input else cfg["input"]

CATEGORY_ORDER = ["L > T (Sempre)", "T1 < L < T2 (Sempre)", "L < T (Sempre)",
                  "Altro", "Sopra-sotto", "Tutto"]
COLORS = ['#4477AA', '#228833', '#EE6677', '#CCBB44', '#AA3377', '#66CCEE']

# Categorie in cui mettere i riquadri
CAT_BLU = 0      # area blu
CAT_VIOLA = 4    # area viola
CAT_AZZURRO = 5  # area azzurra
epsilon = 1 / 72

# Passo dei tick
STEP_X = 0.25
STEP_Y = 0.25

# --- Caricamento dati ---------------------------------------------------
# La prima colonna è gamma1 (SC) o gamma2 (FCC): la chiamo genericamente gx
try:
    df = pd.read_csv(INPUT_FILE, sep=r'\s+',
                     names=['gx', 'gamma3', 'cmp_T_L', 'frac', 'frac1', 'fracdeg', 'fracdeg1'])
except FileNotFoundError:
    print(f"Errore: Il file {INPUT_FILE} non esiste. Controlla il percorso.")
    sys.exit(1)

# Righe non numeriche (intestazione) diventano NaN e vengono scartate
for col in ['gx', 'gamma3', 'cmp_T_L']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna(subset=['gx', 'gamma3', 'cmp_T_L'])
df['cmp_T_L'] = df['cmp_T_L'].astype(int)

# --- Classificazione dei codici C++ nelle macro-categorie ---------------
def map_code_to_category(code):
    if code == 0:
        return 0  # L > T (sempre)
    elif code == 1:
        return 1  # T1 < L < T2 (sempre)
    elif code == 2:
        return 2  # L < T (sempre)
    elif code in [3, 5]:
        return 3  # Altro
    elif code == 4:
        return 4  # sopra + sotto
    elif code == 6:
        return 5  # tutte e tre
    else:
        return -1

df['cat_code'] = df['cmp_T_L'].apply(map_code_to_category)
df = df[df['cat_code'] != -1]

# --- Pivot dei dati per la mappa 2D -------------------------------------
pivot = df.pivot(index='gamma3', columns='gx', values='cat_code')

# --- Grafico ------------------------------------------------------------
cmap = ListedColormap(COLORS)
bounds = [i - 0.5 for i in range(len(CATEGORY_ORDER) + 1)]
norm = BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(8, 6.5))
ax.pcolormesh(pivot.columns, pivot.index, pivot.values,
              cmap=cmap, norm=norm, shading='nearest')

ax.set_xlabel(cfg["xlabel"], fontsize=14)
ax.set_ylabel(r"$\gamma_3$", fontsize=14)

# Tick asse x
xmin, xmax = float(pivot.columns.min()), float(pivot.columns.max())
xticks = np.arange(np.ceil(xmin / STEP_X) * STEP_X, xmax + 1e-9, STEP_X)
ax.set_xticks(xticks)
ax.set_xticklabels([f"{t:.2f}" for t in xticks])
ax.set_xlim(xmin, xmax)

# Tick asse y, con 0.25 etichettato "18ε = 0.25"
ymin, ymax = float(pivot.index.min()), float(pivot.index.max())
yticks = np.arange(np.ceil(ymin / STEP_Y) * STEP_Y, ymax + 1e-9, STEP_Y)
ax.set_yticks(yticks)
ylabels = []
for t in yticks:
    if np.isclose(t, 18 * epsilon):
        ylabels.append(r"$18\,\varepsilon\ =\ 0.25$")
    else:
        ylabels.append(f"{t:.2f}")
ax.set_yticklabels(ylabels)
ax.set_ylim(ymin, ymax)

ax.grid(False)

# --- Riquadri di testo dentro le aree -----------------------------------
def centro_area(cat):
    """Baricentro delle celle appartenenti alla categoria cat."""
    sub = df[df['cat_code'] == cat]
    if sub.empty:
        return None
    return sub['gx'].mean(), sub['gamma3'].mean()

box_style = dict(boxstyle="round,pad=0.4", facecolor="white",
                 edgecolor="black", alpha=0.9)

c = centro_area(CAT_BLU)
if c is not None:
    ax.text(c[0], c[1], r"$L > T_1, T_2$ everywhere", ha="center", va="center",
            fontsize=14, bbox=box_style)

c = centro_area(CAT_VIOLA)
if c is not None:
    ax.text(c[0], c[1], r"$L < T_1,T_2$ or $L > T_1,T_2$", ha="center", va="center",
            fontsize=14, bbox=box_style)

c = centro_area(CAT_AZZURRO)
if c is not None:
    ax.text(c[0], c[1], r"$L < T_1,T_2$ or $T_1 < L < T_2$ or $L > T_1,T_2$",
            ha="center", va="center", fontsize=14, bbox=box_style)

# Etichetta del reticolo (una sola volta, per entrambi i casi)
ax.text(0.1, 1.85, LATTICE, fontsize=15, bbox=box_style)

plt.tight_layout()
plt.savefig(cfg["output"], dpi=150, bbox_inches='tight')
plt.show()
#-----This script takes the files 2D_Results_SC.txt or 2D_Results_FCC.txt  as input and it creates the phase diagrams-----

import argparse
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# --- Input arguments ---------------------------------------
parser = argparse.ArgumentParser(description="Map (gamma_x, gamma3) for SC or FCC lattice")
parser.add_argument("lattice", choices=["SC", "FCC"], help="to be used lattice")
parser.add_argument("--input", default=None,
                    help=" input file (default: 2D_Results_<lattice>.txt)")
args = parser.parse_args()

LATTICE = args.lattice

# --- Lattice configurations -----------------------------
CONFIG = {
    "SC": {
        "input":  "/home/tonelli/Tesi/Multi_Dir/Results/2D_Results/2D_Results_SC.txt",
        "output": "Color_Map_Plot_SC.png",
        "xlabel": r"$(\gamma_1 + \gamma_5)/2$",
    },
    "FCC": {
        "input":  "/home/tonelli/Tesi/Multi_Dir/Results/2D_Results/2D_Results_FCC.txt",
        "output": "Color_Map_Plot_FCC.png",
        "xlabel": r"$(\gamma_2 + \gamma_4)/2$",
    },
}
cfg = CONFIG[LATTICE]
INPUT_FILE = args.input if args.input else cfg["input"]

CATEGORY_ORDER = ["L > T (Always)", "T1 < L < T2 (Always)", "L < T (Always)",
                  "other options", "above-under", "Everything"]
COLORS = ['#4477AA', '#228833', '#EE6677', '#CCBB44', '#AA3377', '#66CCEE']

# Color of the categories
CAT_BLU = 0      #  blu area
CAT_VIOLA = 4    #  purple area
CAT_AZZURRO = 5  #  azurre area
epsilon = 1 / 72

# Tick steps
STEP_X = 0.25
STEP_Y = 0.25

#--- Data loading ---------------------------------------------------
#The first column is gamma1 (SC) or gamma2 (FCC): i call it generically gx
try:
    df = pd.read_csv(INPUT_FILE, sep=r'\s+',
                     names=['gx', 'gamma3', 'cmp_T_L', 'frac', 'frac1', 'fracdeg', 'fracdeg1'])
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} does not exist. Check the path.")
    sys.exit(1)

# not numerical lines becomes Nan and are excluded
for col in ['gx', 'gamma3', 'cmp_T_L']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna(subset=['gx', 'gamma3', 'cmp_T_L'])
df['cmp_T_L'] = df['cmp_T_L'].astype(int)

# --- Integer assignment ---------------
def map_code_to_category(code):
    if code == 0:
        return 0  # L > T (always)
    elif code == 1:
        return 1  # T1 < L < T2 (always)
    elif code == 2:
        return 2  # L < T (always)
    elif code in [3, 5]:
        return 3  # other options
    elif code == 4:
        return 4  # above-under
    elif code == 6:
        return 5  # everything
    else:
        return -1

df['cat_code'] = df['cmp_T_L'].apply(map_code_to_category)
df = df[df['cat_code'] != -1]

# --- Data Pivot for the 2D map -------------------------------------
pivot = df.pivot(index='gamma3', columns='gx', values='cat_code')

# --- Graph ------------------------------------------------------------
cmap = ListedColormap(COLORS)
bounds = [i - 0.5 for i in range(len(CATEGORY_ORDER) + 1)]
norm = BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(8, 6.5))
ax.pcolormesh(pivot.columns, pivot.index, pivot.values,
              cmap=cmap, norm=norm, shading='nearest')

ax.set_xlabel(cfg["xlabel"], fontsize=14)
ax.set_ylabel(r"$\gamma_3$", fontsize=14)

# x axis tick
xmin, xmax = float(pivot.columns.min()), float(pivot.columns.max())
xticks = np.arange(np.ceil(xmin / STEP_X) * STEP_X, xmax + 1e-9, STEP_X)
ax.set_xticks(xticks)
ax.set_xticklabels([f"{t:.2f}" for t in xticks])
ax.set_xlim(xmin, xmax)

#y axis tick, highlighting "18ε = 0.25"
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

# --- Text boxes inside different areas -----------------------------------
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

# Lattice label
ax.text(0.1, 1.85, LATTICE, fontsize=15, bbox=box_style)

plt.tight_layout()
plt.savefig(f"/home/tonelli/Tesi/Multi_Dir/Plots/Color_Map_Plots/{cfg["output"]}", dpi=150, bbox_inches='tight')
plt.show()





























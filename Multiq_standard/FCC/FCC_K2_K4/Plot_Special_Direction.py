"""
Plot 2D categoriale (K2 vs K4) del confronto T-L per le tre direzioni
speciali (100, 110, 111), lette da results_special_directions.csv.

Ogni cella della griglia viene colorata in base al valore di cmp_T_L:
  n = T < L
  y = T > L
  m = misto (un T sopra, un T sotto L)
  = = T e L coincidono (degenerazione completa)

Uso:
    python plot_special_directions.py results_special_directions.csv
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# --- Config ---------------------------------------------------------
INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "results_special_directions.csv"
DIREZIONI = ["100", "110", "111"]

LABEL_MAP = {'n': 0, 'y': 1, 'm': 2, '=': 3}
LABELS_LEGENDA = ['n (T<L)', 'y (T>L)', 'm (misto)', '= (uguali)']
COLORS = ['#4477AA', '#EE6677', '#228833', '#CCBB44']

# --- Caricamento dati ------------------------------------------------
df = pd.read_csv(INPUT_FILE)
df['direzione'] = df['direzione'].astype(str)  # forza confronto testuale (100/110/111)
df['code'] = df['cmp_T_L'].map(LABEL_MAP)

cmap = ListedColormap(COLORS)
bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
norm = BoundaryNorm(bounds, cmap.N)

# --- Canvas con 3 subplot affiancati ----------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)

mesh = None
for ax, direzione in zip(axes, DIREZIONI):
    sub = df[df['direzione'] == direzione]

    if sub.empty:
        ax.set_title(f"direzione {direzione} (nessun dato)")
        continue

    pivot = sub.pivot(index='K4', columns='K2', values='code')

    mesh = ax.pcolormesh(
        pivot.columns, pivot.index, pivot.values,
        cmap=cmap, norm=norm, shading='nearest'
    )

    ax.set_title(f"Direzione {direzione}")
    ax.set_xlabel("K2")

axes[0].set_ylabel("K4")

# --- Colorbar comune (unica legenda per tutti e 3 i subplot) ----------
if mesh is not None:
    cbar = fig.colorbar(mesh, ax=axes, ticks=[0, 1, 2, 3],
                         fraction=0.03, pad=0.02)
    cbar.ax.set_yticklabels(LABELS_LEGENDA)

fig.suptitle("Confronto T vs L nelle direzioni speciali", y=1.03)

plt.savefig("special_directions_comparison.png", dpi=150, bbox_inches='tight')
plt.show()

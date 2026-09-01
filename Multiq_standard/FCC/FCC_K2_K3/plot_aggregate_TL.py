"""
Mappa 2D (K2 vs K3) che classifica ogni punto della griglia in base al
comportamento di cmp_T_L aggregato su TUTTE le direzioni q campionate
per quel (K2, K3), lette da results_Multiq.csv (lo sweep generico
theta/phi, non le sole direzioni speciali).

Categorie, mutuamente esclusive:
  1) "sempre_n"  -> per tutti i q, L > T   (cmp_T_L == 'n' ovunque)
  2) "sempre_y"  -> per tutti i q, T > L   (cmp_T_L == 'y' ovunque)
  3) "misto"     -> tutto il resto (compresi 'm', 'y' non esclusivo, '=',
                    o qualunque combinazione che non rientri nei due casi
                    sopra). Su questo dataset, "misto" coincide di fatto
                    con "almeno un q ha cmp_T_L == 'm'": verificato che
                    non esistono punti (K2,K3) con 'y' ma senza 'm'
                    (conseguenza della continuita' degli autovalori
                    rispetto a q).

IMPORTANTE: richiede che results_Multiq.csv sia stato generato con la
logica a 4 stati (y/n/m/=) corretta, non con la vecchia logica a
cascata. Se il CSV proviene dal main() non ancora aggiornato, i
risultati di questa aggregazione non sono affidabili.

Uso:
    python plot_aggregate_TL.py results_Multiq.csv
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# --- Config -----------------------------------------------------------
INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "results_Multiq.csv"

CATEGORY_ORDER = ["sempre_n", "sempre_y", "misto"]
CATEGORY_CODE = {name: i for i, name in enumerate(CATEGORY_ORDER)}
CATEGORY_LABELS = [
    "sempre L>T",
    "sempre T>L",
    "misto (almeno 1 q con T<L<T o disomogeneo)",
]
COLORS = ['#4477AA', '#EE6677', '#228833']

# --- Caricamento dati ---------------------------------------------------
df = pd.read_csv(INPUT_FILE)
df['cmp_T_L'] = df['cmp_T_L'].astype(str).str.strip()

# --- Classificazione per (K2, K3), 3 categorie esclusive -----------------
def classify(group):
    values = group['cmp_T_L']
    if (values == 'n').all():
        return CATEGORY_CODE["sempre_n"]
    if (values == 'y').all():
        return CATEGORY_CODE["sempre_y"]
    return CATEGORY_CODE["misto"]

result = (
    df.groupby(['K2', 'K3'])
      .apply(classify)
      .reset_index(name='code')
)

pivot = result.pivot(index='K3', columns='K2', values='code')

# --- Plot -----------------------------------------------------------------
cmap = ListedColormap(COLORS)
bounds = [i - 0.5 for i in range(len(CATEGORY_ORDER) + 1)]
norm = BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(7, 6))
mesh = ax.pcolormesh(
    pivot.columns, pivot.index, pivot.values,
    cmap=cmap, norm=norm, shading='nearest'
)

cbar = fig.colorbar(mesh, ticks=range(len(CATEGORY_ORDER)))
cbar.ax.set_yticklabels(CATEGORY_LABELS)

ax.set_xlabel("K2")
ax.set_ylabel("K3")
ax.set_title("Classificazione T vs L aggregata su tutte le direzioni q")

plt.tight_layout()
plt.savefig("aggregate_TL_map.png", dpi=150, bbox_inches='tight')
plt.show()
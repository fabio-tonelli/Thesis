#-----This script takes the files results_SC.txt or results_FCC.txt  as input and it creates the 'fraction of directions' diagrams-----

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# --- Input arguments ---------------------------------------
parser = argparse.ArgumentParser(description="Mappe a colori delle frazioni di punti q per reticolo SC o FCC")
parser.add_argument("lattice", choices=["SC", "FCC"], help="reticolo da usare")
parser.add_argument("--input", default=None,
                    help="file csv di input (default: results_<lattice>.txt)")
args = parser.parse_args()

LATTICE = args.lattice

# --- Lattice configurations -----------------------------
CONFIG = {
    "SC": {
        "input":  "/home/tonelli/Tesi/Multiq_standard/Results/2D_Results/results_SC.txt",
        "output": "color_map_gamma_SC_TL_shared.png",
        "xlabel": r'$(\gamma_1 + \gamma_5)/2$',
        "vmin": 0, "vmax": 0.15,
    },
    "FCC": {
        "input":  "/home/tonelli/Tesi/Multiq_standard/Results/2D_Results/results_FCC.txt",
        "output": "color_map_gamma_FCC_TL_shared.png",
        "xlabel": r'$(\gamma_2+\gamma_4)/2$',
        "vmin": 0, "vmax": 0.6,
    },
}
cfg = CONFIG[LATTICE]
INPUT_FILE = args.input if args.input else cfg["input"]

# --- Data loading ---------------------------------------------------
#  loadtxt ignore rows starting with #
try:
    x, y, flag, z, z1, zdeg, zdeg1 = np.loadtxt(INPUT_FILE, unpack=True)
except FileNotFoundError:
    raise SystemExit(f"Errore: il file {INPUT_FILE} non esiste. Controlla il percorso.")

def to_map(values):
    N = int(len(values) ** .5)
    return values.reshape(N, N).transpose()[::-1, :]   # flip verticale

extent = (np.amin(x), np.amax(x), np.amin(y), np.amax(y))

# Boxstyle
box_style = dict(boxstyle="round,pad=0.4", facecolor="white",
                 edgecolor="black", alpha=0.9)

# Shared scale
vmin, vmax = cfg["vmin"], cfg["vmax"]


# Box labels
box_labels = [ r'$T_2 > L$',
               r'$T_1, T_2 > L$']

fig, axs = plt.subplots(1, 2, sharey=True, figsize=(10, 4.5),
                        constrained_layout=True)

#titles = [r'$T_2 > L$', r'$T_1, T_2 > L$']
for ax, vals, label in zip(axs, (z, z1), box_labels):
    im = ax.imshow(to_map(vals), extent=extent, cmap=cm.rainbow,
                   vmin=vmin, vmax=vmax)
    ax.set_xlabel(cfg["xlabel"], fontsize=14)
    ax.text(0.1, 1.85, label, fontsize=15, bbox=box_style)
axs[0].set_ylabel(r'$\gamma_3$', fontsize=14)

cbar = fig.colorbar(im, ax=axs, shrink=0.9)
cbar.set_label('fraction of directions', rotation=90, labelpad=20)

fig.savefig(f"/home/tonelli/Tesi/Multiq_standard/Plots/Frac_Dir_Plots/{cfg["output"]}", dpi=150, bbox_inches='tight')
plt.show()
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# from matplotlib.colors import LogNorm
# import numpy as np

# x, y, flag, z = np.loadtxt('results.csv', unpack=True)
# N = int(len(z)**.5)
# z = z.reshape(N, N).transpose()
# zp = np.zeros((N,N))
# for i in range(N):
#     for j in range(N):
#         zp[i,j] = z[N-i-1,j]

# fig, ax = plt.subplots()        
# im=plt.imshow(zp, extent=(np.amin(x), np.amax(x), np.amin(y), np.amax(y)),
#         cmap=cm.rainbow)#, norm=LogNorm())
    
# cbar=fig.colorbar(im)
# cbar.set_label('fraction of q points where $T_2 > L$', rotation=90,labelpad=20)

# im.axes.set_xlabel(r'$\gamma2$')
# im.axes.set_ylabel(r'$\gamma3$')
# # plt.pcolormesh(z, cmap='Accent')
# # plt.Axes.set_xscale("linear",0,5)

# plt.savefig("color_map_gamma_FCC_TL.png", dpi=150, bbox_inches='tight')

# plt.show()
#Grafici a posto0, a parte 0.5 , fatto sia FCC che SC
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm

# #Commento
# #x, y, flag, z, z1,zdeg,zdeg1 = np.loadtxt('results_SC.csv', unpack=True)
# x, y, flag, z, z1,zdeg,zdeg1 = np.loadtxt('results_FCC.csv', unpack=True)
# def to_map(values):
#     N = int(len(values)**.5)
#     return values.reshape(N, N).transpose()[::-1, :]   # flip verticale

# extent = (np.amin(x), np.amax(x), np.amin(y), np.amax(y))

# #Boxstyle
# box_style = dict(boxstyle="round,pad=0.4", facecolor="white",
#                  edgecolor="black", alpha=0.9)
# #Commento
# # scala condivisa
# #SC
# #vmin, vmax = 0, 0.15
# #FCC
# vmin, vmax = 0, 0.6  

# # vmin = min(z.min(), z1.min()); vmax = max(z.max(), z1.max())   # oppure dai dati

# fig, axs = plt.subplots(1, 2, sharey=True, figsize=(10, 4.5),
#                         constrained_layout=True)

# titles = [r'$T_2 > L$', r'$T_1, T_2 > L$']
# for ax, vals, title in zip(axs, (z, z1), titles):
#     im = ax.imshow(to_map(vals), extent=extent, cmap=cm.rainbow,
#                    vmin=vmin, vmax=vmax)
#     #Commento
#     #SC
#     #ax.set_xlabel(r'$(\gamma_1 + \gamma_5)/2$',fontsize=14)
#     #FCC
#     ax.set_xlabel(r'$(\gamma_2+\gamma_4)/2$',fontsize=14)
#     #ax.set_title(title)
#     #Commento
#     #SC
#     #ax.text(0.1,1.85, "SC",fontsize=15,bbox=box_style)
#     #FCC
#     ax.text(0.1,1.85, "FCC",fontsize=15,bbox=box_style)
# axs[0].set_ylabel(r'$\gamma_3$',fontsize=14)


# cbar = fig.colorbar(im, ax=axs, shrink=0.9)
# cbar.set_label('fraction of q points', rotation=90, labelpad=20)

# #Commento
# #SC
# #fig.savefig('color_map_gamma_SC_TL_shared.png', dpi=150, bbox_inches='tight')
# #FCC
# fig.savefig('color_map_gamma_FCC_TL_shared.png', dpi=150, bbox_inches='tight')
# plt.show()

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# --- Argomenti da riga di comando ---------------------------------------
parser = argparse.ArgumentParser(description="Mappe a colori delle frazioni di punti q per reticolo SC o FCC")
parser.add_argument("lattice", choices=["SC", "FCC"], help="reticolo da usare")
parser.add_argument("--input", default=None,
                    help="file csv di input (default: results_<lattice>.csv)")
args = parser.parse_args()

LATTICE = args.lattice

# --- Configurazione dipendente dal reticolo -----------------------------
CONFIG = {
    "SC": {
        "input":  "results_SC.csv",
        "output": "color_map_gamma_SC_TL_shared.png",
        "xlabel": r'$(\gamma_1 + \gamma_5)/2$',
        "vmin": 0, "vmax": 0.15,
    },
    "FCC": {
        "input":  "results_FCC.csv",
        "output": "color_map_gamma_FCC_TL_shared.png",
        "xlabel": r'$(\gamma_2+\gamma_4)/2$',
        "vmin": 0, "vmax": 0.6,
    },
}
cfg = CONFIG[LATTICE]
INPUT_FILE = args.input if args.input else cfg["input"]

# --- Caricamento dati ---------------------------------------------------
# Le righe che iniziano con # (intestazione) sono ignorate da loadtxt
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

# Scala condivisa
vmin, vmax = cfg["vmin"], cfg["vmax"]
# vmin = min(z.min(), z1.min()); vmax = max(z.max(), z1.max())   # oppure dai dati

# etichette per i box: una per pannello (sinistro, destro)
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

fig.savefig(cfg["output"], dpi=150, bbox_inches='tight')
plt.show()
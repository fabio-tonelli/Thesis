import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap, BoundaryNorm

LATTICES = ["SC", "FCC"]
N = 60                                      # numero di frame (animazione del primo valore)
N_GAMMA3 = 9                                # numero di valori di gamma3 (file 0..4)

#            0: L sotto   1: L in mezzo   2: L sopra
colors = ['#AA3377', '#228833', '#4477AA']
labels = [r'$L < T_1 \leq T_2$', r'$T_1 < L < T_2$', r'$T_1 \leq T_2 < L$']
cmap = ListedColormap(colors)
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

plt.rcParams.update({"font.size": 18, "axes.labelsize": 24,
                     "xtick.labelsize": 16, "ytick.labelsize": 16,
                     "mathtext.fontset": "cm"})
box = dict(boxstyle="round,pad=0.35", facecolor="white",
           edgecolor="black", linewidth=1.5)

os.makedirs("frames", exist_ok=True)

for g in range(N_GAMMA3):
    fig = plt.figure(figsize=(16, 9))
    axs = [fig.add_subplot(1, 2, i + 1, projection="3d") for i in range(2)]
    # margini fissi: a destra resta spazio per la colorbar
    fig.subplots_adjust(left=0.03, right=0.84, top=0.98, bottom=0.04, wspace=0.12)

    data = []
    for ax, lat in zip(axs, LATTICES):
        fname = f"{g}_results_{lat}_sphere.csv"
        try:
            qx, qy, qz, lab = np.loadtxt(fname, unpack=True)
        except FileNotFoundError:
            raise SystemExit(f"Errore: il file {fname} non esiste.")

        # angolo dalla direzione [111]
        q = np.stack([qx, qy, qz], axis=1)
        cos_t = q.sum(axis=1) / (np.sqrt(3) * np.linalg.norm(q, axis=1))
        theta = np.arccos(np.clip(cos_t, -1, 1))
        data.append((qx, qy, qz, lab, theta))

        ax.set_xlabel("$n_x$", labelpad=12)
        ax.set_ylabel("$n_y$", labelpad=12)
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel("$n_z$", rotation=0, labelpad=8)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
        ax.set_xticks([0, .2, .4, .6, .8, 1]); ax.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1"])
        ax.set_yticks([0, .2, .4, .6, .8, 1]); ax.set_yticklabels(["0", "0.2", "0.4", "0.6", "0.8", ""])   # un solo "1"
        ax.set_zticks([0, .2, .4, .6, .8, 1]); ax.set_zticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1"])
        ax.set_box_aspect((1, 1, 1), zoom=0.9)
        ax.view_init(elev=25, azim=45)
        ax.text2D(0.05, 0.9, lat, transform=ax.transAxes, fontsize=28,
                  fontweight="bold", bbox=box)

    # colorbar verticale condivisa, fissa in tutti i frame
    cax = fig.add_axes([0.87, 0.25, 0.015, 0.5])
    cbar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax, ticks=[0, 1, 2])
    cbar.ax.set_yticklabels(labels, fontsize=22)

    # stessa scala angolare per i due reticoli, così crescono in sincrono
    thmax = max(d[4].max() for d in data) * (1 + 1e-9)
    soglie = np.linspace(0, thmax, N)

    if g == 0:
        # animazione di crescita: solo per il primo valore di gamma3
        scatters = [None, None]
        for i, soglia in enumerate(soglie):
            for k, (ax, (qx, qy, qz, lab, theta)) in enumerate(zip(axs, data)):
                if scatters[k] is not None:
                    scatters[k].remove()
                m = theta <= soglia
                scatters[k] = ax.scatter(qx[m], qy[m], qz[m], c=lab[m], cmap=cmap,
                                         norm=norm, s=30, alpha=0.9, linewidths=0,
                                         depthshade=False)
            fig.savefig(f"frames/f_{i:03d}.png", dpi=80)    # 1280x720
        # l'ultimo frame è già il grafico completo: lo salvo anche come png finale
        fig.savefig(f"sphere_SC_FCC_{g}.png", dpi=80)
    else:
        # solo il grafico completo (tutti i punti)
        for ax, (qx, qy, qz, lab, theta) in zip(axs, data):
            ax.scatter(qx, qy, qz, c=lab, cmap=cmap, norm=norm,
                       s=30, alpha=0.9, linewidths=0, depthshade=False)
        fig.savefig(f"sphere_SC_FCC_{g}.png", dpi=80)       # 1280x720

    print(f"Salvato sphere_SC_FCC_{g}.png")
    plt.close(fig)
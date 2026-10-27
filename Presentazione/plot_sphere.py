import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D

# uso: python3 plot_sphere.py
LATTICES = ["SC", "FCC"]
gamma3_val = [1, 1.5, 2, 2.5, 3,3.5,4,4.5,5]          # stessi valori del C++ (stesso ordine)
N_gamma3 = len(gamma3_val)

colors = ['#AA3377', '#228833', '#4477AA']      # palette di Tol, adatta ai daltonici
labels = [r'$L < T_1 \leq T_2$',
          r'$T_1 < L < T_2$',
          r'$T_1 \leq T_2 < L$']
cmap = ListedColormap(colors)
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

# --- stile per proiezione -------------------------------------------
plt.rcParams.update({
    "font.size": 18,
    "axes.labelsize": 24,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "mathtext.fontset": "cm",
})

box_style = dict(boxstyle="round,pad=0.35", facecolor="white",
                 edgecolor="black", linewidth=1.5)

handles = [Line2D([], [], marker="o", linestyle="", markersize=16,
                  markerfacecolor=c, markeredgecolor="none", label=l)
           for c, l in zip(colors, labels)]

for i in range(N_gamma3):
    fig = plt.figure(figsize=(16, 9))               # 16:9, a dpi=120 -> 1920x1080
    axs = [fig.add_subplot(1, 2, k + 1, projection="3d") for k in range(2)]

    for ax, lattice in zip(axs, LATTICES):
        fname = f"{i}_results_{lattice}_sphere.csv"
        try:
            qx, qy, qz, label = np.loadtxt(fname, unpack=True)
        except FileNotFoundError:
            raise SystemExit(f"Errore: il file {fname} non esiste.")

        ax.scatter(qx, qy, qz, c=label, cmap=cmap, norm=norm,
                   s=30, alpha=0.9, linewidths=0, depthshade=False)

        ax.set_xlabel("$q_x$", labelpad=14)
        ax.set_ylabel("$q_y$", labelpad=14)
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel("$q_z$", rotation=0, labelpad=14)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
        ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1]); ax.set_zticks([0, 0.5, 1])
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=25, azim=45)
        ax.text2D(0.05, 0.9, lattice, transform=ax.transAxes,
                  fontsize=28, fontweight="bold", bbox=box_style)

    # legenda unica, grande, sotto i due pannelli
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=24,
               frameon=False, handletextpad=0.3, columnspacing=2.5)

    fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.12, wspace=0.0)

    out = f"sphere_SC_FCC_{i}.png"
    fig.savefig(out, dpi=120)                       # 1920x1080
    print(f"Salvato {out}  (gamma3 = {gamma3_val[i]})")
    plt.close(fig)                                  # libera memoria
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# uso: python3 plot_sphere.py
LATTICES = ["SC", "FCC"]
letters = ["(a)", "(b)"]

#            0: L sotto   1: L in mezzo   2: L sopra
colors = ['#AA3377',     '#228833',      '#4477AA']
cmap = ListedColormap(colors)
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

box_style = dict(boxstyle="round,pad=0.3", facecolor="white",
                 edgecolor="black", alpha=0.9)

fig = plt.figure(figsize=(12, 6))
axs = [fig.add_subplot(1, 2, i + 1, projection="3d") for i in range(2)]

for ax, lattice,letter in zip(axs, LATTICES, letters):
    fname = f"results_{lattice}_sphere.csv"
    try:
        qx, qy, qz, label = np.loadtxt(fname, unpack=True)
    except FileNotFoundError:
        raise SystemExit(f"Errore: il file {fname} non esiste.")

    sc = ax.scatter(qx, qy, qz, c=label, cmap=cmap, norm=norm, s=6)

    ax.set_xlabel("$q_x$"); ax.set_ylabel("$q_y$")
    ax.zaxis.set_rotate_label(False)          
    ax.set_zlabel("$q_z$", rotation=0)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.text2D(0.95, -0.1, letter, transform=ax.transAxes,
              fontsize=15, ha="right", va="bottom")
    ax.view_init(elev=25, azim=45)
    # ax.set_proj_type('ortho')
    ax.text2D(0.05, 0.92, lattice, transform=ax.transAxes,
              fontsize=15, bbox=box_style)

# colorbar unica, condivisa dai due pannelli
cbar = fig.colorbar(sc, ax=axs, ticks=[0, 1, 2], shrink=0.7, pad=0.08)
cbar.ax.set_yticklabels([r'$L < T_1 \leq T_2$', r'$T_1 < L < T_2$', r'$T_1 \leq T_2 < L$'])

fig.savefig("sphere_SC_FCC.png", dpi=200)#bbox_inches="tight"
plt.show()

 
    
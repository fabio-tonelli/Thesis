#-----This script takes the files results_SC.txt or results_FCC.txt  as input and it creates the Many-directions plots (for one file with fixed gamma3)-----

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm


LATTICES = ["SC", "FCC"]
letters = ["(a)", "(b)"]

#            0: L below   1: L middle   2: L over
colors = ['#AA3377',     '#228833',      '#4477AA']
cmap = ListedColormap(colors)
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

box_style = dict(boxstyle="round,pad=0.3", facecolor="white",
                 edgecolor="black", alpha=0.9)

fig = plt.figure(figsize=(12, 6))
axs = [fig.add_subplot(1, 2, i + 1, projection="3d") for i in range(2)]

# Reserve space on the right and create a fixed axis for the colorbar
fig.subplots_adjust(right=0.88)
cax = fig.add_axes([0.91, 0.25, 0.015, 0.5])   

# Create the colorbar ONCE, from a ScalarMappable (norm + cmap), independent of the data
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
cbar = fig.colorbar(sm, cax=cax, ticks=[0, 1, 2])
cbar.ax.set_yticklabels([r'$L < T_1 \leq T_2$', r'$T_1 < L < T_2$', r'$T_1 \leq T_2 < L$'])

# Number of files to plot
N_Files = 9

for file_number in range(N_Files):
    for ax, lattice, letter in zip(axs, LATTICES, letters):
        # Clear the previous scatter (also resets labels, limits and view,
        # which are all set again below)
        ax.cla()

        fname = f"/home/tonelli/Tesi/Multi_Dir/Results/Sphere_Results/Sphere_Results_{lattice}/{file_number}_Sphere_Results_{lattice}.txt"
        try:
            qx, qy, qz, label = np.loadtxt(fname, unpack=True)
        except FileNotFoundError:
            raise SystemExit(f"Error: file {fname} does not exist.")

        # Scatter plot colored by label
        ax.scatter(qx, qy, qz, c=label, cmap=cmap, norm=norm, s=6)

        # Axis labels (z label kept horizontal)
        ax.set_xlabel("$q_x$"); ax.set_ylabel("$q_y$")
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel("$q_z$", rotation=0)

        # Fixed limits and cubic aspect ratio
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
        ax.set_box_aspect((1, 1, 1))

        # Panel letter (bottom right) and lattice name (top left)
        ax.text2D(0.95, -0.1, letter, transform=ax.transAxes,
                  fontsize=15, ha="right", va="bottom")
        ax.text2D(0.05, 0.92, lattice, transform=ax.transAxes,
                  fontsize=15, bbox=box_style)

        # Camera angle
        ax.view_init(elev=25, azim=45)
        # ax.set_proj_type('ortho')

    # Save the figure for this file
    fig.savefig(f"/home/tonelli/Tesi/Multi_Dir/Plots/Sphere_Plots/Sphere_Plot_{file_number}.png", dpi=200)
    # plt.show()
 
    
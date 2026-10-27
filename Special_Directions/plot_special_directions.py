#grafico giusto, solo da sistemare fore gli 0.5

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.ticker import FormatStrFormatter

# --- Parametri -----------------------------------------------------------
epsilon = 1 / 72

COLORS = ['#4477AA', '#AA3377']   # 0 = blu (sotto la retta), 1 = viola (sopra)

# Limiti degli assi (come nel grafico precedente)
x_max = 2.0
y_max = 2.0

# --- Griglia e classificazione ------------------------------------------
x = np.linspace(0, x_max, 800)    # (gamma1 + gamma5)/2
y = np.linspace(0, y_max, 900)    # gamma3
X, Y = np.meshgrid(x, y)

# gamma3 = 18*epsilon + (gamma1 + gamma5)/2
retta = 18 * epsilon + X
cat_code = (Y > retta).astype(int)   # 0 = sotto (blu), 1 = sopra (viola)

CAT_BLU = 0
CAT_VIOLA = 1

# --- Generazione del Grafico (Plot) --------------------------------------
cmap = ListedColormap(COLORS)
bounds = [-0.5, 0.5, 1.5]
norm = BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(8, 6.5))

ax.pcolormesh(x, y, cat_code, cmap=cmap, norm=norm, shading='nearest')

ax.set_xlabel(r"$(\gamma_1 + \gamma_5)/2$", fontsize=14)
ax.set_ylabel(r"$\gamma_3$", fontsize=14)

#ax.grid(True, linestyle='--', alpha=0.3)

# --- Tick dell'asse x: passo fisso (modifica s a piacere) ---------------
s = 0.25   # passo desiderato
ax.set_xticks(np.arange(0, x_max + 1e-9, s))
ax.set_xlim(0, x_max)
ax.set_ylim(0, y_max)
ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f"))

# --- Tick dell'asse y: passo 0.25, con etichetta "18ε = 0.25" ------------
yticks = np.arange(0, y_max + 1e-9, 0.25)
ax.set_yticks(yticks)
ylabels = []
for t in yticks:
    if np.isclose(t, 18 * epsilon):
        ylabels.append(r"$18\,\varepsilon\ =\ 0.25$")
    else:
        ylabels.append(f"{t:.2f}")
ax.set_yticklabels(ylabels)

# --- Riquadri di testo dentro le aree -----------------------------------
def centro_area(cat):
    """Baricentro delle celle appartenenti alla categoria cat."""
    mask = cat_code == cat
    if not mask.any():
        return None
    return X[mask].mean(), Y[mask].mean()

box_style = dict(boxstyle="round,pad=0.4", facecolor="white",
                 edgecolor="black", alpha=0.9)

# Riquadro nell'area blu
c = centro_area(CAT_BLU)
if c is not None:
    ax.text(c[0], c[1], "T < L", ha="center", va="center",
            fontsize=14, bbox=box_style)

# Riquadro nell'area viola
c = centro_area(CAT_VIOLA)
if c is not None:
    ax.text(c[0], c[1], "T > L", ha="center", va="center",
            fontsize=14, bbox=box_style)

ax.text(0.1,1.85, "SC",fontsize=15,bbox=box_style)
plt.tight_layout()
plt.savefig("map_gamma_TL_analytic.png", dpi=150, bbox_inches='tight')
print("Plot generated and saved as 'map_gamma_TL_analytic.png'.")
plt.show()
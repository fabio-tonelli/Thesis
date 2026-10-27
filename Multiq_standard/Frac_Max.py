import numpy as np

INPUT_FILE = "results_SC.csv"
COL = 3   # quarta colonna (indice da 0)

try:
    values = np.loadtxt(INPUT_FILE, usecols=COL)
except FileNotFoundError:
    raise SystemExit(f"Errore: il file {INPUT_FILE} non esiste.")
except IndexError:
    raise SystemExit(f"Errore: la colonna {COL} non esiste nel file.")

imax = np.argmax(values)
print(f"Massimo: {values[imax]}  (riga {imax}, escluse intestazioni)")
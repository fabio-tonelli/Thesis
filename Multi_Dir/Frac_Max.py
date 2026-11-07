#-----This script takes the file results_SC.txt as input and it prints the max value-----
#----- of the fraction of directions in wich any inversion occours.-----
#-----The max is obviously referred to the considerated area of the parameter space.-----

import numpy as np
import argparse

# --- Input arguments ---------------------------------------
parser = argparse.ArgumentParser(description="Frac_Max for SC or FCC lattice")
parser.add_argument("lattice", choices=["SC", "FCC"], help="to be used lattice")
parser.add_argument("--input", default=None,
                    help=" input file (default: 2D_Results_<lattice>.txt)")
args = parser.parse_args()

LATTICE = args.lattice

INPUT_FILE = f"/home/tonelli/Tesi/Multi_Dir/Results/2D_Results/2D_Results_{LATTICE}.txt"
COL = 3   # fourth column (index from 0)

try:
    values = np.loadtxt(INPUT_FILE, usecols=COL)
except FileNotFoundError:
    raise SystemExit(f"Error: the file {INPUT_FILE} does not exist.")
except IndexError:
    raise SystemExit(f"Error: the column {COL} does not exist in the file.")

imax = np.argmax(values)
print(f"Max: {values[imax]}  (row {imax}, headings excluded)")


#estendere anche a FCC
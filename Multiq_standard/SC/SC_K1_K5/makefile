# ---- Configurazione: modifica solo qui se cambi macchina/percorso LAMMPS ----
LAMMPS_DIR := /home/tonelli/lammps-22Jul2025

CXX        := mpicxx
CXXFLAGS   := -O2 -fopenmp -I$(LAMMPS_DIR)/build/includes
LDFLAGS    := -L$(LAMMPS_DIR)/build -Wl,-rpath,$(LAMMPS_DIR)/build
LDLIBS     := -llammps -ljpeg -lpng -lz
ARM		   := -larmadillo

SRC        := main.cpp
CAL        := calc.cpp
# ---- Target di default: build di produzione (log LAMMPS disattivato) ----
all: Main Calc

Main: $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) $(LDFLAGS) $(LDLIBS) -o Main

Calc: $(CAL)
	$(CXX) -O2 $(CAL) $(ARM) -o Calc

# ---- Build di debug: log LAMMPS attivo, per capire errori ----
debug: MainDebug

#definendo la macro per log lammps

MainDebug: $(SRC)
	$(CXX) $(CXXFLAGS) -DDEBUG_LOG $(SRC) $(LDFLAGS) $(LDLIBS)  $(ARM) -o MainDebug 
clean:
	rm -f Main MainDebug

.PHONY: all debug clean
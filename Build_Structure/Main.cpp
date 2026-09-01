#include <cstdio>
#include <fstream>
#include <iostream>
#include <vector>

#include "Class.h"
#include "TPaveText.h"

using namespace std;

int main(int argc, char** argv) {
  if (argc < 2) {
    cout << "Uso: ./Main [fcc|sc]\n";
    return 1;
  }

  string lattice = argv[1];

  if (lattice != "fcc" && lattice != "sc") {
    cout << "Reticolo non riconosciuto\n";
    return 1;
  }

  cout << "Creo reticolo " << lattice << endl;

  // --------------------------
  // Parametri fissi
  // --------------------------

  double r0 = 1;

  double Klj = 1;

  double epsilon = Klj * pow(r0, 2) / 72;

  double k1 = 0;
  double k2 = 0;
  double k3 = 0;
  double k4 = 0;
  double k5 = 0;
  double k6 = 0;

  vector<double> k;

  k.push_back(k1);
  k.push_back(k2);
  k.push_back(k3);
  k.push_back(k4);
  k.push_back(k5);
  k.push_back(k6);
  // NB: ai fini di questo programma k non serve.

  if (lattice == "fcc") {
    Simulation sim(lattice, r0, 5, 1, epsilon, k);

    // crea struttura
    sim.BuildStructure();
  }

  if (lattice == "sc") {
    Simulation sim(lattice, r0, 5, 1, epsilon, k);

    // crea struttura
    sim.BuildStructure();
  }

  return 0;
}
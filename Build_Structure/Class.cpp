#include "Class.h"

#include <math.h>

#include <array>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "TAxis.h"
#include "VectorOperations.h"

using namespace std;

void Simulation::WritePotential() {
  ofstream file("Potential.mod");

  if (!file) {
    cout << "Errore apertura file " << std::endl;
    return;
  }

  // Lennard-Jones

  file << "# -------------------------------\n";
  file << "# Pair potential: Lennard-Jones\n";
  file << "# -------------------------------\n\n";

  double Rc;
  double sigma;
  if (m_Lattice == "fcc") {
    Rc = m_LatticeParameter / sqrt(2) * 1.05;

    sigma = m_LatticeParameter / (sqrt(2) * pow(2, 1.0 / 6.0));

  }

  else if (m_Lattice == "sc") {
    Rc = m_LatticeParameter * 1.05;

    sigma = m_LatticeParameter / pow(2, 1.0 / 6.0);

  } else {
    cout << "unknown lattice selected" << endl;
    return;
  }

  file << "variable epsilon equal " << m_epsilon << "\n";
  file << "variable Rc equal " << Rc << "\n\n ";

  file << "variable epsilon equal " << m_epsilon << "\n";
  file << "variable sigma equal " << sigma << "\n\n";

  file << "pair_style lj/cut ${Rc}\n";
  file << "pair_coeff 1 1 ${epsilon} ${sigma}\n\n\n";

  // Potenziale angolare

  file << "# -------------------------------\n";
  file << "# Three body angular potential\n";
  file << "# -------------------------------\n\n";

  file << "angle_style cosine/delta\n\n";

  // da modificare, se è lattice=fcc deve stampare solo i k dell'fcc
  for (size_t i = 0; i < m_k.size(); i++) {
    file << "variable k" << i + 1 << " equal " << m_k[i] << "\n";
  }

  file << "\n";

  // angoli
  if (m_Lattice == "fcc") {
    file << "angle_coeff 1 ${k2} 60.0\n";
    file << "angle_coeff 2 ${k3} 90.0\n";
    file << "angle_coeff 3 ${k4} 120.0\n";
    file << "angle_coeff 4 ${k6} 180.0\n";
  } else if (m_Lattice == "sc") {
    file << "angle_coeff 1 ${k1} 45.0\n";
    file << "angle_coeff 2 ${k2} 60.0\n";
    file << "angle_coeff 3 ${k3} 90.0\n";
    file << "angle_coeff 4 ${k4} 120.0\n";
    file << "angle_coeff 5 ${k5} 135.0\n";
    file << "angle_coeff 6 ${k6} 180.0\n";
  }

  file.close();
}

void Simulation::RunMinimize() {
  cout << "Running minimization...\n";

  int result =
      system(" ~/lammps-22Jul2025/build/lmp -in in.minimize > /dev/null  ");

  if (result != 0) {
    cout << "Errore durante la minimizzazione LAMMPS\n";
    exit(1);
  }

  cout << "Minimization completed.\n";
}

void Simulation::BuildStructure() {
  if (m_Lattice == "fcc") {
    FCCLattice lattice(m_LatticeParameter, m_NumCells, m_AtomType);

    lattice.PrintLAMMPSData("structure_fcc.data");
  }

  else if (m_Lattice == "sc") {
    SCLattice lattice(m_LatticeParameter, m_NumCells, m_AtomType);

    lattice.PrintLAMMPSData("structure_sc.data");
  }

  else {
    cerr << "Errore: tipo di reticolo non riconosciuto: " << m_Lattice << endl;
    exit(1);
  }
}

void Simulation::RunElastic() {
  // Esegue LAMMPS
  int status =
      system("~/lammps-22Jul2025/build/lmp -in in.elastic > /dev/null  ");  //

  if (status != 0) {
    std::cerr << "Errore durante l'esecuzione di in.elastic." << std::endl;
    return;
  }

  std::ifstream log("log.lammps");
  if (!log) {
    std::cerr << "Impossibile aprire log.lammps." << std::endl;
    return;
  }

  /*
  std::string line;

  while (std::getline(log, line)) {
    if (sscanf(line.c_str(), "Elastic Constant C11all = %lf", &C11) == 1)
      continue;

    if (sscanf(line.c_str(), "Elastic Constant C12all = %lf", &C12) == 1)
      continue;

    if (sscanf(line.c_str(), "Elastic Constant C44all = %lf", &C44) == 1)
      continue;

    // Se vuoi leggere tutte le costanti:

    sscanf(line.c_str(), "Elastic Constant C22all = %lf", &C22);
    sscanf(line.c_str(), "Elastic Constant C33all = %lf", &C33);
    sscanf(line.c_str(), "Elastic Constant C13all = %lf", &C13);
    sscanf(line.c_str(), "Elastic Constant C23all = %lf", &C23);
    sscanf(line.c_str(), "Elastic Constant C55all = %lf", &C55);
    sscanf(line.c_str(), "Elastic Constant C66all = %lf", &C66);
  }

  log.close();

  */
}
// Functions needed for the constructor of the Triplet class

void Simulation::ComputeWaveVelocities(unsigned int n1, unsigned int n2) {
  if (m_Lattice == "fcc") {
    if (n1 == 2 && n2 == 3) {
      ifstream file("elastic_constantsfcc_k2_k3.dat");

      if (!file) {
        cout << "Errore apertura elastic_constantsfcc_k2_k3.dat\n";
        return;
      }

      // ==============================
      // Scrittura intestazione
      // ==============================

      ofstream out("wave_velocitiesfcc_k2_k3.dat");

      out << "# Wave velocities\n";
      out << "# Lattice = " << m_Lattice << "\n";
      out << "# a = " << m_LatticeParameter << "\n";
      out << "# epsilon = " << m_epsilon << "\n";
      out << "# k1 = " << m_k[0] << "\n";
      // out << "# k2 = " << m_k[1] << "\n";
      out << "# k4 = " << m_k[3] << "\n";
      out << "# k5 = " << m_k[4] << "\n";
      out << "# k6 = " << m_k[5] << "\n";
      out << "#\n";

      out << "# k2 "
          << "k3 "
          << "L100 T100 "
          << "L110 T110_1 T110_2 "
          << "L111 T111\n";

      double k2, k3;
      double C11, C12, C44;

      string line;

      while (getline(file, line)) {
        // salta commenti e righe vuote
        if (line.empty() || line[0] == '#') continue;

        stringstream ss(line);

        if (ss >> k2 >> k3 >> C11 >> C12 >> C44) {
          // ==============================
          // velocità relative
          // ==============================

          double L100 = C11;

          double T100 = C44;

          double L110 = (C11 + C12 + 2 * C44) / 2.0;

          double T110_1 = (C11 - C12) / 2.0;

          double T110_2 = C44;

          double L111 = (C11 + 2 * C12 + 4 * C44) / 3.0;

          double T111 = (C11 - C12 + C44) / 3.0;

          out << k2 << " " << k3 << " " << L100 << " " << T100 << " " << L110
              << " " << T110_1 << " " << T110_2 << " " << L111 << " " << T111
              << endl;
        }
      }

      out.close();

      file.close();
    }

    if (n1 == 2 && n2 == 4) {
      ifstream file("elastic_constantsfcc_k2_k4.dat");

      if (!file) {
        cout << "Errore apertura elastic_constantsfcc_k2_k4.dat\n";
        return;
      }

      // ==============================
      // Scrittura intestazione
      // ==============================

      ofstream out("wave_velocitiesfcc_k2_k4.dat");

      out << "# Wave velocities\n";
      out << "# Lattice = " << m_Lattice << "\n";
      out << "# a = " << m_LatticeParameter << "\n";
      out << "# epsilon = " << m_epsilon << "\n";
      out << "# k1 = " << m_k[0] << "\n";
      // out << "# k2 = " << m_k[1] << "\n";
      out << "# k3 = " << m_k[2] << "\n";
      // out << "# k4 = " << m_k[3] << "\n";
      out << "# k5 = " << m_k[4] << "\n";
      out << "# k6 = " << m_k[5] << "\n";
      out << "#\n";

      out << "# k2 "
          << "k4 "
          << "L100 T100 "
          << "L110 T110_1 T110_2 "
          << "L111 T111\n";

      double k2, k4;
      double C11, C12, C44;

      string line;

      while (getline(file, line)) {
        // salta commenti e righe vuote
        if (line.empty() || line[0] == '#') continue;

        stringstream ss(line);

        if (ss >> k2 >> k4 >> C11 >> C12 >> C44) {
          // ==============================
          // velocità relative
          // ==============================

          double L100 = C11;

          double T100 = C44;

          double L110 = (C11 + C12 + 2 * C44) / 2.0;

          double T110_1 = (C11 - C12) / 2.0;

          double T110_2 = C44;

          double L111 = (C11 + 2 * C12 + 4 * C44) / 3.0;

          double T111 = (C11 - C12 + C44) / 3.0;

          out << k2 << " " << k4 << " " << L100 << " " << T100 << " " << L110
              << " " << T110_1 << " " << T110_2 << " " << L111 << " " << T111
              << endl;
        }
      }

      out.close();

      file.close();
    }
  }

  if (m_Lattice == "sc") {
    if (n1 == 1 && n2 == 3) {
      ifstream file("elastic_constantssc_k1_k3.dat");

      if (!file) {
        cout << "Errore apertura elastic_constantssc_k1_k3.dat\n";
        return;
      }

      // ==============================
      // Scrittura intestazione
      // ==============================

      ofstream out("wave_velocitiessc_k1_k3.dat");

      out << "# Wave velocities\n";
      out << "# Lattice = " << m_Lattice << "\n";
      out << "# a = " << m_LatticeParameter << "\n";
      out << "# epsilon = " << m_epsilon << "\n";
      // out << "# k1 = " << m_k[0] << "\n";
      out << "# k2 = " << m_k[1] << "\n";
      out << "# k4 = " << m_k[3] << "\n";
      out << "# k5 = " << m_k[4] << "\n";
      out << "# k6 = " << m_k[5] << "\n";
      out << "#\n";

      out << "# k1 "
          << "k3 "
          << "L100 T100 "
          << "L110 T110_1 T110_2 "
          << "L111 T111\n";

      double k1, k3;
      double C11, C12, C44;

      string line;

      while (getline(file, line)) {
        // salta commenti e righe vuote
        if (line.empty() || line[0] == '#') continue;

        stringstream ss(line);

        if (ss >> k1 >> k3 >> C11 >> C12 >> C44) {
          // ==============================
          // velocità relative
          // ==============================

          double L100 = C11;

          double T100 = C44;

          double L110 = (C11 + C12 + 2 * C44) / 2.0;

          double T110_1 = (C11 - C12) / 2.0;

          double T110_2 = C44;

          double L111 = (C11 + 2 * C12 + 4 * C44) / 3.0;

          double T111 = (C11 - C12 + C44) / 3.0;

          out << k1 << " " << k3 << " " << L100 << " " << T100 << " " << L110
              << " " << T110_1 << " " << T110_2 << " " << L111 << " " << T111
              << endl;
        }
      }

      out.close();

      file.close();
    }

    if (n1 == 1 && n2 == 5) {
      ifstream file("elastic_constantssc_k1_k5.dat");

      if (!file) {
        cout << "Errore apertura elastic_constantssc_k1_k5.dat\n";
        return;
      }

      // ==============================
      // Scrittura intestazione
      // ==============================

      ofstream out("wave_velocitiessc_k1_k5.dat");

      out << "# Wave velocities\n";
      out << "# Lattice = " << m_Lattice << "\n";
      out << "# a = " << m_LatticeParameter << "\n";
      out << "# epsilon = " << m_epsilon << "\n";
      // out << "# k1 = " << m_k[0] << "\n";
      out << "# k2 = " << m_k[1] << "\n";
      out << "# k3 = " << m_k[2] << "\n";
      out << "# k4 = " << m_k[3] << "\n";
      // out << "# k5 = " << m_k[4] << "\n";
      out << "# k6 = " << m_k[5] << "\n";
      out << "#\n";

      out << "# k1 "
          << "k5 "
          << "L100 T100 "
          << "L110 T110_1 T110_2 "
          << "L111 T111\n";

      double k1, k5;
      double C11, C12, C44;

      string line;

      while (getline(file, line)) {
        // salta commenti e righe vuote
        if (line.empty() || line[0] == '#') continue;

        stringstream ss(line);

        if (ss >> k1 >> k5 >> C11 >> C12 >> C44) {
          // ==============================
          // velocità relative
          // ==============================

          double L100 = C11;

          double T100 = C44;

          double L110 = (C11 + C12 + 2 * C44) / 2.0;

          double T110_1 = (C11 - C12) / 2.0;

          double T110_2 = C44;

          double L111 = (C11 + 2 * C12 + 4 * C44) / 3.0;

          double T111 = (C11 - C12 + C44) / 3.0;

          out << k1 << " " << k5 << " " << L100 << " " << T100 << " " << L110
              << " " << T110_1 << " " << T110_2 << " " << L111 << " " << T111
              << endl;
        }
      }

      out.close();

      file.close();
    }
  }
}

void Simulation::ReadElasticConstants(double param1, double param2,
                                      unsigned int n1, unsigned int n2) {
  std::ifstream log("log.lammps");

  if (!log) {
    std::cerr << "Errore: impossibile aprire log.lammps\n";
    return;
  }

  C11 = C12 = C44 = 0.0;

  std::string line;

  while (std::getline(log, line)) {
    sscanf(line.c_str(), "Elastic Constant C11all = %lf", &C11);

    sscanf(line.c_str(), "Elastic Constant C12all = %lf", &C12);

    sscanf(line.c_str(), "Elastic Constant C44all = %lf", &C44);
  }

  log.close();

  if (m_Lattice == "sc") {
    if (n1 == 1 && n2 == 3) {
      std::ofstream out("elastic_constantssc_k1_k3.dat", std::ios::app);

      if (!out) {
        std::cerr << "Errore apertura elastic_constantssc_k1_k3.dat\n";
        return;
      }
      out << "# Elastic constants from LAMMPS\n";
      out << "#\n";
      out << "# k1"
          << "\tk3"
          << "\tC11"
          << "\tC12"
          << "\tC44\n";
      out << param1 << " " << param2 << " " << C11 << " " << C12 << " " << C44
          << "\n";

      out.close();
    }
    if (n1 == 1 && n2 == 5) {
      std::ofstream out("elastic_constantssc_k1_k5.dat", std::ios::app);

      if (!out) {
        std::cerr << "Errore apertura elastic_constantssc_k1_k5.dat\n";
        return;
      }
      out << "# Elastic constants from LAMMPS\n";
      out << "#\n";
      out << "# k1"
          << "\tk5"
          << "\tC11"
          << "\tC12"
          << "\tC44\n";
      out << param1 << " " << param2 << " " << C11 << " " << C12 << " " << C44
          << "\n";

      out.close();
    }
  }

  if (m_Lattice == "fcc") {
    if (n1 == 2 && n2 == 3) {
      std::ofstream out("elastic_constantsfcc_k2_k3.dat", std::ios::app);

      if (!out) {
        std::cerr << "Errore apertura elastic_constantsfcc_k2_k3.dat\n";
        return;
      }
      out << "# Elastic constants from LAMMPS\n";
      out << "#\n";
      out << "# k2"
          << "\tk3"
          << "\tC11"
          << "\tC12"
          << "\tC44\n";
      out << param1 << " " << param2 << " " << C11 << " " << C12 << " " << C44
          << "\n";

      out.close();
    }
    if (n1 == 2 && n2 == 4) {
      std::ofstream out("elastic_constantsfcc_k2_k4.dat", std::ios::app);

      if (!out) {
        std::cerr << "Errore apertura elastic_constantsfcc_k2_k4.dat\n";
        return;
      }
      out << "# Elastic constants from LAMMPS\n";
      out << "#\n";
      out << "# k2"
          << "\tk4"
          << "\tC11"
          << "\tC12"
          << "\tC44\n";
      out << param1 << " " << param2 << " " << C11 << " " << C12 << " " << C44
          << "\n";

      out.close();
    }
  }
}
// Compute the angle formed by the three atoms
// NB: the second is the vertex of the angle
double ComputeAngle(const Triplet& t) {
  double v1x = t.getAtom1().getX() - t.getAtom2().getX();
  double v1y = t.getAtom1().getY() - t.getAtom2().getY();
  double v1z = t.getAtom1().getZ() - t.getAtom2().getZ();

  double v2x = t.getAtom3().getX() - t.getAtom2().getX();
  double v2y = t.getAtom3().getY() - t.getAtom2().getY();
  double v2z = t.getAtom3().getZ() - t.getAtom2().getZ();

  double dot_product = v1x * v2x + v1y * v2y + v1z * v2z;
  double mag_v1 = sqrt(v1x * v1x + v1y * v1y + v1z * v1z);
  double mag_v2 = sqrt(v2x * v2x + v2y * v2y + v2z * v2z);

  double cosTheta = dot_product / (mag_v1 * mag_v2);

  // Clamp per evitare errori di dominio in acos dovuti a floating-point
  // rounding
  cosTheta = std::max(-1.0, std::min(1.0, cosTheta));

  return acos(cosTheta);
}

// FindTypeSC
unsigned int FindTypeSC(const Triplet& t) {
  double Theta = ComputeAngle(t);

  double tolerance =
      1e-6;  // Define a small tolerance for floating-point comparison

  double Theta1 = M_PI / 4;      // 45 degrees in radians
  double Theta2 = M_PI / 3;      // 60 degrees in radians
  double Theta3 = M_PI / 2;      // 90 degrees in radians
  double Theta4 = 2 * M_PI / 3;  // 120 degrees in radians
  double Theta5 = 3 * M_PI / 4;  // 135 degrees in radians
  double Theta6 = M_PI;          // 180 degrees in radians

  // Type 1: 45 degrees (right angle)
  if (abs(Theta - Theta1) < tolerance) {
    return 1;
  }
  // Type 2: 60 degrees (straight line)
  else if (abs(Theta - Theta2) < tolerance) {
    return 2;
  }
  // Type 3: 90 degrees (equilateral triangle)
  else if (abs(Theta - Theta3) < tolerance) {
    return 3;
  }
  // Type 4: 120 degrees (obtuse angle)
  else if (abs(Theta - Theta4) < tolerance) {
    return 4;
  }
  // Type 5: 135 degrees
  else if (abs(Theta - Theta5) < tolerance) {
    return 5;
  }
  // Type 6: 180 degrees
  else if (abs(Theta - Theta6) < tolerance) {
    return 6;
  }

  // If none of the above, return 0 (undefined type)
  else {
    return 0;
  }
}
// FindTypeFCC
unsigned int FindTypeFCC(const Triplet& t) {
  double Theta = ComputeAngle(t);

  double tolerance =
      1e-6;  // Define a small tolerance for floating-point comparison

  double Theta2 = M_PI / 3;      // 60 degrees in radians
  double Theta3 = M_PI / 2;      // 90 degrees in radians
  double Theta4 = 2 * M_PI / 3;  // 120 degrees in radians
  double Theta6 = M_PI;          // 180 degrees in radians

  // Type 2: 60 degrees
  if (abs(Theta - Theta2) < tolerance) {
    return 1;
  }
  // Type 3: 90 degrees
  else if (abs(Theta - Theta3) < tolerance) {
    return 2;
  }
  // Type 4: 120 degrees
  else if (abs(Theta - Theta4) < tolerance) {
    return 3;
  }
  // Type 6: 180 degrees
  else if (abs(Theta - Theta6) < tolerance) {
    return 4;
  }

  // If none of the above, return 0 (undefined type)
  else {
    return 0;
  }
}

// Constructors of the Triplet class

// FCC
Triplet::Triplet(Atom a1, Atom a2, Atom a3, FCCTag)
    : atom1(a1), atom2(a2), atom3(a3) {
  theta = ComputeAngle(*this);
  Type = FindTypeFCC(*this);
}

// SC
Triplet::Triplet(Atom a1, Atom a2, Atom a3, SCTag)
    : atom1(a1), atom2(a2), atom3(a3) {
  theta = ComputeAngle(*this);
  Type = FindTypeSC(*this);
}

// FCC Lattice class methods

// BuildAtoms
void FCCLattice::BuildAtoms() {
  // Riserva memoria per evitare riallocazioni
  atoms.reserve(4 * NumCells * NumCells * NumCells);

  unsigned int atomID = 0;

  for (int i = 0; i < NumCells; ++i) {
    for (int j = 0; j < NumCells; ++j) {
      for (int k = 0; k < NumCells; ++k) {
        // Basis 0 : (0,0,0)
        atomIndex[i][j][k][0] = atoms.size();  // this way i know the index of
                                               // an atom in the atom structure
        atoms.emplace_back(i * LatticeParameter, j * LatticeParameter,
                           k * LatticeParameter, AtomType, atomID++);

        // Basis 1 : (1/2,1/2,0)
        atomIndex[i][j][k][1] = atoms.size();
        atoms.emplace_back((i + 0.5) * LatticeParameter,
                           (j + 0.5) * LatticeParameter, k * LatticeParameter,
                           AtomType, atomID++);

        // Basis 2 : (1/2,0,1/2)
        atomIndex[i][j][k][2] = atoms.size();
        atoms.emplace_back((i + 0.5) * LatticeParameter, j * LatticeParameter,
                           (k + 0.5) * LatticeParameter, AtomType, atomID++);

        // Basis 3 : (0,1/2,1/2)
        atomIndex[i][j][k][3] = atoms.size();
        atoms.emplace_back(i * LatticeParameter, (j + 0.5) * LatticeParameter,
                           (k + 0.5) * LatticeParameter, AtomType, atomID++);
      }
    }
  }
}
// BuildNeighbourList
void FCCLattice::BuildNeighbourLists() {
  // FCC conventional cell:
  //
  // basis 0 = (0,   0,   0)
  // basis 1 = (1/2, 1/2, 0)
  // basis 2 = (1/2, 0,   1/2)
  // basis 3 = (0,   1/2, 1/2)

  firstNeighbours.resize(atoms.size());
  secondNeighbours.resize(atoms.size());

  const double basisCoord[4][3] = {
      {0.0, 0.0, 0.0}, {0.5, 0.5, 0.0}, {0.5, 0.0, 0.5}, {0.0, 0.5, 0.5}};

  for (int i = 0; i < NumCells; ++i) {
    for (int j = 0; j < NumCells; ++j) {
      for (int k = 0; k < NumCells; ++k) {
        for (int basis = 0; basis < 4; ++basis) {
          int atom = atomIndex[i][j][k][basis];

          int nFirst = 0;
          int nSecond = 0;

          // Search neighbouring cells
          for (int di = -1; di <= 1; ++di) {
            for (int dj = -1; dj <= 1; ++dj) {
              for (int dk = -1; dk <= 1; ++dk) {
                for (int b = 0; b < 4; ++b) {
                  // Skip the atom itself
                  if (di == 0 && dj == 0 && dk == 0 && b == basis) {
                    continue;
                  }

                  double dx = di + basisCoord[b][0] - basisCoord[basis][0];

                  double dy = dj + basisCoord[b][1] - basisCoord[basis][1];

                  double dz = dk + basisCoord[b][2] - basisCoord[basis][2];

                  double r2 = dx * dx + dy * dy + dz * dz;

                  int ni = (i + di + NumCells) % NumCells;
                  int nj = (j + dj + NumCells) % NumCells;
                  int nk = (k + dk + NumCells) % NumCells;

                  int neighbour = atomIndex[ni][nj][nk][b];

                  if (neighbour == atom) {
                    cout << "ERRORE: atom " << atom
                         << " trovato come proprio vicino!"
                         << " di=" << di << " dj=" << dj << " dk=" << dk
                         << " b=" << b << " r2=" << r2 << endl;
                  }
                  // First neighbours
                  if (std::abs(r2 - 0.5) < 1e-10) {
                    firstNeighbours[atom][nFirst] = neighbour;

                    ++nFirst;
                  }

                  // Second neighbours
                  else if (std::abs(r2 - 1.0) < 1e-10) {
                    secondNeighbours[atom][nSecond] = neighbour;

                    ++nSecond;
                  }
                }
              }
            }
          }

          // Check that the number of neighbours is correct
          if (nFirst != 12) {
            std::cerr << "ERROR: atom " << atom << " has " << nFirst
                      << " first neighbours instead of 12\n";
          }

          if (nSecond != 6) {
            std::cerr << "ERROR: atom " << atom << " has " << nSecond
                      << " second neighbours instead of 6\n";
          }
        }
      }
    }
  }
}
// BuildTriplets
void FCCLattice::BuildTriplets() {
  triplets.clear();

  double L = NumCells * LatticeParameter;

  // For every atom, use it as the central atom
  for (int j = 0; j < atoms.size(); ++j) {
    const Atom& central = atoms[j];

    // The central atom has 12 first neighbours
    for (int n1 = 0; n1 < 12; ++n1) {
      int i = firstNeighbours[j][n1];

      // Copy the neighbour and move it to the closest periodic image
      Atom atom1 = atoms[i];

      double dx = atom1.getX() - central.getX();
      double dy = atom1.getY() - central.getY();
      double dz = atom1.getZ() - central.getZ();

      dx -= L * std::round(dx / L);
      dy -= L * std::round(dy / L);
      dz -= L * std::round(dz / L);

      atom1.setX(central.getX() + dx);
      atom1.setY(central.getY() + dy);
      atom1.setZ(central.getZ() + dz);

      // Choose a second neighbour of j
      for (int n2 = n1 + 1; n2 < 12; ++n2) {
        int k = firstNeighbours[j][n2];

        // Copy the second neighbour and move it to the closest periodic image
        Atom atom3 = atoms[k];

        dx = atom3.getX() - central.getX();
        dy = atom3.getY() - central.getY();
        dz = atom3.getZ() - central.getZ();

        dx -= L * std::round(dx / L);
        dy -= L * std::round(dy / L);
        dz -= L * std::round(dz / L);

        atom3.setX(central.getX() + dx);
        atom3.setY(central.getY() + dy);
        atom3.setZ(central.getZ() + dz);

        // Build the triplet
        triplets.emplace_back(atom1, central, atom3, FCCTag{});
      }
    }
  }
  // conrol over 0 type triplet
  /*
  int c1 = 0, c2 = 0, c3 = 0, c4 = 0, c0 = 0;

  for (const auto& t : triplets) {
    switch (t.getType()) {
      case 1:
        ++c1;
        break;
      case 2:
        ++c2;
        break;
      case 3:
        ++c3;
        break;
      case 4:
        ++c4;
        break;
      default:
        ++c0;
        break;
    }
  }

  std::cout << "Triplets: " << triplets.size() << '\n';
  std::cout << "Type 1: " << c1 << '\n';
  std::cout << "Type 2: " << c2 << '\n';
  std::cout << "Type 3: " << c3 << '\n';
  std::cout << "Type 4: " << c4 << '\n';
  std::cout << "Undefined: " << c0 << '\n';
  */
}

// getN FCC
unsigned int FCCLattice::getNatoms() { return atoms.size(); }

unsigned int FCCLattice::getNangles() { return triplets.size(); }

// Print .Data LAAMPS FCC
void FCCLattice::PrintLAMMPSData(const string& filename) const {
  ofstream output(filename);

  if (!output.is_open()) {
    cout << "Errore: impossibile aprire il file " << filename << endl;
    return;
  }

  // -------------------------------------------------
  // Header
  // -------------------------------------------------

  output << "LAMMPS data file for FCC lattice\n\n";

  output << atoms.size() << " atoms\n";
  output << triplets.size() << " angles\n\n";

  output << "1 atom types\n";
  output << "4 angle types\n\n";

  // -------------------------------------------------
  // Simulation box
  // -------------------------------------------------

  double boxSize = NumCells * LatticeParameter;

  output << "0.0 " << boxSize << " xlo xhi\n";
  output << "0.0 " << boxSize << " ylo yhi\n";
  output << "0.0 " << boxSize << " zlo zhi\n\n";

  // -------------------------------------------------
  // Masses
  // -------------------------------------------------

  output << "Masses\n\n";

  output << "1 1.0\n\n";

  // -------------------------------------------------
  // Atoms
  // -------------------------------------------------

  output << "Atoms\n\n";

  for (const Atom& atom : atoms) {
    output << atom.getId() + 1 << " " << 1 << " " << atom.getType() << " "
           << atom.getX() << " " << atom.getY() << " " << atom.getZ() << "\n";
  }

  output << "\n";

  // -------------------------------------------------
  // Angles
  // -------------------------------------------------

  output << "Angles\n\n";

  int angleID = 1;

  for (const Triplet& triplet : triplets) {
    output << angleID << " " << triplet.getType() << " "
           << triplet.getAtom1().getId() + 1 << " "
           << triplet.getAtom2().getId() + 1 << " "
           << triplet.getAtom3().getId() + 1 << "\n";

    ++angleID;
  }

  output.close();
}

// periodic lattice condition FCC
Atom FCCLattice::ClosestImage(const Atom& atom, const Atom& reference) const {
  Atom image = atom;

  double L = NumCells * LatticeParameter;

  double dx = atom.getX() - reference.getX();
  double dy = atom.getY() - reference.getY();
  double dz = atom.getZ() - reference.getZ();

  dx -= L * std::round(dx / L);
  dy -= L * std::round(dy / L);
  dz -= L * std::round(dz / L);

  image.setX(reference.getX() + dx);
  image.setY(reference.getY() + dy);
  image.setZ(reference.getZ() + dz);

  return image;
}

// SC Lattice class methods

// BuildAtoms  //aggiornato
void SCLattice::BuildAtoms() {
  // Riserva memoria
  atoms.reserve(NumCells * NumCells * NumCells);

  unsigned int atomID = 0;

  for (int i = 0; i < NumCells; ++i) {
    for (int j = 0; j < NumCells; ++j) {
      for (int k = 0; k < NumCells; ++k) {
        // Unica base: (0,0,0)
        atomIndex[i][j][k][0] = atoms.size();

        atoms.emplace_back(i * LatticeParameter, j * LatticeParameter,
                           k * LatticeParameter, AtomType, atomID++);
      }
    }
  }
}
// BuildNeighbourList
void SCLattice::BuildNeighbourLists() {
  firstNeighbours.resize(atoms.size());
  secondNeighbours.resize(atoms.size());

  for (int i = 0; i < NumCells; ++i) {
    for (int j = 0; j < NumCells; ++j) {
      for (int k = 0; k < NumCells; ++k) {
        int atom = atomIndex[i][j][k][0];

        int nFirst = 0;
        int nSecond = 0;

        // Search neighbouring cells
        for (int di = -1; di <= 1; ++di) {
          for (int dj = -1; dj <= 1; ++dj) {
            for (int dk = -1; dk <= 1; ++dk) {
              // Skip the atom itself
              if (di == 0 && dj == 0 && dk == 0) continue;

              double r2 = di * di + dj * dj + dk * dk;

              int ni = (i + di + NumCells) % NumCells;
              int nj = (j + dj + NumCells) % NumCells;
              int nk = (k + dk + NumCells) % NumCells;

              int neighbour = atomIndex[ni][nj][nk][0];

              // First neighbours: distance a
              if (std::abs(r2 - 1.0) < 1e-10) {
                firstNeighbours[atom][nFirst] = neighbour;
                ++nFirst;
              }

              // Second neighbours: distance sqrt(2)*a
              else if (std::abs(r2 - 2.0) < 1e-10) {
                secondNeighbours[atom][nSecond] = neighbour;
                ++nSecond;
              }
            }
          }
        }

        // Check
        if (nFirst != 6) {
          std::cerr << "ERROR: atom " << atom << " has " << nFirst
                    << " first neighbours instead of 6\n";
        }

        if (nSecond != 12) {
          std::cerr << "ERROR: atom " << atom << " has " << nSecond
                    << " second neighbours instead of 12\n";
        }
      }
    }
  }
}
// BuildTriplets
void SCLattice::BuildTriplets() {
  triplets.clear();

  double L = NumCells * LatticeParameter;

  // For every atom, use it as the central atom
  for (int j = 0; j < atoms.size(); ++j) {
    const Atom& central = atoms[j];

    // Create angular neighbour list:
    // 6 first neighbours + 12 second neighbours
    vector<int> angularNeighbours;

    for (int n = 0; n < 6; ++n)
      angularNeighbours.push_back(firstNeighbours[j][n]);

    for (int n = 0; n < 12; ++n)
      angularNeighbours.push_back(secondNeighbours[j][n]);

    // Create all possible angles
    for (int n1 = 0; n1 < angularNeighbours.size(); ++n1) {
      int i = angularNeighbours[n1];

      Atom atom1 = atoms[i];

      // Move atom1 to closest periodic image
      double dx = atom1.getX() - central.getX();
      double dy = atom1.getY() - central.getY();
      double dz = atom1.getZ() - central.getZ();

      dx -= L * std::round(dx / L);
      dy -= L * std::round(dy / L);
      dz -= L * std::round(dz / L);

      atom1.setX(central.getX() + dx);
      atom1.setY(central.getY() + dy);
      atom1.setZ(central.getZ() + dz);

      for (int n2 = n1 + 1; n2 < angularNeighbours.size(); ++n2) {
        int k = angularNeighbours[n2];

        Atom atom3 = atoms[k];

        // Move atom3 to closest periodic image
        dx = atom3.getX() - central.getX();
        dy = atom3.getY() - central.getY();
        dz = atom3.getZ() - central.getZ();

        dx -= L * std::round(dx / L);
        dy -= L * std::round(dy / L);
        dz -= L * std::round(dz / L);

        atom3.setX(central.getX() + dx);
        atom3.setY(central.getY() + dy);
        atom3.setZ(central.getZ() + dz);

        // Build triplet SC
        triplets.emplace_back(atom1, central, atom3, SCTag{});
      }
    }
  }
}

// getN
unsigned int SCLattice::getNatoms() { return atoms.size(); }

unsigned int SCLattice::getNangles() { return triplets.size(); }

// Print .Data LAAMPS
void SCLattice::PrintLAMMPSData(const string& filename) const {
  ofstream output(filename);

  if (!output.is_open()) {
    cout << "Errore: impossibile aprire il file " << filename << endl;
    return;
  }

  // -------------------------------------------------
  // Header
  // -------------------------------------------------

  output << "LAMMPS data file for SC lattice\n\n";

  output << atoms.size() << " atoms\n";
  output << triplets.size() << " angles\n\n";

  output << "1 atom types\n";
  output << "6 angle types\n\n";

  // -------------------------------------------------
  // Simulation box
  // -------------------------------------------------

  double boxSize = NumCells * LatticeParameter;

  output << "0.0 " << boxSize << " xlo xhi\n";
  output << "0.0 " << boxSize << " ylo yhi\n";
  output << "0.0 " << boxSize << " zlo zhi\n\n";

  // -------------------------------------------------
  // Masses
  // -------------------------------------------------

  output << "Masses\n\n";

  output << "1 1.0\n\n";

  // -------------------------------------------------
  // Atoms
  // -------------------------------------------------

  output << "Atoms\n\n";

  for (const Atom& atom : atoms) {
    output << atom.getId() + 1 << " " << 1 << " " << atom.getType() << " "
           << atom.getX() << " " << atom.getY() << " " << atom.getZ() << "\n";
  }

  output << "\n";

  // -------------------------------------------------
  // Angles
  // -------------------------------------------------

  output << "Angles\n\n";

  int angleID = 1;

  for (const Triplet& triplet : triplets) {
    output << angleID << " " << triplet.getType() << " "
           << triplet.getAtom1().getId() + 1 << " "
           << triplet.getAtom2().getId() + 1 << " "
           << triplet.getAtom3().getId() + 1 << "\n";

    ++angleID;
  }

  output.close();
}

// periodic lattice condition
Atom SCLattice::ClosestImage(const Atom& atom, const Atom& reference) const {
  Atom image = atom;

  double L = NumCells * LatticeParameter;

  double dx = atom.getX() - reference.getX();
  double dy = atom.getY() - reference.getY();
  double dz = atom.getZ() - reference.getZ();

  dx -= L * std::round(dx / L);
  dy -= L * std::round(dy / L);
  dz -= L * std::round(dz / L);

  image.setX(reference.getX() + dx);
  image.setY(reference.getY() + dy);
  image.setZ(reference.getZ() + dz);

  return image;
}
// conrol over 0 type triplet
/*
int c1 = 0, c2 = 0, c3 = 0, c4 = 0, c0 = 0;

for (const auto& t : triplets) {
  switch (t.getType()) {
    case 1:
      ++c1;
      break;
    case 2:
      ++c2;
      break;
    case 3:
      ++c3;
      break;
    case 4:
      ++c4;
      break;
    default:
      ++c0;
      break;
  }
}

std::cout << "Triplets: " << triplets.size() << '\n';
std::cout << "Type 1: " << c1 << '\n';
std::cout << "Type 2: " << c2 << '\n';
std::cout << "Type 3: " << c3 << '\n';
std::cout << "Type 4: " << c4 << '\n';
std::cout << "Undefined: " << c0 << '\n';
*/

#ifndef CLASS_H
#define CLASS_H

#include <math.h>

#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "VectorOperations.h"

using namespace std;

class Simulation {
 public:
  // default constructor
  Simulation() { ; };

  // oprative constructor
  Simulation(string LatticeType, double r0, int NumCells, int AtomType,
             double epsilon, vector<double> k)
      : m_Lattice(LatticeType),
        m_NumCells(NumCells),
        m_AtomType(AtomType),
        m_epsilon(epsilon),
        m_k(k) {
    if (m_Lattice == "fcc")
      m_LatticeParameter = r0 * 2.0 / sqrt(2.0);

    else if (m_Lattice == "sc")
      m_LatticeParameter = r0;
    else
      throw std::runtime_error("Unknown lattice type");
  }
  // BuildStructure: screates the .data file
  void BuildStructure();

  // WritePotential: it writes the Potential.mod lammps file
  void WritePotential();

  // RunMinimize
  void RunMinimize();

  // RunRlastic
  void RunElastic();

  // ReadElasticConstants
  void ReadElasticConstants(double param1, double param2, unsigned int n1,
                            unsigned int n2);

  // ComputeWaveVelocities()
  void ComputeWaveVelocities(unsigned int n1, unsigned int n2);

 private:
  string m_Lattice;
  int m_NumCells;
  int m_AtomType;
  double m_LatticeParameter;
  double m_epsilon;
  double C11, C12, C44;
  vector<double> m_k;
};

class Atom {
 public:
  // Constructor to initialize the atom's position, type, and ID
  Atom(double x, double y, double z, unsigned int type, unsigned int id)
      : x(x), y(y), z(z), type(type), id(id) {}

  // set methods to modify the atom's properties
  void setX(double x) { this->x = x; }
  void setY(double y) { this->y = y; }
  void setZ(double z) { this->z = z; }
  void setType(unsigned int type) { this->type = type; }
  void setId(unsigned int id) { this->id = id; }

  // get methods to access the atom's properties
  double getX() const { return x; }
  double getY() const { return y; }
  double getZ() const { return z; }
  unsigned int getType() const { return type; }
  unsigned int getId() const { return id; }

 private:
  double x, y, z;     // Position of the atom
  unsigned int type;  // Type of the atom
  unsigned int id;    // ID of the atom
};

// struct
struct FCCTag {};
struct SCTag {};

class Triplet {
 public:
  // Constructor FCC
  Triplet(Atom a1, Atom a2, Atom a3, FCCTag);
  // Constructor SC
  Triplet(Atom a1, Atom a2, Atom a3, SCTag);
  // Getters
  Atom getAtom1() const { return atom1; }
  Atom getAtom2() const { return atom2; }
  Atom getAtom3() const { return atom3; }
  double getTheta() const { return theta; }
  unsigned int getType() const { return Type; }
  // Setters
  void SetAtom1(const Atom& a) { atom1 = a; }
  void SetAtom2(const Atom& a) { atom2 = a; }
  void SetAtom3(const Atom& a) { atom3 = a; }

 private:
  Atom atom1, atom2, atom3;
  double theta;       // Angle formed by the three atoms in radiants
  unsigned int Type;  // Type of the triplet
  // ID: to be added if needed
};

class FCCLattice {
 public:
  // Constructor
  FCCLattice(double LatticeParameter, int NumCells, int AtomType)
      : LatticeParameter(LatticeParameter),
        NumCells(NumCells),
        AtomType(AtomType) {
    // Allocate the atomIndex structure
    atomIndex.resize(NumCells);

    for (int i = 0; i < NumCells; ++i) {
      atomIndex[i].resize(NumCells);

      for (int j = 0; j < NumCells; ++j) {
        atomIndex[i][j].resize(NumCells);

        for (int k = 0; k < NumCells; ++k) {
          atomIndex[i][j][k].fill(-1);
        }
      }
    }

    BuildAtoms();
    BuildNeighbourLists();
    BuildTriplets();
  }

  // Getters
  const vector<Atom>& getAtoms() const { return atoms; }
  const vector<Triplet>& getTriplets() const { return triplets; }
  const vector<vector<vector<array<int, 4>>>>& getAtomIndex() const {
    return atomIndex;
  }
  const array<int, 12>& getfirstNeighbours(int index) const {
    return firstNeighbours[index];
  }

  unsigned int getNatoms();
  unsigned int getNangles();

  // Print

  void PrintLAMMPSData(const string& filename) const;

 private:
  // Methods
  void BuildAtoms();
  void BuildNeighbourLists();
  void BuildTriplets();

  // Data
  vector<Atom> atoms;
  vector<Triplet> triplets;
  // atomIndex[i][j][k][basis] = index of the atom in the atoms vector
  vector<vector<vector<array<int, 4>>>> atomIndex;
  // first and second neighbour lists to be implemented
  vector<array<int, 12>> firstNeighbours;
  vector<array<int, 6>> secondNeighbours;
  // periodic structure condition
  Atom ClosestImage(const Atom& atom, const Atom& reference) const;

  double LatticeParameter;
  int NumCells;
  int AtomType;
};

// Teoricamente dovrebbe essere pronto cosi
class SCLattice {
 public:
  // Constructor
  SCLattice(double LatticeParameter, int NumCells, int AtomType)
      : LatticeParameter(LatticeParameter),
        NumCells(NumCells),
        AtomType(AtomType) {
    // Allocate the atomIndex structure
    atomIndex.resize(NumCells);

    for (int i = 0; i < NumCells; ++i) {
      atomIndex[i].resize(NumCells);

      for (int j = 0; j < NumCells; ++j) {
        atomIndex[i][j].resize(NumCells);

        for (int k = 0; k < NumCells; ++k) {
          atomIndex[i][j][k].fill(-1);
        }
      }
    }

    BuildAtoms();
    BuildNeighbourLists();
    BuildTriplets();
  }

  // Getters
  const vector<Atom>& getAtoms() const { return atoms; }
  const vector<Triplet>& getTriplets() const { return triplets; }
  const vector<vector<vector<array<int, 1>>>>& getAtomIndex() const {
    return atomIndex;
  }
  const array<int, 6>& getfirstNeighbours(int index) const {
    return firstNeighbours[index];
  }

  unsigned int getNatoms();
  unsigned int getNangles();

  // Print

  void PrintLAMMPSData(const string& filename) const;

 private:
  // Methods
  void BuildAtoms();
  void BuildNeighbourLists();
  void BuildTriplets();

  // Data
  vector<Atom> atoms;
  vector<Triplet> triplets;
  // atomIndex[i][j][k][basis] = index of the atom in the atoms vector
  vector<vector<vector<array<int, 1>>>> atomIndex;
  // first and second neighbour lists to be implemented
  vector<array<int, 6>> firstNeighbours;
  vector<array<int, 12>> secondNeighbours;
  // periodic structure condition
  Atom ClosestImage(const Atom& atom, const Atom& reference) const;

  double LatticeParameter;
  int NumCells;
  int AtomType;
};

#endif  // CLASS_H
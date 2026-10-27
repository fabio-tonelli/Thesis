#ifndef MULTIQ_2_3_H
#define MULTIQ_2_3_H

#include <array>      // std::array nei prototipi/funzioni
#include <vector>     // std::vector nelle classi e in Flag_Assignment
#include <cstdint>    // uint32_t in RandomGen
#include <cmath>      // log, sqrt, cos, M_PI in RandomGen
#include <armadillo>  // arma::mat, arma::vec, eig_sym, normalise, dot
#include <fstream>
using namespace std;
using namespace arma;



//RandomGen
class RandomGen {
 public:
  RandomGen(uint32_t seed) {
    m_a = 1664525, m_c = 1013904223, m_m = 4294967296.0;
    m_seed = seed;
  };

  double Rand() {
    m_seed = (m_a * m_seed + m_c);
    return (double)m_seed / m_m;
  };
  // distribuzione uniforme tra 0 e 1
  double Unif(double xmin, double xmax) {
    return (xmin + (xmax - xmin) * Rand());
  };  // distribuzione uniforme tra xmin e xmax

  double Exp(double lambda) {
    return -log(1 - Rand()) / lambda;
  };  // distribuzione esponenziale con costante lambda
  double Gaus(double mean, double sigma) {
    double s = Rand();
    double t = Rand();
    double x = sqrt(-2. * log(1. - s)) * cos(2. * M_PI * t);
    return (mean + x * sigma);
  };  // distribuzione gaussiana (Box-Muller)
  

 private:
  uint32_t m_a, m_c;
  uint32_t m_seed;
  double m_m;
};

//Diagonalize
class Diagonalize {
 public:
  Diagonalize(double C11, double C12, double C44)
      : m_C11(C11), m_C12(C12), m_C44(C44) {}

  void Setq(double qx, double qy, double qz) {
    m_qx = qx; m_qy = qy; m_qz = qz;
    double a = m_C11*qx*qx + m_C44*(qy*qy + qz*qz);
    double e = m_C11*qy*qy + m_C44*(qx*qx + qz*qz);
    double i = m_C11*qz*qz + m_C44*(qx*qx + qy*qy);
    double b = (m_C12 + m_C44)*qx*qy;
    double c = (m_C12 + m_C44)*qx*qz;
    double f = (m_C12 + m_C44)*qy*qz;
    m_A = {{a, b, c}, {b, e, f}, {c, f, i}};
  }

  void Compute() {
    m_Eigenvalues.clear();
    m_L_Coefficients.clear();

    vec eigval;
    mat eigvec;
    eig_sym(eigval, eigvec, m_A);

    vec q = {m_qx, m_qy, m_qz};
    q = normalise(q);

    for (int k = 0; k < 3; k++) {
      m_Eigenvalues.push_back(eigval(k));
      m_L_Coefficients.push_back(dot(eigvec.col(k), q));
    }
  }

  vector<double> get_Eig() { return m_Eigenvalues; }
  vector<double> get_L_Coef() { return m_L_Coefficients; }

 private:
  mat m_A = zeros<mat>(3, 3);
  vector<double> m_Eigenvalues, m_L_Coefficients;
  double m_qx = 0, m_qy = 0, m_qz = 0;
  double m_C11, m_C12, m_C44;
};

//Funzione void di modifica delle flag
inline void Flag_Assignment(bool &trovato_L_sotto, bool &trovato_L_mezzo,
                     bool &trovato_L_sopra, int &count, int &count1,
                     int &countdeg, int &countdeg1, Diagonalize D,
                     const vector<array<double, 3>> &dirs) {
  for (const auto& d : dirs) {
    D.Setq(d[0], d[1], d[2]);
    D.Compute();
    vector<double> Eigv = D.get_Eig();
    vector<double> C = D.get_L_Coef();

    double c0 = abs(C[0]), c1 = abs(C[1]), c2 = abs(C[2]);

    if (Eigv[1] - Eigv[0] < 1e-12) countdeg1++;
    if (Eigv[2] - Eigv[0] < 1e-12) {
      countdeg++;
    } else {
      if (c0 >= c1 && c0 >= c2)      { trovato_L_sotto = true; count++; count1++; }
      else if (c1 >= c0 && c1 >= c2) { trovato_L_mezzo = true; count++; }
      else                           { trovato_L_sopra = true; }
    }
  }
}

inline void Flag_Assignment_Sphere(ofstream &outfile, int &count, int &count1,
                     int &countdeg, int &countdeg1, Diagonalize D,
                     const vector<array<double, 3>> &dirs) {
  
     outfile << "#qx qy qz label" << endl;
    
    for (const auto& d : dirs) {
    D.Setq(d[0], d[1], d[2]);
    D.Compute();
    vector<double> Eigv = D.get_Eig();
    vector<double> C = D.get_L_Coef();

    int qlabel=-1;
    double c0 = abs(C[0]), c1 = abs(C[1]), c2 = abs(C[2]);

    if (Eigv[1] - Eigv[0] < 1e-12) countdeg1++;
    if (Eigv[2] - Eigv[0] < 1e-12) {
      countdeg++;
    } else {
      if (c0 >= c1 && c0 >= c2)      { qlabel=0; count++; count1++; }
      else if (c1 >= c0 && c1 >= c2) { qlabel=1; count++; }
      else                           { qlabel=2; }
    }
    outfile << d[0] << " " << d[1] << " " << d[2] << " " << qlabel << endl;
  }
}

//Costruzione di dirs
inline void make_dirs( vector<array<double, 3>> &dirs,long unsigned int N_vectors,uint32_t seed){
  

   RandomGen R(seed);

   // direzioni speciali: determinano i bordi della mappa
  // dirs.push_back({1., 0., 0.});                                  // [100]
  // dirs.push_back({1 / sqrt(2.), 1 / sqrt(2.), 0.});              // [110]
  // dirs.push_back({1 / sqrt(3.), 1 / sqrt(3.), 1 / sqrt(3.)});    // [111]

  while (dirs.size() < N_vectors) {
    vec3 q;
    q(0) = R.Unif(0, 1);
    q(1) = R.Unif(0, 1);
    q(2) = R.Unif(0, 1);

    double q2 = dot(q, q);
    if (q2 < 1 && q2 > 0) {
      q = normalise(q);
      dirs.push_back({q(0), q(1), q(2)});
      
    }
  }
}


//integer assignment
inline void cmp_T_L_Assignment(int &cmp_T_L,bool trovato_L_sotto, bool trovato_L_mezzo,
                     bool trovato_L_sopra){
                    // convenzione:
      // 0: L>T sempre      1: T1<L<T2 sempre   2: L<T sempre
      // 3: sopra+mezzo     4: sopra+sotto      5: mezzo+sotto
      // 6: tutte e tre
      if (trovato_L_sopra && !trovato_L_mezzo && !trovato_L_sotto) cmp_T_L = 0;
      else if (!trovato_L_sopra && trovato_L_mezzo && !trovato_L_sotto) cmp_T_L = 1;
      else if (!trovato_L_sopra && !trovato_L_mezzo && trovato_L_sotto) cmp_T_L = 2;
      else if (trovato_L_sopra && trovato_L_mezzo && !trovato_L_sotto) cmp_T_L = 3;
      else if (trovato_L_sopra && !trovato_L_mezzo && trovato_L_sotto) cmp_T_L = 4;
      else if (!trovato_L_sopra && trovato_L_mezzo && trovato_L_sotto) cmp_T_L = 5;
      else if (trovato_L_sopra && trovato_L_mezzo && trovato_L_sotto) cmp_T_L = 6;
      else cmp_T_L = -1;
                     }


#endif 
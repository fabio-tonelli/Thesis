#include <math.h>

#include <armadillo>
#include <fstream>
#include <iostream>
#include <string>
using namespace arma;

using namespace std;

// soglia di uguaglianza
const double epsilon = 1e-6;
// classe Diagonalize e metodi
class Diagonalize {
 public:
  // Constructor 1
  Diagonalize() {
    // mettere matrice elastica
    // per ora metto l'identità
    m_A = eye<mat>(3, 3);
  }
  // Constructor 2
  Diagonalize(double qx, double qy, double qz, double C11, double C12,
              double C44)
      : m_qx(qx), m_qy(qy), m_qz(qz), m_C11(C11), m_C12(C12), m_C44(C44) {
    m_A = {{m_a, m_b, m_c}, {m_d, m_e, m_f}, {m_g, m_h, m_i}};
  }
  // Compute method
  void Compute() {
    // Calcolo autovalori
    vec eigval;
    mat eigvec;

    eig_sym(eigval, eigvec, m_A);

    // filling m_Eigenvalues
    m_Eigenvalues.push_back(eigval.at(0));
    m_Eigenvalues.push_back(eigval.at(1));
    m_Eigenvalues.push_back(eigval.at(2));

    // Computin L_T_coefficients

    // creating q vector
    vec q(3);

    q(0) = m_qx;
    q(1) = m_qy;
    q(2) = m_qz;

    // Normalizing q  per sicurezza, dovrebbero essere già normalizzati
    q = normalise(q);

    // Extractig vectors
    vec v0 = eigvec.col(0);
    vec v1 = eigvec.col(1);
    vec v2 = eigvec.col(2);

    // Fillling coefficients
    m_L_Coefficients.push_back(dot(v0, q));
    m_L_Coefficients.push_back(dot(v1, q));
    m_L_Coefficients.push_back(dot(v2, q));
  }

  // getters
  vector<double> get_Eig() { return m_Eigenvalues; }
  vector<double> get_L_Coef() { return m_L_Coefficients; }

 private:
  mat m_A;
  vector<double> m_Eigenvalues;
  vector<double> m_L_Coefficients;
  double m_qx, m_qy, m_qz;
  double m_C11, m_C12, m_C44;
  // entrate della matrice
  // prima riga
  double m_a = m_C11 * m_qx * m_qx + m_C44 * (m_qy * m_qy + m_qz * m_qz);
  double m_b = (m_C12 + m_C44) * m_qx * m_qy;
  double m_c = (m_C12 + m_C44) * m_qx * m_qz;
  // seconda riga
  double m_d = (m_C12 + m_C44) * m_qx * m_qy;
  double m_e = m_C11 * m_qy * m_qy + m_C44 * (m_qx * m_qx + m_qz * m_qz);
  double m_f = (m_C12 + m_C44) * m_qy * m_qz;
  // terza riga
  double m_g = (m_C12 + m_C44) * m_qx * m_qz;
  double m_h = (m_C12 + m_C44) * m_qy * m_qz;
  double m_i = m_C11 * m_qz * m_qz + m_C44 * (m_qx * m_qx + m_qy * m_qy);
};

int main() {
  // letture da file elastic
  ifstream elastic("results_all.csv");

  if (!elastic.is_open()) {
    cout << "Could not open elastic\n";
    return 1;
  }

  unsigned int N_columns = 5;
  vector<vector<double>> dati;

  string line;

  // salto intestazione
  getline(elastic, line);

  while (getline(elastic, line)) {
    stringstream ss(line);
    string valore;

    vector<double> riga;

    int colonna = 0;

    while (getline(ss, valore, ',')) {
      // prendiamo solo colonne:
      // 0 K2
      // 1 K4
      // 2 C11
      // 3 C12
      // 4 C44

      if (colonna <= N_columns - 1) {
        riga.push_back(stod(valore));
      }

      colonna++;
    }

    if (riga.size() == N_columns) dati.push_back(riga);
  }

  // file results
  string outfile = "results_Multiq.csv";

  FILE* out = fopen(outfile.c_str(), "w");
  fprintf(out,
          "K2,K4,C11,C12,C44,q_x,q_y,q_z,Rho*v1^2,Rho*v2^2,Rho*v3^2,L_coeff1,L_"
          "coeff2,L_coeff3,cmp_T_L\n");

  // per ogni coppia di valori k2-k4 devo costruire, per ogni terna qx,qy,qz ,
  // la matrice e diagonalizzarla. dopo di che devo trovare gli autovettori ,
  // proiettarli sul vettore q e trovare i coefficienti longitudinale e
  // trasversale. poi devo scrivere tutto in un file e , successivamente,
  // plottarlo

  // per non sovraccaricare il main ha senso costruire una funzione che , dato
  // un vector in ingresso, calcoli autovalori e autovettori. in questo modo
  // nel main si fa solo un for sugli elementi di dati.

  // numero di righe (i.e. valori diversi della coppia k2-k4)
  unsigned int N_dati = dati.size();

  // ============================================================
  // TEST: direzioni cristallografiche speciali (100, 110, 111)
  // ============================================================
  {
    string outfile_special = "results_special_directions.csv";
    FILE* out_special = fopen(outfile_special.c_str(), "w");
    fprintf(
        out_special,
        "K2,K4,C11,C12,C44,direzione,q_x,q_y,q_z,e1,e2,e3,L_coeff1,L_coeff2,"
        "L_coeff3,cmp_T_L\n");

    // direzioni speciali normalizzate: nome + (qx,qy,qz)
    struct Direzione {
      string nome;
      double qx, qy, qz;
    };

    double s2 = 1.0 / sqrt(2.0);  // per 110
    double s3 = 1.0 / sqrt(3.0);  // per 111

    vector<Direzione> direzioni = {
        {"100", 1.0, 0.0, 0.0}, {"110", s2, s2, 0.0}, {"111", s3, s3, s3}};

    for (int i = 0; i < N_dati; i++) {
      double C11 = dati[i][2];
      double C12 = dati[i][3];
      double C44 = dati[i][4];
      double k2 = dati[i][0];
      double k4 = dati[i][1];

      for (auto& d : direzioni) {
        Diagonalize D(d.qx, d.qy, d.qz, C11, C12, C44);
        D.Compute();

        vector<double> E = D.get_Eig();
        vector<double> C = D.get_L_Coef();

        double e1 = E[0];
        double e2 = E[1];
        double e3 = E[2];

        double L_Coeff1 = C[0];
        double L_Coeff2 = C[1];
        double L_Coeff3 = C[2];

        double L_C1 = abs(L_Coeff1);
        double L_C2 = abs(L_Coeff2);
        double L_C3 = abs(L_Coeff3);

        double L_Cmax = max({L_C1, L_C2, L_C3});

        double L_val, T_a, T_b;
        if (L_Cmax == L_C1) {
          L_val = e1;
          T_a = e2;
          T_b = e3;
        } else if (L_Cmax == L_C2) {
          L_val = e2;
          T_a = e1;
          T_b = e3;
        } else {
          L_val = e3;
          T_a = e1;
          T_b = e2;
        }

        char cmp_T_L;
        if (abs(T_a - L_val) < epsilon && abs(T_b - L_val) < epsilon) {
          cmp_T_L = '=';
        } else if (T_a > L_val && T_b > L_val) {
          cmp_T_L = 'y';
        } else if (T_a < L_val && T_b < L_val) {
          cmp_T_L = 'n';
        } else {
          cmp_T_L = 'm';
        }

        fprintf(out_special,
                "%g,%g,%g,%g,%g,%s,%g,%g,%g,%g,%g,%g,%g,%g,%g,%c\n", k2, k4,
                C11, C12, C44, d.nome.c_str(), d.qx, d.qy, d.qz, e1, e2, e3,
                L_Coeff1, L_Coeff2, L_Coeff3, cmp_T_L);
      }
    }

    fclose(out_special);
    cout << "Scritto: " << outfile_special << "\n";
  }

  // valori di qx.qy,qz metto la norma di q uguale a 1
  double delta_theta = 0.1;
  double delta_phi = 0.1;

  for (double theta = 0; theta <= M_PI / 2; theta += delta_theta) {
    for (double phi = 0; phi <= M_PI / 2; phi += delta_phi) {
      double qx = sin(theta) * cos(phi);
      double qy = sin(theta) * sin(phi);
      double qz = cos(theta);
      // ciclo sulle righe (k2-k4)
      for (int i = 0; i < N_dati; i++) {
        // ciclo sui valori di q
        // elastic constants
        double C11 = dati[i][2];
        double C12 = dati[i][3];
        double C44 = dati[i][4];
        // k2 and k4
        double k2 = dati[i][0];
        double k4 = dati[i][1];
        Diagonalize D(qx, qy, qz, C11, C12, C44);
        D.Compute();

        vector<double> E = D.get_Eig();
        vector<double> C = D.get_L_Coef();

        // Eig
        double e1 = E[0];
        double e2 = E[1];
        double e3 = E[2];

        // LCoeff
        double L_Coeff1 = C[0];
        double L_Coeff2 = C[1];
        double L_Coeff3 = C[2];
        // absCoeff
        double L_C1 = abs(L_Coeff1);
        double L_C2 = abs(L_Coeff2);
        double L_C3 = abs(L_Coeff3);

        // T and L velocity variable
        char cmp_T_L;  // T>L yes, T<L no, T=L =

        //  determination of L_T relation (to be improved)
        // determina quale autovalore corrisponde al modo L (proiezione massima)
        double L_Cmax = max({L_C1, L_C2, L_C3});

        double L_val, T_a, T_b;
        if (L_Cmax == L_C1) {
          L_val = e1;
          T_a = e2;
          T_b = e3;
        } else if (L_Cmax == L_C2) {
          L_val = e2;
          T_a = e1;
          T_b = e3;
        } else {
          L_val = e3;
          T_a = e1;
          T_b = e2;
        }

        if (abs(T_a - L_val) < epsilon && abs(T_b - L_val) < epsilon) {
          cmp_T_L = '=';  // tutti e tre uguali
        } else if (T_a > L_val && T_b > L_val) {
          cmp_T_L = 'y';  // entrambi i T > L
        } else if (T_a < L_val && T_b < L_val) {
          cmp_T_L = 'n';  // entrambi i T < L
        } else {
          cmp_T_L = 'm';  // misto: un T sopra, un T sotto L
        }
        // stampa su file
        if (!isfinite(C11) || !isfinite(C12) || !isfinite(C44) ||
            !isfinite(e1) || !isfinite(e2) || !isfinite(e3) ||
            !isfinite(L_Coeff1) || !isfinite(L_Coeff2) || !isfinite(L_Coeff3)) {
          fprintf(stderr,
                  "K2=%g K4=%g -> mancante: C11=%s C12=%s C44=%s e1=%s e2=%s "
                  "e3=%s L_Coeff1=%s L_Coeff2=%s L_Coeff3=%s cmp_T_L=%c  \n",
                  k2, k4, C11 ? "ok" : "NULL", C12 ? "ok" : "NULL",
                  C44 ? "ok" : "NULL", e1 ? "ok" : "NULL", e2 ? "ok" : "NULL",
                  e3 ? "ok" : "NULL", L_Coeff1 ? "ok" : "NULL",
                  L_Coeff2 ? "ok" : "NULL", L_Coeff3 ? "ok" : "NULL", cmp_T_L);
        } else {
          fprintf(out, "%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%c\n", k2, k4,
                  C11, C12, C44, qx, qy, qz, e1, e2, e3, L_Coeff1, L_Coeff2,
                  L_Coeff3, cmp_T_L);
        }

        // cout << "Eigenvalues: " << E[0] << " " << E[1] << " " << E[2] <<
        // endl; cout << "Coefficients: " << C[0] << " " << C[1] << " " <<
        // C[2]
        // << endl;
      }
    }
  }
  /*
    // esempio controllo
    for (auto& riga : dati) {
      cout << riga[0] << " " << riga[1] << " " << riga[2] << " " << riga[3]
    << "
    "
           << riga[4] << "\n";
    }
  */
  /*// Declaring Matrix (Armadillo)

      // N colonne
      double N_col = 3;
      double N_rows = 3;

      mat M = eye<mat>(3, 3);

      /*
      // filling M
      M.col(0) = vec("1.0 0.0 0.0");
      M.col(0) = vec("0.0 1.0 0.0");
      M.col(0) = vec("0.0 0.0 1.0");

      // Calcolo autovalori e autovettori
      vec eigval;
      mat eigvec;

      eig_sym(eigval, eigvec,
              M);  // it stores eigenvalues in eigval and
                   // eigenvectors in eigvec only right eigenvectors
                   // eigenvectors are stored ad column vectors
                   // balance: diagonally scale and permute X to improve
                   // conditioning of the eigenvalues

      // eigenvalues
      complex<double> e0 = eigval.at(0);
      complex<double> e1 = eigval.at(1);
      complex<double> e2 = eigval.at(2);

      // eigenvectors
      vec v0 = eigvec.col(0);
      vec v1 = eigvec.col(1);
      vec v2 = eigvec.col(2);
      */
  return 0;
}

// funzione ch eprende un vector<double> , range(qx),range(qy), range(qz) e
// Delta_q in entrata , calcola autovalori e autovettori della matrice per
// quei q, poi fa il prodotto scalare con il vettore q, normalizza, e trova i
// coefficienti di proiezione. questa funzione ritornerà un vector<double>
// formato da: (e1 , e2, e3 , coeff_T , coeff_L). q deve essere normalizzato,
// quindi coeff_T e coeff_L<=1. forse è meglio avere una classe

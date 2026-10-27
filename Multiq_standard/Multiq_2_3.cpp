
#include <iostream>   // cout, endl
#include <fstream>    // ofstream
#include <iomanip>    // setprecision
#include <string>     // std::string


#include "Multiq_2_3.h"

using namespace std;

using namespace arma;

int main(int argc , char* argv[]) {

  //controllo numero argomenti
  if (argc != 2) {
  cout << "Inserire un argomento: SC o FCC" << endl;
  return -1;
}
string lattice = argv[1];
//file per diagram classico
string filename;
//file per diagram sferico
string filename_sphere;
if (lattice == "SC"){
       filename = "results_SC.csv";
       
}
else if (lattice == "FCC"){
 filename = "results_FCC.csv";
 
}
else {
  cout << "Scegliere o FCC o SC" << endl;
  return -2;
}

 // cancella il vecchio file results.csv (se non esiste, non è un errore grave)
  if (remove(filename.c_str()) == -1) {
    perror("Errore durante la rimozione del file");
  }

ofstream outfile(filename);
if (!outfile.is_open()) {
  cout << "Errore apertura file" << endl;
  return 1;


}
if (lattice == "SC")
  outfile << "#gamma1 gamma3 cmp_T_L frac frac1 fracdeg fracdeg1" << endl;
else{
  outfile << "#gamma2 gamma3 cmp_T_L frac frac1 fracdeg fracdeg1" << endl;
}
 

  // ---------------- Random generator ----------------
  uint32_t seed = 12345;
 

  // numero di direzioni casuali (oltre alle 3 speciali)
  long unsigned int N_vectors = 5000;

  // ---------------- Parametri fisici ----------------
  double epsilon = 1 / 72.;
  double gamma1=0 , gamma2 = 0, gamma3 = 0, gamma4 = 0, gamma5 = 0, gammax = 0;
  double r0 = 1.;
  double r03 = pow(r0, 3);

  double gamma_step = 0.005;
  double gamma_max = 2;
  int i_gamma_max = (int)round(gamma_max / gamma_step);
  int j_gamma_max = i_gamma_max;

  

  // ---------------- Direzioni: generate UNA sola volta ----------------
  vector<array<double, 3>> dirs;
 

  // direzioni casuali nell'ottante positivo (rejection sulla palla)
  make_dirs(dirs,N_vectors,seed);
  



  // ---------------- Scansione (gamma2, gamma3) ----------------
  int cmp_T_L;

  

  for (int i = 0; i <= i_gamma_max; i++) {
    gammax = i * gamma_step;

    for (int j = 0; j <= j_gamma_max; j++) {
      gamma3 = j * gamma_step;

      //Commento
      // costanti elastiche

      double S=0;
      double C11=0;
      double C12=0;
      double C44=0;
      if(lattice == "SC"){
      gamma1=gammax;
      gamma5=gammax;
       S = gamma1 + gamma2 + 2. * gamma3 + gamma4 + gamma5;
       C11 = (1. / r03) * (72. * epsilon + 4. * S);
       C12 = -(2. / r03) * S;
       C44 = (2. / r03) *
                   (gamma1 + 2. * gamma2 + 6. * gamma3 + 2. * gamma4 + gamma5);
  }
  if(lattice == "FCC"){
      gamma2=gammax;
      gamma4=gammax;
       S = gamma2 + 2. * gamma3 + gamma4;
       C11 = sqrt(2.) / r03 * (72. * epsilon + 4. * S);
       C12 = sqrt(2.) / r03 * (36. * epsilon - 2. * S);
       C44 = 4. * sqrt(2.) / r03 * (9. * epsilon + gamma2 + gamma4);
  }

      
      // flag di classificazione
      bool trovato_L_sopra = false;  // L ha l'autovalore più alto (L > T)
      bool trovato_L_mezzo = false;  // T1 < L < T2
      bool trovato_L_sotto = false;  // L ha l'autovalore più basso (L < T)

      //contatori
      int count =0;
      int count1 =0;
      int countdeg=0;
      int countdeg1=0;

      Diagonalize D(C11,C12,C44);
      //assegno le flag
      Flag_Assignment(trovato_L_sotto,trovato_L_mezzo,trovato_L_sopra,count,count1,countdeg,countdeg1,D,dirs);
      //in base alle flag stabilisco l'intero
      cmp_T_L_Assignment(cmp_T_L , trovato_L_sotto,trovato_L_mezzo,trovato_L_sopra);

      double frac = float(count)/N_vectors;
      double frac1 = float(count1)/N_vectors;
      double fracdeg = float(countdeg)/N_vectors;
      double fracdeg1 = float(countdeg1)/N_vectors;
      
      

      outfile << gammax << " " << gamma3 << " " << cmp_T_L << " " << setprecision(12)<<frac <<" "<<frac1 << " " << fracdeg << " " << fracdeg1 <<endl;


    }
}



  return 0;
}
 

 

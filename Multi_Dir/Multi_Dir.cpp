
#include <iostream>   
#include <fstream>    
#include <iomanip>    
#include <string>    


#include "Multi_Dir.h"

using namespace std;

using namespace arma;

int main(int argc , char* argv[]) {

  //checking the number of the arguments
  if (argc != 2) {
  cout << "Argument required: SC or FCC" << endl;
  return -1;
}
string lattice = argv[1];

string filename;

//string filename assignment
if (lattice == "SC" || lattice == "FCC"){
       filename = "2D_Results_"+ lattice +".txt";
       
}
else {
  cout << "The argument has to be SC or FCC" << endl;
  return -2;
}

string filepath = "/home/tonelli/Tesi/Multi_Dir/Results/2D_Results/";
 //removes the old file filename
  if (remove((filepath + filename).c_str()) == -1) {
    perror("Could not remove the results file for the selected lattice");

  }

ofstream outfile("/home/tonelli/Tesi/Multi_Dir/Results/2D_Results/" + filename);
if (!outfile.is_open()) {
  cout << "Could not open output file" << endl;
  return 1;


}
if (lattice == "SC")
  outfile << "#gamma1 gamma3 cmp_T_L frac frac1 fracdeg fracdeg1" << endl;
else{
  outfile << "#gamma2 gamma3 cmp_T_L frac frac1 fracdeg fracdeg1" << endl;
}
 

  // ---------------- Random generator ----------------
  uint32_t seed = 12345;
 

  // Number of random uniform directions
  long unsigned int N_vectors = 5000;

  // ---------------- Physical parameters ----------------
  double epsilon = 1 / 72.;
  double gamma1=0 , gamma2 = 0, gamma3 = 0, gamma4 = 0, gamma5 = 0, gammax = 0;
  double r0 = 1.;
  double r03 = pow(r0, 3);

  double gamma_step = 0.005;
  double gamma_max = 2;
  int i_gamma_max = (int)round(gamma_max / gamma_step);
  int j_gamma_max = i_gamma_max;

  

  // ---------------- Directions array (generated once) ----------------
  vector<array<double, 3>> dirs;
 

 

  //definition of the special_directions bool
  bool special_directions = false;
  make_dirs(dirs,N_vectors,seed,special_directions);
  



  // ---------------- Scanning (gamma2, gamma3) ----------------
  
  //invarsion integer lable for each gamma point
  int cmp_T_L;

  
 //cicle on gamma2,gamma3
  for (int i = 0; i <= i_gamma_max; i++) {
    gammax = i * gamma_step;

    for (int j = 0; j <= j_gamma_max; j++) {
      gamma3 = j * gamma_step;

      
      // Elastic constants
      double S=0;
      double C11=0;
      double C12=0;
      double C44=0;

      //Derived expressions
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

      
      // Bool classification flags
      bool trovato_L_sopra = false;  // L has the higher eigenvalue (L > T)
      bool trovato_L_mezzo = false;  // T1 < L < T2
      bool trovato_L_sotto = false;  // L has the lower eigenvalue (L < T)

      //counters
      int count =0;
      int count1 =0;
      int countdeg=0;
      int countdeg1=0;

      //creating an object of the Diagonalize class
      Diagonalize D(C11,C12,C44);
      //Flag assignment
      Flag_Assignment(trovato_L_sotto,trovato_L_mezzo,trovato_L_sopra,count,count1,countdeg,countdeg1,D,dirs);
      //Based on the flags, comes the integer lable xmp_T_L
      cmp_T_L_Assignment(cmp_T_L , trovato_L_sotto,trovato_L_mezzo,trovato_L_sopra);

      //frac variables 
      double frac = float(count)/N_vectors;
      double frac1 = float(count1)/N_vectors;
      double fracdeg = float(countdeg)/N_vectors;
      double fracdeg1 = float(countdeg1)/N_vectors;
      
      
      //writing the results in the output file
      outfile << gammax << " " << gamma3 << " " << cmp_T_L << " " << setprecision(12)<<frac <<" "<<frac1 << " " << fracdeg << " " << fracdeg1 <<endl;


    }
}



  return 0;
}
 

 

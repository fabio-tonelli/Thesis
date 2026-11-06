#include <iostream>   
#include <fstream>    
#include <iomanip>   
#include <string>    
#include <filesystem>

#include "Multiq_2_3.h"

using namespace std;

using namespace arma;



void delete_dir_content(const filesystem::path& dir_path) {
    for (auto& path: filesystem::directory_iterator(dir_path)) {
        filesystem::remove_all(path);
    }
}

int main(int argc , char* argv[]) {

    //controllo numero argomenti
  if (argc != 2) {
  cout << "Argument required: SC or FCC" << endl;
  return -1;
}
string lattice = argv[1];

//file per diagram sferico
string filename;
if (lattice == "SC"){
       filename = "results_SC_sphere.txt";
       
}
else if (lattice == "FCC"){
 filename = "results_FCC_sphere.txt";
 
}
else {
  cout << "Scegliere o FCC o SC" << endl;
  return -2;
}

// removes the old files
filesystem::path P ="/home/tonelli/Tesi/Multiq_standard/Results/Sphere_Results/Sphere_Results_"+ lattice;
//delete function
delete_dir_content(P);
 



int N_gamma3 = 9;
ofstream outfile[N_gamma3];

for (int i = 0; i < N_gamma3; i++) {
  
    string nome_i = to_string(i) + "_" + filename;   // 0_results_SC_sphere.txt, ...
    outfile[i].open("/home/tonelli/Tesi/Multiq_standard/Results/Sphere_Results/Sphere_Results_"+ lattice + "/" + nome_i);
    if (!outfile[i].is_open()) {
        cout << "Could not open file: " << nome_i << endl;
        return 1;
    }
}

 // ---------------- Parametri fisici ----------------
  double epsilon = 1 / 72.;
  double gamma1=0 , gamma2 = 0, gamma4 = 0, gamma5 = 0;
  double r0 = 1.;
  double r03 = pow(r0, 3);

  
  double gamma3_val[]{1 , 1.5 , 2 , 2.5 , 3,3.5,4,4.5,5};
  
  double gammax = 1;

  double S=0;
      double C11=0;
      double C12=0;
      double C44=0;
  // ---------------- Random generator ----------------
  uint32_t seed = 12345;
 

  // numero di direzioni casuali (oltre alle 3 speciali)
  long unsigned int N_vectors = 5000;

  
      

  // ---------------- Direzioni: generate UNA sola volta ----------------
  vector<array<double, 3>> dirs;
 

  // direzioni casuali nell'ottante positivo (rejection sulla palla)
  //definition of the special_directions bool
  bool special_directions = false;
  make_dirs(dirs,N_vectors,seed,special_directions);

//ciclo sui valori di gamma3
for(int i=0 ; i<N_gamma3 ; i++){

  //contatori
      int count =0;
      int count1 =0;
      int countdeg=0;
      int countdeg1=0;

  //valori delle C
 
if(lattice == "SC"){
      gamma1=gammax;
      gamma5=gammax;
       S = gamma1 + gamma2 + 2. * gamma3_val[i] + gamma4 + gamma5;
       C11 = (1. / r03) * (72. * epsilon + 4. * S);
       C12 = -(2. / r03) * S;
       C44 = (2. / r03) *
                   (gamma1 + 2. * gamma2 + 6. * gamma3_val[i] + 2. * gamma4 + gamma5);
  }
  if(lattice == "FCC"){
      gamma2=gammax;
      gamma4=gammax;
       S = gamma2 + 2. * gamma3_val[i] + gamma4;
       C11 = sqrt(2.) / r03 * (72. * epsilon + 4. * S);
       C12 = sqrt(2.) / r03 * (36. * epsilon - 2. * S);
       C44 = 4. * sqrt(2.) / r03 * (9. * epsilon + gamma2 + gamma4);
  }

   Diagonalize D(C11,C12,C44);
      
   Flag_Assignment_Sphere(outfile[i], count, count1,
                      countdeg,  countdeg1, D,dirs); 

   }
    
  return 0;
}



 

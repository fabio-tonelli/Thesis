#include <lammps/library.h>

#include <cstdio>
#include <cstdlib>
#include <string>

using namespace std;
int main(int argc, char** argv) {
  int i2_start = 0, i2_end = 6;
  std::string outfile = "results.csv";

  if (argc >= 3) {
    i2_start = std::atoi(argv[1]);
    i2_end = std::atoi(argv[2]);
  }
  if (argc >= 4) {
    outfile = argv[3];
  }

#ifdef DEBUG_LOG
  const char* args[] = {"lammps", "-screen", "none"};
#else
  const char* args[] = {"lammps", "-screen", "none", "-log", "none"};
#endif
  int nargs = sizeof(args) / sizeof(args[0]);
  void* lmp = lammps_open_no_mpi(nargs, (char**)args, nullptr);

  lammps_command(lmp, "variable K2 equal 0.0");
  lammps_command(lmp, "variable K3 equal 0.0");
  lammps_command(lmp, "variable K4 equal 0.0");
  lammps_command(lmp, "variable K6 equal 0.0");

  const int N = 6;
  const double step = 0.01;

  FILE* out = fopen(outfile.c_str(), "w");
  fprintf(out, "K2,K3,C11,C12,C44,L100,T100,L110,T110_1,T110_2,L111,T111\n");

  for (int i2 = i2_start; i2 < i2_end; i2++) {
    double k2 = i2 * step;
    for (int i3 = 0; i3 < N; i3++) {
      double k3 = i3 * step;

      char cmd[256];
      snprintf(cmd, sizeof(cmd), "variable K2 equal %g", k2);
      lammps_command(lmp, cmd);
      snprintf(cmd, sizeof(cmd), "variable K3 equal %g", k3);
      lammps_command(lmp, cmd);

      lammps_command(lmp, "clear");
      lammps_file(lmp, "in.elastic");

      double* c11 = (double*)lammps_extract_variable(lmp, "C11all", nullptr);
      double* c12 = (double*)lammps_extract_variable(lmp, "C12all", nullptr);
      double* c44 = (double*)lammps_extract_variable(lmp, "C44all", nullptr);

      if (lammps_has_error(lmp)) {
        char errmsg[512];
        lammps_get_last_error_message(lmp, errmsg, sizeof(errmsg));
        fprintf(stderr, "K2=%g K3=%g -> ERRORE LAMMPS: %s\n", k2, k3, errmsg);
      } else {
        double* c11 = (double*)lammps_extract_variable(lmp, "C11all", nullptr);
        // ... resto come prima ...
      }
      // Dereference
      double C11 = *c11;
      double C12 = *c12;
      double C44 = *c44;

      // 100
      double L100 = C11;
      double T100 = C44;
      // 110
      double L110 = (C11 + C12 + C44) / 2.;
      double T110_1 = C44;
      double T110_2 = (C11 - C12) / 2.;
      // 111
      double L111 = (C11 + 2 * C12 + 4 * C44) / 3.;
      double T111 = (C11 - C12 + C44) / 3.;

      if (!c11 || !c12 || !c44) {
        fprintf(stderr, "K2=%g K3=%g -> mancante: C11=%s C12=%s C44=%s\n", k2,
                k3, c11 ? "ok" : "NULL", c12 ? "ok" : "NULL",
                c44 ? "ok" : "NULL");
      } else {
        fprintf(out, "%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g\n", k2, k3, C11, C12,
                C44, L100, T100, L110, T110_1, T110_2, L111, T111);
      }
      if (c11) lammps_free(c11);
      if (c12) lammps_free(c12);
      if (c44) lammps_free(c44);
    }
  }

  fclose(out);
  lammps_close(lmp);
  return 0;
}
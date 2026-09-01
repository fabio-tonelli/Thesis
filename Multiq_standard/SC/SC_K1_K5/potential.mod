# NOTE: This script can be modified for different pair styles 
# See in.elastic for more info.


# Choose potential
#lj variables

variable Rc equal ${ro}*1.05

variable epsilon equal ${ro}^2 * ${klj} / 72

variable sigma equal ${ro}/(2^(1/6))




#pair style
pair_style	lj/cut ${Rc}
pair_coeff * * ${epsilon} ${sigma}  #atom type 1 atom type 2 epsilon sigma 

#angle style
angle_style cosine/delta 
angle_coeff 1 ${K1} 45
angle_coeff 2 ${K2} 60
angle_coeff 3 ${K3} 90
angle_coeff 4 ${K4} 120
angle_coeff 5 ${K5} 135
angle_coeff 6 ${K6} 180

# Setup neighbor style
#default settings recommended by LAMMPS
neighbor 2.0 nsq
neigh_modify once no every 1 delay 0 check yes page 100000 one 2000

# Setup minimization algoritm when a minimization is done
min_style	     cg
min_modify	     dmax ${dmax} line quadratic norm two

# Setup output
thermo		1
thermo_style custom step temp pe press pxx pyy pzz pxy pxz pyz lx ly lz vol
thermo_modify norm no

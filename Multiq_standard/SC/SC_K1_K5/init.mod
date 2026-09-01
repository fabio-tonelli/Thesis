# NOTE: This script can be modified for different atomic structures, 
# units, etc. See in.elastic for more info.

variable up equal 1.0e-6
variable atomjiggle equal 1.0e-5

units		metal
variable cfac equal 6.2414e-7
variable cunits string eV/A^3

variable etol equal 0.0 
variable ftol equal 1.0e-10
variable maxiter equal 100
variable maxeval equal 1000
variable dmax equal 1.0e-1

#variables
variable ro equal 1.0
variable klj equal 1.0
variable a equal ${ro} 

atom_style hybrid atomic angle

boundary	p p p


#read data
read_data	structure_sc.data

change_box all triclinic

#mass
 mass 1 1.0e-20
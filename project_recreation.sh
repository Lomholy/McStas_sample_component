# This script runs every mcrun needed for the validification of 
# The single scattering components in McStas
rm -r ./data/*

mcrun ./Incoherent/inc.instr sample=0 -n 1e7 -c -d ./data/inc_box_thin

mcrun ./Incoherent/inc.instr sample=0 thickness=0.1 -n 1e7\
 -d ./data/inc_box_thick 


mcplot ./data/inc_box_thick

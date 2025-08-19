# This script runs every mcrun needed for the validification of 
# The single scattering components in McStas


# First move into this folder
cd $HOME/Desktop/Phd/Projects/single_scattering/recreation

rm -r ../data/*

#Scan flux
if test "$1" = "flux"; then
    cd ../Incoherent
    mcrun -c ./inc.instr flux_mult=0.55,0.56 sample=0 thick=0\
    -N 20 -n 1e4 -d ../data/inc_flux
    mcplot ../data/inc_flux
fi

# Incoherent scattering one shot
if test "$1" = "thin"; then
    cd ../Incoherent
    mcrun ./inc.instr sample="thin" -n 1e6 -c -d ../data/inc_box_thin\
     total_scattering=0 
    mcplot ../data/inc_box_thin
fi

# Backscattering
if test "$1" = "thick"; then
    cd ../Incoherent
    mcrun -c ./inc.instr sample="thick" thick=0.001,0.05 -N 50 -n 1e5\
    -d ../data/inc_box_thick 
    mcplot ../data/inc_box_thick
fi


# Small angle scattering instrument
if test "$1" = "sans"; then
    cd ../Sans
    mcrun --mpi=16 -c ../Sans/sans.instr E_i=5 -n 1e7\
    -d ../data/sans 
    mcplot ../data/sans
fi

# Powder diffractometer
if test "$1" = "powder"; then
    cd ../Powder
    mcrun -c ../Powder/DMC.instr flux_mult=3.44 -n 1e7\
    -d ../data/powder_nacalf
    # mcplot ../data/powder

    # Powder diffractometer copper
    mcrun -c ../Powder/DMC.instr flux_mult=3.44 -n 1e7  \
    -d ../data/powder_cop filename="Copper.cif"
    # mcplot ../data/powder
fi

cd ../recreation
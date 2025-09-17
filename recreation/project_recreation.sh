# This script runs every mcrun needed for the validification of 
# The single scattering components in McStas


# First move into this folder
cd $HOME/Desktop/Phd/Projects/single_scattering/recreation
if ! [ $# -eq 2 ]; then
    rm -r ../data/*
fi

#Scan flux
if test "$1" = "flux"; then
    cd ../Incoherent
    rm -r ../data/inc_flux
    mcrun -c ./inc.instr flux_mult=0.55,0.56 sample=0 thick=0.001\
    -N 20 -n 1e4 -d ../data/inc_flux
    # mcplot ../data/inc_flux
fi

# Incoherent scattering one shot
if test "$1" = "thin"; then
    cd ../Incoherent
    rm -r ../data/inc_box_thin
    mcrun ./inc.instr sample="thin" -n 1e6 -c -d ../data/inc_box_thin\
     total_scattering=1 
    # mcplot ../data/inc_box_thin
fi

# Backscattering
if test "$1" = "thick"; then
    cd ../Incoherent
    rm -r ../data/inc_box_thick
    mcrun -c ./inc.instr sample="thick" thick=0.001,0.05 -N 50 -n 1e5\
    -d ../data/inc_box_thick 
    # mcplot ../data/inc_box_thick
fi


# Small angle scattering instrument
if test "$1" = "sans"; then
    cd ../Sans
    rm -r ../data/sans
    mcrun --mpi=15 -c ../Sans/sans.instr E_i=5 -n 1e9\
    -d ../data/sans 
    # mcplot ../data/sans
fi

# Powder diffractometer
if test "$1" = "powder"; then
    cd ../Powder
    mcrun --mpi=15 -c ../Powder/DMC.instr flux_mult=3.44 -n 1e8\
    -d ../data/powder_nacalf_no_debye filename="NaCaAlF_no_debye.cif"

    mcrun --mpi=15 -c ../Powder/DMC.instr flux_mult=3.44 -n 1e8\
    -d ../data/powder_nacalf
    # mcplot ../data/powder

    # Powder diffractometer copper
    mcrun -c ../Powder/DMC.instr flux_mult=3.44 -n 1e7  \
    -d ../data/powder_cop filename="Copper.cif"
    # mcplot ../data/powder
fi

# Single Crystal
if test "$1" = "single"; then
    cd ../Single_crystal
    # Copper
    mcrun --mpi=15 -c ./DMC.instr flux_mult=6.44 -n 1e7\
    -d ../data/single_crystal_cop mos=20 filename="Copper.cif" dlam=0.1 lam0=1.82 beam_size=0.01\
     delta_bragg=2

    # YBCO
    mcrun --mpi=15 -c ./DMC.instr flux_mult=1e-2 -n 1e6\
    -d ../data/single_crystal_ybco mos=20 dlam=0.2

    # NCrystal
    mcrun --mpi=15 -c ./DMC.instr flux_mult=1e-2 -n 1e8\
    -d ../data/ncrystal_ybco mos=20 sample=1

    # High wavelength scan for pretty plot
    mcrun --mpi=15 -c ./DMC.instr flux_mult=3.44 -n 1e7\
    -d ../data/single_crystal_high_wave lam0=2 dlam=1.6 mos=50    
    # mcplot ../data/single_crystal
    
    # Scan over delta bragg
    # mcrun --scan_split=0 -c ./DMC.instr flux_mult=1e-2 -n 1e6\
    #  -d ../data/single_crystal_scan mos=20 delta_bragg=-0.025,0.025 -N 21 dlam=1e-3 lam0=1.940
fi


# Reflectivity 
if test "$1" = "refl"; then
    cd ../Reflecting
    mcrun --scan_split=0 -c ../Reflecting/Refl.instr -n 1e5\
    -d ../data/refl sample_rotation=0,1 -N 80 
    # mcplot ../data/refl
fi

# Run all for recreating them
if test "$1" = "all"; then
    #Scan flux
    source ./project_recreation.sh flux dontdelete
    

    # Incoherent scattering one shot
    source ./project_recreation.sh thin dontdelete

    # Backscattering
    source ./project_recreation.sh thick dontdelete


    # Small angle scattering instrument
    source ./project_recreation.sh sans dontdelete


    # Powder diffractometer
    source ./project_recreation.sh powder dontdelete

    # Single crystal simulation
    source ./project_recreation.sh single dontdelete


    # Reflectivity simulation
    source ./project_recreation.sh refl dontdelete
fi

cd ../recreation
# This script runs every mcrun needed for the validification of 
# The single scattering components in McStas


# First move into this folder
cd $HOME/Phd/Projects/McStas_dev/single_scattering/recreation

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
    rm -r ../data/sans_andreas
    mcrun --mpi=15 -c ../Sans/sans.instr -n 1e9 use_andreas=0\
    improved_res=0 -d ../data/sans 
    mcrun --mpi=15 -c ../Sans/sans.instr -n 1e9 use_andreas=1\
    improved_res=0 -d ../data/sans_andreas
    # mcplot ../data/sans
fi

# Powder diffractometer
if test "$1" = "powder"; then
    cd ../Powder
    rm -r ../data/powder_cop
    rm -r ../data/powder_nacalf
    rm -r ../data/powder_nacalf_no_debye
    mcrun --mpi=15 -c ../Powder/DMC.instr flux_mult=3.44 -n 1e8\
    -d ../data/powder_nacalf

    mcrun --mpi=15 -c ../Powder/DMC.instr flux_mult=3.44 -n 1e8\
    -d ../data/powder_nacalf_no_debye filename="NaCaAlF_no_debye.cif"


    # mcplot ../data/powder

    # Powder diffractometer copper
    mcrun -c ../Powder/DMC.instr flux_mult=3.44 -n 1e7  \
    -d ../data/powder_cop filename="Copper.cif"
    # mcplot ../data/powder
fi

# Single Crystal
if test "$1" = "single"; then
    cd ../Single_crystal
    rm -r ../data/single_crystal_cop
    rm -r ../data/single_crystal_ybco
    rm -r ../data/ncrystal_ybco
    rm -r ../data/single_crystal_high_wave

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
    source ./project_recreation.sh flux 

    # Incoherent scattering one shot
    source ./project_recreation.sh thin 

    # Backscattering
    source ./project_recreation.sh thick 


    # Small angle scattering instrument
    source ./project_recreation.sh sans 


    # Powder diffractometer
    source ./project_recreation.sh powder

    # Single crystal simulation
    source ./project_recreation.sh single 


    # Reflectivity simulation
    source ./project_recreation.sh refl 
fi

cd ../recreation

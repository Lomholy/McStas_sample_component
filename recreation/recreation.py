# Author: Daniel Lomholt Christensen
# This script aims at recreating all the plots for the mcstas sample review
import os
import numpy as np
import matplotlib.pyplot as plt
import mcstasscript as ms
plt.style.use('./Diablo.mplstyle')


################################################################################
########## INCOHERENT SCATTERING
################################################################################

def n_measured_thin(flux, area, dist, rho, solid, cross, mu):
    return flux*area*rho*cross*dist*solid/4/np.pi*mu
############### Thin sample

# Load in the intensity of the thin sample
thin_mcstas = ms.load_data("../data/inc_box_thin")
thin_mcstas = thin_mcstas[2].metadata.total_I

# Calculated total scattered intensity, uncorrected for absorption
flux = 1e7 # incoming flux 25 mm from sample n/s/cm^2
area = 1 # square cm
dist = 0.1 # Distance travelled by the neutron inside sample in cm
rho= 0.0723#1/13.827 # Unit cell density. AA^-3 (10^-24 cm)
cross=5.08 # Cross section in barns (10^-24 cm)
mu = 1 # Attenuation factor
solid_total = 4*np.pi# Solid angle in radians. A/r^2
n_tot = n_measured_thin(flux, area, dist, rho, solid_total, cross, mu)
solid_angle = 10/100**2# Solid angle in radians. A/r^2
n_solid =n_measured_thin(flux, area, dist, rho, solid_angle, cross, mu)
print(f"No absorption incoherent: \nTotal scattering= {n_tot:.4g}n/s\tScattering at detector={n_solid:.4g}n/s")

#Next calculate the attenuation factor
wavelength = 1/np.sqrt(25.3)/0.11056
mu = (5.08 + 5.08*wavelength/1.7982)*rho # Attenuation factor in cm^-1
print(f"Attenuation mu = {mu:.4g}")
mu = np.exp(-mu*(dist + 0.003)) # Attenuation factor
print(f"att factor ={mu:.4g}")

n_tot = n_measured_thin(flux, area, dist, rho, solid_total, cross, mu)

solid = 10/100**2# Solid angle in radians. A/r^2
n_solid =n_measured_thin(flux, area, dist, rho, solid_angle, cross, mu)
print(f"Thin: Total scattering= {n_tot:.4g}n/s\tScattering at detector={n_solid:.4g}n/s")
print(f"Simulation result at detector = {thin_mcstas:.2f}")


############### Thick sample
# # Now simulate for many thicknesses what their scattering is

def n_measured_thick(flux, area, dist, rho, solid, cross, mu):
    solid = 10/(100+(1-np.exp(-2*mu*dist))/2/mu)**2
    result = flux*area*rho*cross*solid/4/np.pi *(1-np.exp(-2*mu*dist))/2/mu
    return result
# Adjust for using a different wavelength
wavelength = 1/np.sqrt(10)/0.11056
mu = (5.08 + 5.08*wavelength/1.7982)*rho # Attenuation factor in cm^-1

n_solid =n_measured_thick(flux, area, dist, rho, solid_angle, cross, mu)
print(f"Total scattering= {n_tot:.4g}n/s\tScattering at detector={n_solid:.4g}n/s")

# If there is data, load it in
# path = "../data/inc_box_thick/"
# if os.path.exists(path):
#     data_X = []
#     data_I = []
#     data_E = []
#     for file in os.listdir(path):
#         if "." in file:
#             continue
#         sim = ms.load_data(path+file)
#         data_X.append(sim[2].metadata.parameters['thick'])
#         data_I.append(sim[2].metadata.total_I)
#         data_E.append(sim[2].metadata.total_E)
# data = np.array([data_X, data_I, data_E])

# dist = np.linspace(0.1,5,1000)
# absolute_scattering = n_measured_thick(flux, area, dist, rho, solid, cross, mu)
# fig, ax = plt.subplots(ncols=1, figsize=(10,4))
# ax.plot(dist, absolute_scattering, '-', label="Analytical")
# ax.errorbar(data[0]*100,data[1],data[2], fmt='+', label="McStas")
# ax.set(xlabel="thickness [cm]", ylabel="Intensity [n/s]")
# ax.legend()
# fig.tight_layout()
# fig.savefig('./figures/Incoherent_backscattering', dpi=300)



################################################################################
########## SANS
################################################################################
import pyFAI as pf

def P_sphere(q, R):
    res = 3*(np.sin(q*R) - q*R*np.cos(q*R) )/ (q*R)**3
    res = res**2
    return res

def n_measured(flux, A, dist, solid, sigma_att, phi,delta_rho, V, S, q,R):
    return flux*A*dist*solid/4/np.pi*sigma_att*phi*delta_rho**2*V*S*P_sphere(q,R)
flux = 1e7 # n/s/cm^2
a = 1 # cm^2
dist = 1 # cm
solid = 10_000/1000_000 # cm^2/cm^2
sigma_att = np.exp(-0.5*dist*10) # convert dist to meters
delta_rho = 5**2 #
phi = 1e-2 #
V = 1
S = 1
q = np.linspace(0.01, 1, 10000)
R = 100


# Load in the sans data
data = ms.load_data("../data/sans")
data = data[2] # And restrict ourselves to the last monitor

# Plot the raw data monitor
fig, ax = plt.subplots()
heat = ax.imshow(data.Intensity, norm='symlog', extent=data.metadata.limits)
fig.colorbar(heat, label=r'Intensity [\#n/s]')
ax.set(xlabel='x [cm]', ylabel ='y [cm]')

fig.tight_layout()
fig.savefig('./figures/sans_detector.png', dpi=300)

# Warning occurs from detector and ai. Disregard this.

detector = pf.detector_factory("detector")
detector.set_pixel1(1/1000)
detector.set_pixel2(1/1000)

# Set the azimuthal integrator
ai = pf.AzimuthalIntegrator(dist=5, detector=detector)


wavelength = 1/np.sqrt(5)/0.11056
ai.set_wavelength(4*1e-10)
ai.poni1  = 0.5
ai.poni2 = 0.5
two_theta, I = ai.integrate1d(data.Intensity, 1000, unit="2th_deg") 

fig, ax = plt.subplots(figsize=(10,4))
q = np.sin((two_theta)*np.pi/180/2)*4*np.pi/wavelength


ax.set(yscale="log")

ax.plot(q,n_measured(flux, a, dist, solid, sigma_att, phi,delta_rho, V, S, q,R), label="Analytical")
# q = np.insert(q,0,1e-3)[:-1]
ax.step(q, I,label="McStas")

# Set legends and labels
ax.legend()
ax.grid(True, which='major')
ax.set(xlabel=r"$Q [nm^-1]$", ylabel=r"Intensity [\#n/s]")
fig.tight_layout()
fig.savefig("./figures/SANS.png", dpi=300)


################################################################################
########## Powder
################################################################################

import pandas as pd
# # Load the powder structure and generate the theoretical diffractogram
# Load in Structure factor from Vesta

def get_formfact(file):
    data_from_cif = pd.read_table(file, sep=r'\s+', header=0)
    # data_from_cif = pd.read_table("Copper.txt", sep=r'\s+', header=0)

    cif = np.array([data_from_cif['2θ'],data_from_cif['|F|'],data_from_cif['M'], data_from_cif['d(Å)']] )

    theta_list = {}
    for i in range(len(cif[0])):
        if cif[0,i]>100 or np.isnan(cif[0,i]):
            continue
        # print(cif[3,i])
        
        form_factor = cif[1,i]**2
        # print(f"|F|={form_factor/100:.3f}\tmult={cif[2,i]}\tQ = {2*np.pi/cif[3,i]:.6f}\tTheta={cif[0,i]:.4g}")
        if cif[0,i] not in theta_list.keys():
            theta_list[cif[0,i]] = form_factor*cif[2,i]
            
        else:
            theta_list[cif[0,i]] += form_factor*cif[2,i]

    arr = np.zeros((len(theta_list),2))

    for i, (k, v) in enumerate(theta_list.items()):
        arr[i,:] = np.array((k,v))
    cif = arr.T
    return cif

# Scale the cif pattern 
def  n_measured(flux,A, dist,h, unit_cell_vol, wavelength, r,pattern):
    form_factor = pattern[1]/100
    # print(np.sqrt(form_factor))
    deb_prop = h/(2*np.sin(pattern[0]*np.pi/180)*r*np.pi)

    cross_section = 1 / unit_cell_vol**2 * wavelength**3 /4 /np.sin( pattern[0]*np.pi/180/2)*form_factor
    # cross_section = 
    result = flux * A * dist * deb_prop * cross_section # A * dist er basically bare V som ellers indgaar i spredninstvaersnit
    return np.array([pattern[0], result])

flux = 1.56009 * 1e6 # n/s/cm^2
A = 1 # cm^2
dist = 0.1 # cm
vol = 0.1 # cm^3
h = 0.1 # cm
r = 100 # cm
unit_cell_vol = 1079.1 # AA^3=10^-24 cm
wavelength = 2.567 # AA
rho = 1/unit_cell_vol # AA^-3

nacalf_analytical = get_formfact('../Powder/NaCaAlF_no_debye.txt')
nacalf_analytical = n_measured(flux, A, dist,h, unit_cell_vol, wavelength,r, nacalf_analytical)


# Load the data and generate the simulated diffractogram
data = ms.load_data("../data/powder_nacalf_no_debye")
data = data[-1]
print(data)
# split the data up into peaks and integrate over each peak
data_int = []
mask_areas = []
errs = []
for pos in nacalf_analytical[0]:
    mask = (data.xaxis>(pos-1.5)) & (data.xaxis<(pos+1.5))
    mask_areas.append(data.xaxis[mask])
    intensity = np.sum(data.Intensity[mask])
    errs.append(np.sqrt(np.sum(data.Error**2)))
    data_int.append(intensity)
data_int = np.array(data_int)


fig, ax = plt.subplots(figsize=(12,4), ncols=1)
ax.plot(nacalf_analytical[0], nacalf_analytical[1], 'x',markersize=10,label='Analytical')

ax.errorbar(nacalf_analytical[0], data_int,yerr=errs, fmt='.', label='McStas simulation')
ax.legend()
ax.set(ylim=(0))

ax.grid(True)
ax.set(xlabel=r"2$\theta$ [deg]",ylabel="Intensity Integrated at peaks [n/s]")
fig.tight_layout()
fig.savefig('./figures/powder.png', dpi=300)


######## Load in extra plot with anisotropy
# # Load the powder structure and generate the theoretical diffractogram
# Load in Structure factor from Vesta

def get_formfact(file):
    data_from_cif = pd.read_table(file, sep=r'\s+', header=0)
    # data_from_cif = pd.read_table("Copper.txt", sep=r'\s+', header=0)

    cif = np.array([data_from_cif['2θ'],data_from_cif['|F|'],data_from_cif['M'], data_from_cif['d(Å)']] )

    theta_list = {}
    for i in range(len(cif[0])):
        if cif[0,i]>100 or np.isnan(cif[0,i]):
            continue
        # print(cif[3,i])
        
        form_factor = cif[1,i]**2
        # print(f"|F|={form_factor/100:.3f}\tmult={cif[2,i]}\tQ = {2*np.pi/cif[3,i]:.6f}\tTheta={cif[0,i]:.4g}")
        if cif[0,i] not in theta_list.keys():
            theta_list[cif[0,i]] = form_factor*cif[2,i]
            
        else:
            theta_list[cif[0,i]] += form_factor*cif[2,i]

    arr = np.zeros((len(theta_list),2))

    for i, (k, v) in enumerate(theta_list.items()):
        arr[i,:] = np.array((k,v))
    cif = arr.T
    return cif

# Scale the cif pattern 
def  n_measured(flux,A, dist,h, unit_cell_vol, wavelength, r,pattern):
    form_factor = pattern[1]/100
    # print(np.sqrt(form_factor))
    deb_prop = h/(2*np.sin(pattern[0]*np.pi/180)*r*np.pi)

    cross_section = 1 / unit_cell_vol**2 * wavelength**3 /4 /np.sin( pattern[0]*np.pi/180/2)*form_factor
    # cross_section = 
    result = flux * A * dist * deb_prop * cross_section # A * dist er basically bare V som ellers indgaar i spredninstvaersnit
    return np.array([pattern[0], result])

flux = 1.56009 * 1e6 # n/s/cm^2
A = 1 # cm^2
dist = 0.1 # cm
vol = 0.1 # cm^3
h = 0.1 # cm
r = 100 # cm
unit_cell_vol = 1079.1 # AA^3=10^-24 cm
wavelength = 2.567 # AA
rho = 1/unit_cell_vol # AA^-3

nacalf_analytical = get_formfact('../Powder/NaCaAlF.txt')
nacalf_F = nacalf_analytical[1]


Qs = [0.866313, 1.22515, 1.5005, 1.73262, 1.93713, 1.93713, 2.12202, 2.29205, 2.29205, 2.4503,
 2.59894, 2.59894, 2.73953, 2.73953, 2.87323, 3.001, 3.12354, 3.12354, 3.12354, 3.12354,
 3.35522, 3.35522, 3.46525, 3.5719, 3.5719, 3.5719, 3.67545, 3.67545]


F_from_mcstas = [11.0757, 99.6616, 210.186, 485.24, 84.0234, 17.388, 198.876, 102.361, 245.603, 331.574,
 5.85067, 829.963, 657.752, 621.93, 3531.75, 77.4813, 2223.77, 141.778, 41.9975, 1094.61,
 2327.73, 1120.93, 2824.76, 5.11079, 289.443, 121.116, 211.953, 678.133]

Fs = []
for i, refl in enumerate(Qs):
    if Qs[i-1] == refl:
        Fs[-1] += F_from_mcstas[i]
    else:
        Fs.append(F_from_mcstas[i])

Fs = np.array(Fs)

# Try to read in reflections from FullProf

form_fullprof = np.loadtxt('../Powder/Full_test.hkl', skiprows=3)
form_fullprof = form_fullprof[:,3:]
full_q_list = {}
for refl in range(len(form_fullprof[:,0])):
    if (form_fullprof[refl,3])>7.5:
        continue
    if (form_fullprof[refl,3])<1.7:
        break
    form_factor = form_fullprof[refl,5]
    # print(f"|F|={form_factor/100:.3f}\tmult={form_ncrystal[2,i]}\tQ = {2*np.pi/form_ncrystal[3,i]:.6f}\tTheta={form_ncrystal[0,i]:.4g}")
    if round(form_fullprof[refl,4],4) not in full_q_list.keys():
        full_q_list[round(form_fullprof[refl,4],4)] = form_factor*form_fullprof[refl,0]
        # print('Adding')
    else:
        # print(i)
        full_q_list[round(form_fullprof[refl,4],4)] += form_factor*form_fullprof[refl,0]
full_q_list = np.array(sorted(full_q_list.items()))


nacalf_McStas = nacalf_analytical.copy()
nacalf_McStas[1] = Fs*100
nacalf_McStas = n_measured(flux, A, dist,h, unit_cell_vol, wavelength,r, nacalf_McStas)
nacalf_Full = nacalf_analytical.copy()
nacalf_Full[1] = full_q_list[:,1]*100
nacalf_Full = n_measured(flux, A, dist,h, unit_cell_vol, wavelength,r, nacalf_Full)
nacalf_analytical = n_measured(flux, A, dist,h, unit_cell_vol, wavelength,r, nacalf_analytical)

for i in range(len(Fs)):
    print(f'Mcstas = {Fs[i]:.5f}\tAnalytical_Vesta={nacalf_F[i]/100:.5f}\tAnal_Full={full_q_list[i,1]}')
# Load the data and generate the simulated diffractogram
data = ms.load_data("../data/powder_nacalf")
data = data[-1]
print(data)
# split the data up into peaks
data_int = []
mask_areas = []
errs = []
for pos in nacalf_analytical[0]:
    mask = (data.xaxis>(pos-1.5)) & (data.xaxis<(pos+1.5))
    mask_areas.append(data.xaxis[mask])
    intensity = np.sum(data.Intensity[mask])
    errs.append(np.sqrt(np.sum(data.Error**2)))
    data_int.append(intensity)


data_int = np.array(data_int)
print(f"Mcstas={data_int}\nAnalytical={nacalf_analytical[1]}\n")

fig, ax = plt.subplots(figsize=(12,4), ncols=1)

# ax2 = ax.twinx()
ax.plot(nacalf_analytical[0], nacalf_analytical[1], 'r.',markersize=10,label=r'Analytical using Vesta $|F|^2$')
ax.plot(nacalf_McStas[0], nacalf_McStas[1], '+',markersize=10,label=r'Analytical using McStas $|F|^2$')
ax.plot(nacalf_Full[0], nacalf_Full[1], 'x',markersize=10,label=r'Analytical using Full $|F|^2$') # With fullprof
ax.errorbar(nacalf_analytical[0], data_int,yerr=errs, fmt='.', label='McStas simulation')

# ax2.errorbar(data.xaxis, data.Intensity, fmt='k-', label='McStas')


ax.legend()

ax.set(ylim=(0))
# ax2.set(ylim=(0,0.4))
ax.grid(True)
ax.set(xlabel=r"2$\theta$ [deg]",ylabel="Intensity Integrated at peaks [n/s]")
# ax2.set(ylabel="Intensity [n/s] simulation output")
fig.tight_layout()
fig.savefig('./figures/powder_debye.png', dpi=300)

print("Just before single crystal")

################################################################################
########## Single Crystal
################################################################################
# Load in the data
data_single = ms.load_data('../data/single_crystal_ybco')
data_pretty_plot = ms.load_data('../data/single_crystal_high_wave')
data_ncrystal = ms.load_data('../data/ncrystal_ybco')
data_cop = ms.load_data('../data/single_crystal_cop')
fourPiMon = data_pretty_plot[-5]
azim = (fourPiMon.metadata.limits[0],fourPiMon.metadata.limits[1])
vert = fourPiMon.metadata.limits[2],fourPiMon.metadata.limits[3]


X, Y = np.meshgrid(np.linspace(*azim, 3600), np.linspace(*vert,3600))

# First plot the 4 Pi monitor
fig, ax = plt.subplots(figsize=(16,8), ncols=2)
ax[0].imshow(fourPiMon.Intensity, norm='log', 
             cmap='Blues_r',
             extent =fourPiMon.metadata.limits, aspect='auto')
ax[0].set(xlabel='Horizontal angle [deg]', ylabel='Vertical angle [deg]')
ax[1].set(xlabel='Horizontal angle [deg]', ylabel='Vertical angle [deg]')
# Make a mask to select only the data that is within a specific reflection
x_min = 86.5
x_max = 98
y_min = -2
y_max = 2
mask = ((X>x_min) & (X<x_max))
mask = mask & ((Y>y_min) & (Y<y_max))
zoomed_in = np.where(mask, fourPiMon.Intensity, np.nan)   # same shape as X (3600, 3600)

heat = ax[1].imshow(zoomed_in, norm='symlog',cmap='Blues_r', aspect='auto',
                    extent=fourPiMon.metadata.limits)
ax[1].set_xlim(x_min, x_max)   # zoom in x-range
ax[1].set_ylim(y_min, y_max)   # zoom in y-range
fig.colorbar(heat, label=r"Intensity [\#n/s]")
# Make a 

# --- Add a zooming box on the left plot ---
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
rect = patches.Rectangle((x_min, y_min),   # lower left corner
                         x_max - x_min,    # width
                         y_max - y_min,    # height
                         linewidth=2, edgecolor='purple', facecolor='none')
ax[0].add_patch(rect)

# --- Draw connector lines between box and zoom subplot ---
mark_inset(ax[0], ax[1],
           loc1=2, loc2=3,   # corners to connect (2=upper left, 4=lower right)
           fc="none", ec="purple", lw=1.5)

# --- Add colored border around zoomed plot ---
for spine in ax[1].spines.values():
    spine.set_edgecolor("purple")
    spine.set_linewidth(2)
fig.tight_layout()

fig.savefig('./figures/single_crystal_four_pi', dpi=600)


#### Calculate the intensities that should be measured on the detector
# Find the integral of the reflection
def calculate_intensity(
        vol, unit_cell, specific_flux, 
        wavelength_band, wavelength, 
        theta, form_factor)->float:
    return vol/unit_cell**2 * specific_flux/wavelength_band * wavelength**4/(2*np.sin(theta)**2) * form_factor

zoomed_in = np.where(mask, data_single[-5].Intensity, np.nan)   # same shape as X (3600, 3600)

simul_result_ybco = np.sum(zoomed_in[zoomed_in>0])
specific_flux_ybco = data_single[0].metadata.total_I # #n/s /cm^2
vol_ybco = 0.01 # cm^3

unit_cell_ybco = 404.778 # AA^3
wavelength_ybco = 1.944 # AA
wavelength_band_ybco = 0.4 ## AA
theta_ybco = 90.8*np.pi/180/2 # Half of the angle measured
form_factor_ybco = 105.588**2/100
anal_ybco: float = calculate_intensity(vol_ybco, unit_cell_ybco,
                                        specific_flux_ybco, wavelength_band_ybco, 
                                        wavelength_ybco, theta_ybco, form_factor_ybco)


zoomed_in_ncrystal = np.where(mask, data_ncrystal[-5].Intensity, np.nan)   # same shape as X (3600, 3600)

simul_result_ybco_ncrystal = np.sum(zoomed_in_ncrystal[zoomed_in_ncrystal>0])

print(f"YBCO Analytical result = {anal_ybco:.4f}\tSimulation result = {simul_result_ybco:.4f}"
      f"\tncrystal={simul_result_ybco_ncrystal:.4f}"
      )
print(f"difference={(anal_ybco-simul_result_ybco)/anal_ybco}")

######################### COPPER SECTION


zoomed_in = np.where(mask, data_cop[-5].Intensity, np.nan)   # same shape as X (3600, 3600)
simul_result_cop = np.sum(zoomed_in[zoomed_in>0])

vol_cop = 0.01 # cm^3
specific_flux_cop = data_cop[0].metadata.total_I # #n/s /cm^2
unit_cell_cop = 47.2416
wavelength_cop = 1.8694804812493104
wavelength_band_cop = 0.2
theta_cop = 94*np.pi/180/2 # Half of the angle measured
form_factor_cop = 30.872


form_factor_cop = form_factor_cop**2/100 # Convert fm^2 to barns 
# form_factor_cop = 9.5308

anal_cop: float = calculate_intensity(vol_cop, unit_cell_cop, specific_flux_cop, 
                                      wavelength_band_cop, wavelength_cop, 
                                      theta_cop, form_factor_cop)


print(f"Copper Analytical result = {anal_cop:.4f}\tSimulation result = {simul_result_cop:.4f}")
# print(anal_cop,vol, unit_cell, specific_flux, wavelength_band, wavelength, theta, form_fact)
print(f"difference={(anal_cop-simul_result_cop)/anal_cop}")



################################################################################
########## Reflectivity
################################################################################


# import the reflectivity file
reflectivity_file = np.loadtxt('../Reflecting/supermirror_m3.rfl').T
# Import the mcstas simulation
files = os.listdir('../data/refl')
simulation = []
for item in files:
    item_path = os.path.join('../data/refl', item)
    if os.path.isdir(item_path) and item.isdigit():
        simulation.append(ms.load_metadata(item_path))

xaxis = np.array([x[4].parameters['sample_rotation'] for x in simulation])
lam = 1.2
xaxis = 4*np.pi/lam*np.sin(xaxis*np.pi/180) # Convert theta to Q
I =  [x[4].total_I/x[1].total_I for x in simulation]

fig, ax = plt.subplots()
ax.plot(reflectivity_file[0], reflectivity_file[1], label='Analytical')
ax.plot(xaxis,I, '.', label='McStas simulation')
ax.set(xlabel=r'Q [$\AA^{-1}$]', ylabel='Reflectivity')
ax.legend()
fig.tight_layout()
fig.savefig('./figures/reflectivity.png', dpi=300)



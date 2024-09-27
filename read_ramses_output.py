import json
import numpy as np
from scipy.io import FortranFile
# with all 36 variables loaded this script takes ~5.9GB of RAM

# the output contains 5 basic hydro variable and 31 mass fraction variable (1 ism, 27 elements and 3 radioactive isotopes)
# var_dict controls the variables this script reads
var_dict = {0:"density", 1:"vx", 2:"vy", 3:"vz", 4:"pressure", 5:"ism",
            6:"C", 7:"N", 8:"O", 9:"F", 10:"Ne",
            11:"Na", 12:"Mg", 13:"Al", 14:"Si", 15:"P",
            16:"S", 17:"Cl", 18:"Ar", 19:"K", 20:"Ca",
            21:"V", 22:"Ti", 23:"Sc", 24:"Cr", 25:"Mn",
            26:"Fe", 27:"Co", 28:"Ni", 29:"Cu", 30:"Zn",
            31:"Ga", 32:"Ge", 33:"Ni56", 34:"Co56", 35:"Ni57"}
ilevel = 8 # sim resolution = 2^8 = 256 grids per side

target_dir = "t24" # reads from this folder

with open(target_dir+'/info.json', 'r') as comoving_info_file:
    comoving_info = json.load(comoving_info_file)

# Physical constant, bolzmann and hydrogen mass
kB = 1.38062e-16
mH = 1.66e-24

scale_d = 1.66e-24 # 1 atom(hydrogen) per cc
scale_t = 2629746 # 1 mo, or 365.2425/12  = 30.439 days
scale_l = 3.0857e18 # 1 pc
scale_T2_inv = (kB*scale_t**2)/ (scale_l**2*mH) # Pressure scaling factor


density_coff = comoving_info['aexp']**(-3.0)
box_len = comoving_info['box_len_0'] * comoving_info['aexp'] # actual box size
dx = box_len / 2**ilevel # grid size in pc
dvol = dx**3 # grid volume (in pc^3)
dvol_cm3 = dvol * scale_l**3 # grid volume in cm^3
aexp_dot = comoving_info["lambda_exp"]**(1-comoving_info["lambda_exp"]) * (comoving_info['aexp'])**((comoving_info["lambda_exp"]-1)/comoving_info["lambda_exp"])

input_data = np.zeros((2**ilevel, 2**ilevel, 2**ilevel, len(var_dict)))

# read desity/mass
raw = FortranFile("{}/{}.dat".format(target_dir,var_dict[0]), "r")
[nx, ny, nz] = raw.read_ints()
dat =  raw.read_reals(dtype='f4')
raw.close()
dat = dat.reshape(nz, ny, nx)
input_data[:, :, :, 0] = dat*scale_d*density_coff # density of each grid in g/cm^3
# input_data[:, :, :, 0] = dat*dvol_cm3*scale_d*density_coff # mass of each grid in g

# read velocity and revert comoving ref. frame to stationary ref. frame, unit in cm/s
centeroid = (2**ilevel-1)/2
coord_array = np.stack(np.meshgrid(np.arange(2**ilevel), np.arange(2**ilevel), np.arange(2**ilevel), indexing='ij'),axis=3) - [centeroid, centeroid, centeroid]
d_array = coord_array*dx/comoving_info['aexp']
# vx
raw = FortranFile("{}/{}.dat".format(target_dir,var_dict[3]), "r")
[nx, ny, nz] = raw.read_ints()
dat =  raw.read_reals(dtype='f4')
raw.close()
dat = dat.reshape(nz, ny, nx)
input_data[:, :, :, 1] = (dat/comoving_info['aexp'] + aexp_dot*d_array[:,:,:,0])*scale_l/scale_t
# vy
raw = FortranFile("{}/{}.dat".format(target_dir,var_dict[2]), "r")
[nx, ny, nz] = raw.read_ints()
dat =  raw.read_reals(dtype='f4')
raw.close()
dat = dat.reshape(nz, ny, nx)
input_data[:, :, :, 2] = (dat/comoving_info['aexp'] + aexp_dot*d_array[:,:,:,1])*scale_l/scale_t
# vz
raw = FortranFile("{}/{}.dat".format(target_dir,var_dict[1]), "r")
[nx, ny, nz] = raw.read_ints()
dat =  raw.read_reals(dtype='f4')
raw.close()
dat = dat.reshape(nz, ny, nx)
input_data[:, :, :, 3] = (dat/comoving_info['aexp'] + aexp_dot*d_array[:,:,:,2])*scale_l/scale_t

# read pressure and convert to temperature
raw = FortranFile("{}/{}.dat".format(target_dir,var_dict[4]), "r")
[nx, ny, nz] = raw.read_ints()
dat =  raw.read_reals(dtype='f4')
raw.close()
dat = dat.reshape(nz, ny, nx)
input_data[:, :, :, 4] = np.divide(dat/scale_T2_inv, input_data[:, :, :, 0]/scale_d/density_coff)/comoving_info['aexp']**2
# temperature in Kelvin, not accurate for cool components (<10^7 K)

# read mass fractions (values from 0 to 1)
for i in var_dict.keys():
    if i < 5:
        continue
    raw = FortranFile("{}/{}.dat".format(target_dir,var_dict[i]), "r")
    [nx, ny, nz] = raw.read_ints()
    dat =  raw.read_reals(dtype='f4')
    raw.close()
    dat = dat.reshape(nz, ny, nx)
    input_data[:, :, :, i] = dat
# you can now access all variables of the simulation output from input_data array
i_x = 127
i_y = 70
i_z = 127
print("For grid No. x = {}, y = {}, z = {}:".format(i_x, i_y, i_z))
print("Density (g/cm^3) = {:.4e}".format(input_data[i_x, i_y, i_z, 0]))
print("X Vel (cm/s) = {:.4e}".format(input_data[i_x, i_y, i_z, 1]))
print("Y Vel (cm/s) = {:.4e}".format(input_data[i_x, i_y, i_z, 2]))
print("Z Vel (cm/s) = {:.4e}".format(input_data[i_x, i_y, i_z, 3]))
print("Mg Mass Fraction = {:.4f}".format(input_data[i_x, i_y, i_z, 12]))
print("Si Mass Fraction = {:.4f}".format(input_data[i_x, i_y, i_z, 14]))
import h5py
filename = 't6.hdf5'
h5 = h5py.File(filename,'r')
input_data = h5['default']
h5.close()
# 36 variables in total
var_dict = {0:"density", 1:"vx", 2:"vy", 3:"vz", 4:"pressure", 5:"temp",
            6:"C", 7:"N", 8:"O", 9:"F", 10:"Ne",
            11:"Na", 12:"Mg", 13:"Al", 14:"Si", 15:"P",
            16:"S", 17:"Cl", 18:"Ar", 19:"K", 20:"Ca",
            21:"V", 22:"Ti", 23:"Sc", 24:"Cr", 25:"Mn",
            26:"Fe", 27:"Co", 28:"Ni", 29:"Cu", 30:"Zn",
            31:"Ga", 32:"Ge", 33:"Ni56", 34:"Co56", 35:"Ni57"}

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
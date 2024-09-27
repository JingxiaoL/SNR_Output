# SNR_Output
Output models of RAMSES SNR simulations

Each t*.tgz is a compressed file of a snapshot, t1 means snapshot at t=1 month, t24 means snapshot at t=24 month

Script read_ramses_output.py is an example for how to read simulation output (requires numpy and scipy)

Example:  
1.Download t24.tgz  
2.Unzip the file  
  >tar -zxvf t24.tgz

  This creates a folder name t24 (2.4GB when unzipped)  
3. Edit line 17 of read_ramses_output.py to point at the t24 folder (target_dir = "t24")  
4. Run "python3 read_ramses_output.py" and it should prints something like this:  
>      For grid No. x = 127, y = 70, z = 127:  
>      Density (g/cm^3) = 2.2703e-19  
>      X Vel (cm/s) = -1.2367e+07  
>      Y Vel (cm/s) = -1.4285e+09  
>      Z Vel (cm/s) = -1.1768e+07  
>      Mg Mass Fraction = 0.1123  
>      Si Mass Fraction = 0.1360  

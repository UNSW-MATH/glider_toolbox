##########################################################
# glider_toolbox.py
#------------------
# toolbox of python functions useful for
# IMOS glider applications
#-------------------------
# Created 08/05/2019
#-------------------
# Contributions: 
# Michael Hemming | UNSW, m.hemming@unsw.edu.au
# name            | uni, email
#----------------------------------------------
 ##########################################################

import numpy as np
import pandas as pd
import xarray as xr
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    

def find_chunks(data_dir):
     # Zarr chunks need to be uniform size 
     # data_dir = directory where IMOS glider .nc files exist
     # grab list of IMOS .nc files in data_dir
     files = glob.glob(data_dir + '*.nc')
     # get size of time dimension if files were concatenated together
     # preallocate
     dim_n = np.zeros(len(files))
     # loop to get size of time dimension
     for n_files in range(1,len(files)):
         # get netCDF file info
         f=Dataset(files[n_files])
         # get length of time dimension in netCDF
         dim_n[n_files-1] = len(f.dimensions['TIME'])
     # get size of time dimension
     sum_file_dim = np.sum(dim_n)
  
     # now to find chunks required fo Dask tasks
     # preallocate 
     chunk_options = np.zeros(int(sum_file_dim))
     # for range between 1 and size of time dimension
     range_of_nchunks = range(1,int(sum_file_dim))
     # loop to find those number divisible without remainders
     for n_chunks in range_of_nchunks: 
         if sum_file_dim%range_of_nchunks[n_chunks-1] == 0:   
             chunk_options[n_chunks-1] = sum_file_dim / range_of_nchunks[n_chunks-1]
     # Use those chunks greater than 1000 and not including size of dimension as a chunk size
     # small chunk size will mean too many chunks
     selection = chunk_options > 1000
     selected_chunks = chunk_options[selection]
     selected_chunks_bool = selected_chunks != sum_file_dim
     glider_chunks = int(np.min(selected_chunks[selected_chunks_bool]))       
             
     return glider_chunks    
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    
    
def glider_concat(data_dir,glider_chunks,file_name):
    # data_dir = directory where IMOS glider .nc files exist
    # chunks = output variable 'glider_chunks' from function 'find_chunks'
    # file_name = specify string for name of file (not including extension e.g. '.nc')
    
    # concatenate IMOS glider netCDF files in data_dir
    data_files = xr.open_mfdataset(data_dir + 'IMOS*2009*.nc', concat_dim='TIME',
                data_vars='minimal',parallel=True).chunk(glider_chunks) # 2009 only for now
    print('Data concatenated..')
    # save concatenated IMOS glider data as netCDF in data_dir
    data_files.to_netcdf(path=data_dir + file_name + '.nc',mode='w',format='netCDF4')
    print('file: ' + file_name + '.nc' + ' saved in: ' + data_dir)
    # save concatenated IMOS glider data as netCDF in data_dir
    data_files.to_zarr(store=data_dir + file_name + '.zarr',mode='w')
    print('file: ' + file_name + '.zarr' + ' saved in: ' + data_dir) 
    
    return data_files
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    
    
#def scatter_time_depth_TEMP(data_files,var):
    # data_files = data set output from glider_concat
    
    # This function is in progress



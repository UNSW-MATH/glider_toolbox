#--------------------------------------------
# import functions
from glider_toolbox import glider_concat
from glider_toolbox import find_chunks

#-------------------------------------------- 
# define local and data directory
local_dir = "/your/directory"
data_dir = local_dir + '/your/data/directory'

#--------------------------------------------
# define best chunks for .zarr file
glider_chunks = find_chunks(data_dir)

#--------------------------------------------
# save concatenated glider data as netCDF and zarr files in 
# data directory
file_name = 'Concat_glider'
data_files = glider_concat(data_dir,glider_chunks,file_name)

#--------------------------------------------








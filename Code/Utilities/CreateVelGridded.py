# CreateLTSPs.py
#
# Created on 30/01/2023
# Written by  Michael Hemming (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au
#
# %% -----------------------------------------------------------------------------------------------
# Determine which computer this script is on

import os
if 'mphem' in os.getcwd():
    account = 'mphem'
else:
    account = 'z3526971'

# %% ------------------------------------------------------------------------------------
# Import Packages

import os
import glob
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\' + 
         'LTSPs\\python-aodntools-master\\')
# Velocity LTSPs
import aodntools.timeseries_products.velocity_aggregated_timeseries as vat
import aodntools.timeseries_products.velocity_hourly_timeseries as vatrly
import aodntools.timeseries_products.velocity_gridded_timeseries_Michael as vatm
# Temp/other LTSPs
import aodntools.timeseries_products.aggregated_timeseries as agg
import aodntools.timeseries_products.hourly_timeseries as hrly
import aodntools.timeseries_products.gridded_timeseries as grid
# other packages
import numpy as np
import numpy.matlib
import requests
import re
import xarray as xr
import psutil
import shutil
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\LTSPs\\')
import LTSP_Functions as LTSPFs
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\')
import QCreport_paths as paths
import QCreport_setup as setup

# %% ------------------------------------------------------------------------------------
# check if not already a velocity gridded product for each site

node = 'NSW'
# sites = ['BMP070','BMP090','BMP120','SYD140','SYD100','PH100','ORS065','CH050','CH070','CH100']
sites = ['CH070','CH100']

files = []
for ns in range(len(sites)):
    path = paths.main_path_data + sites[ns] + '\\LTSPs\\gridded_timeseries\\'
    files.append(glob.glob(path +'*velocity*.nc'))

# %% ------------------------------------------------------------------------------------
# if not existing, create one

for ns in range(len(sites)):
    if '[]' in str(files[ns]):  
        print(sites[ns])
        # get velocity hourly file
        path = paths.main_path_data + sites[ns] + '\\LTSPs\\hourly_timeseries\\'
        fs = glob.glob(path +'*velocity*.nc')
        findfs = fs[0].find('IMOS_ANMN')
        fs = fs[0][findfs::]
        if os.path.exists(paths.TEMPORARY_dir + fs[0]) == False:
            shutil.copy((path + fs),
                        (paths.TEMPORARY_dir + fs))
        # create gridded product
        ncout = vatm.grid_variable(fs, sites[ns], depth_bins=None, max_separation=16, 
                           depth_bins_increment=1, input_dir=paths.TEMPORARY_dir, output_dir=paths.TEMPORARY_dir, 
                           download_url_prefix=None, opendap_url_prefix=None)
        # copy the product to the server
        new_path = paths.main_path_data + sites[ns] + '\\LTSPs\\gridded_timeseries\\'
        new_fs = ncout[ncout.find('IMOS_ANMN')::]
        shutil.copy(ncout,(new_path + new_fs))

# !!! Need to create LTSPs at ORS065, need hourly velocity at CH050 sites


# %% ------------------------------------------------------------------------------------

# %% ------------------------------------------------------------------------------------




# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 16:11:23 2023

@author: z3526971
"""

import glob

files = glob.glob('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\\PROCESSED_2_5\\' + 
                  'PH100\\TEMPERATURE\\IMOS*2112*.nc')

for f in files:
    print(xr.open_dataset(f).instrument_nominal_depth)
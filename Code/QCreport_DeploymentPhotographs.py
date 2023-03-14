#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun 12 14:18:48 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# Section: Deployment Photographs

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Python Packages
import glob
import os
import QCreport_format as form

#------------------------------------------------------------
# Information 
#-------------

# This is the Python package required to run 
# this script. The python modules should be installed using 
# 'pip/condo install'. 

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Function to include all photographs in file location
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

def include_photos(path, doc):   
 
    # Get list of toolbox plots
    # images = glob.glob(path + '\\*')
    images = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.jpg', '.JPG','.png','.PNG')):
                images.append(os.path.join(root, file))
    # include toolbox plots
    for im in images:
        if 'jpg' in im or 'png' in im:
            with doc.create(form.Figure()) as pic:        
                pic.add_image(im,width=form.NoEscape(r'0.7\linewidth'))
             
        

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
            
            

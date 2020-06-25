#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun 11 14:42:34 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Toolbox Plots

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Python Packages
import glob
import QCreport_paths as paths

#------------------------------------------------------------
# Information 
#-------------

# This is the Python package required to run 
# this script. The python modules should be installed using 
# 'pip/condo install'. 
# paths imported

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Function to include Toolbox plots
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

def toolbox_plots(path, report):   
 
    # Get list of toolbox plots
    images = glob.glob(path + '*-' +paths.deployment_file_date_identifier + '*.png')
    # include toolbox plots
    for plots in range(len(images)):
        if plots > 0:
            report.add_page(orientation='l')
        report.image(images[plots],h=150,w=300,x=-10,y=30)

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
        




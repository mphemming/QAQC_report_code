#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun 11 14:42:34 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Toolbox Plots

# %% -----------------------------------------------------------------------------------------------
# Import packages

import QCreport_paths as paths
import glob
from fpdf import FPDF

# %% -----------------------------------------------------------------------------------------------
# Function to include Toolbox plots

def toolbox_plots(path, report):   
 
    # Get list of toolbox plots
    images = glob.glob(path + '*.png')
    # include toolbox plots
    for plots in range(len(images)):
        if plots > 0:
            report.add_page(orientation='l')
        report.image(images[plots],h=150,w=300,x=-10,y=30)






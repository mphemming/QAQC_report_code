#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun 11 14:42:34 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# Section: Toolbox Plots

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Python Packages
import glob
import QCreport_setup as setup
import QCreport_format as form
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

def toolbox_plots(path, doc):   
 
    # Get list of toolbox plots
    images = glob.glob(path + '*-' +setup.deployment_file_date_identifier + '*.png')
    # include toolbox plots
    for plots in range(len(images)):
        if plots > 0:
            doc.append(form.Command('newpage'))
        file = images[plots]
        file = file.replace('\\','/')
        f = max([i for i, letter in enumerate(file) if letter == '/'])
        caption_txt = file[f+1::]
        doc.append(form.Command('begin','sidewaystable'))
        doc.append(form.StandAloneGraphic(file,'scale=0.4'))
        doc.append(form.Command('caption',caption_txt))
        # doc.append(form.Command('end','turn'))
        doc.append(form.Command('end','sidewaystable'))



# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
        




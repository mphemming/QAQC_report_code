# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:03:39 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Deployment Details


# -----------------------------------------------------------------------------------------------
# Import packages

from fpdf import FPDF
import QCreport_paths as paths
import QCreport_format as form
import QCreport_netCDF as nc

attributes = nc.get_netCDF(paths.ncdir())

# -----------------------------------------------------------------------------------------------
# Create Table of details

def Table(report):
    print('Hello')


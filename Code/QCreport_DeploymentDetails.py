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

# get netCDF attributes for section
attributes = nc.get_netCDF(paths.ncdir())

# -----------------------------------------------------------------------------------------------
# Create Table of details


def Table(report):
    
    report.set_font_size(14)
    report.set_fill_color(224,224,224)
    report.cell(200, 10, 'text', 0, 2, 'C') 
    report.cell(20,12,"Order #",1,0,'C');  #Write a cell 20 wide, 12 high, filled and bordered, with Order # centered inside, last argument 'true' tells it to fill the cell with the color specified
    report.cell(20,12,"Coding",1,0,'C');
    report.cell(20,12,"Sales Code",1,1,'C'); #the 1 before the 'C' instead of 0 in previous lines tells it to move down by the height of the cell after writing this
    report.cell(20,12,'1',1,0,'C');
    report.cell(20,12,'1',1,0,'C');
    report.cell(20,12,'1',1,1,'C');
    

#def convert_dict(dict):
#    for key, value in dict.iteritems():
#    temp = [key,value]
#    dictlist.append(temp)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun  4 13:42:02 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Create a QC report for a selected site and deployment
# o   Uses the Python FPDF package t create a PDF report
# o   TBC
# o   TBC

# Instructions:

# o   Modify script 'QCreport_format.py' to setup QC report
# o   Run this script

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Import packages

import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
from PyPDF2 import PdfFileReader
from numpy import loadtxt


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Determine Paths

# import script variables and functions
import QCreport_paths as paths
# obtain paths
netCDF_dir = paths.ncdir()
toolbox_dir = paths.tbdir()
saving_dir = paths.savedir()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Create document and set Format

# import script variables and functions
import QCreport_format as form
# call function to format document
report = form.format_doc(paths.name_of_reportmaker)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Sections

report.add_page(orientation='p')
form.section_header('Deployment Details')
DD = report.add_link()
report.set_link(DD)

report.add_page(orientation='p')
form.section_header('Deployment Instruments')
DI = report.add_link()
report.set_link(DI)

report.add_page(orientation='p')
form.section_header('Mooring Diagram')
MD = report.add_link()
report.set_link(MD)

report.add_page(orientation='l')
form.section_header('Toolbox Plots')
TBP = report.add_link()
report.set_link(TBP)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Plots

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Header and Table of Contents

report.add_page(orientation='p')

# Main Header
report.set_font_size(28)
report.cell(200, 10, form.title_1, 0, 2, 'C') 
report.set_font_size(22)
report.cell(200, 10, form.title_2, 0, 2, 'C') 

# line break
report.ln(30)

# interactive table of contents

# Add section header
form.section_header('Report Contents')

form.TOC('Deployment Details',DD)
form.TOC('Deployment Instruments',DI)
form.TOC('Mooring Diagram',MD)
form.TOC('Toolbox Plots',TBP)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Save report

report.output(saving_dir + paths.site_name + '_' + paths.deployment + '_QC_report.pdf', 'F')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -----------------------------------------------------------------------------------------------
# Reorganise PDF report so that title and table of contents is at the beginning of the document

PDF_report = PdfFileReader(saving_dir + paths.site_name + '_' + paths.deployment + '_QC_report.pdf')

# NOTES: USE PyPDF to REORGANISE THE DOCUMENT AFTERWARDS
# https://pythonhosted.org/PyPDF2/PageObject.html
# https://pythonhosted.org/PyPDF2/PdfFileReader.html
# https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/
# http://fpdf.org/en/doc/

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>









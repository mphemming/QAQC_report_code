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

# %% -----------------------------------------------------------------------------------------------
# Import packages

import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from numpy import loadtxt


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Determine Paths

# import script variables and functions
import QCreport_paths as paths
# obtain paths
netCDF_dir = paths.ncdir_TEMP()
toolbox_dir = paths.tbdir()
saving_dir = paths.savedir()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Create document and set Format

# import script variables and functions
import QCreport_format as form
# call function to format document
report = form.format_doc(paths.name_of_reportmaker)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Sections

# Deployment Details
report.add_page(orientation='p')
form.section_header('Deployment Details')
DD = report.add_link()
report.set_link(DD)
# import Section content
import QCreport_DeploymentDetails as DepDet
DepDet.intro_table(report)
DepDet.instrument_table(report)
#DepDet.parameter_bullets(report)
DepDet.timeinout_table(report)
DepDet.parameter_table(report)
DepDet.files_table(report)
DepDet.instrument_bullets(report)

# Mooring diagram
report.add_page(orientation='p')
form.section_header('Mooring Diagram')
MD = report.add_link()
report.set_link(MD)
# Add image
report.image(paths.mddir())

# Quality Control 
report.add_page(orientation='p')
form.section_header('Quality Control')
QC = report.add_link()
report.set_link(QC)
# import Section content
import QCreport_QualityControl as QCR
QCR.QC_comments(report)

# Toolbox Plots
report.add_page(orientation='l')
form.section_header('Toolbox Plots')
TBP = report.add_link()
report.set_link(TBP)
# import Section content
import QCreport_ToolboxPlots as tbp
tbp.toolbox_plots(paths.tbdir(),report)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Plots

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
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
form.TOC('Mooring Diagram',MD)
form.TOC('Quality Control',QC)
form.TOC('Toolbox Plots',TBP)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Save report

report.output(saving_dir + paths.site_name + '_' + paths.deployment + '_QC_report.pdf', 'F')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Reorganise PDF report so that title and table of contents is at the beginning of the document

# THIS METHOD DOES NOT WORK. THE TOC LINKS NO LONGER WORK... LOOK FOR ANOTHER METHOD

#PDF_report = PdfFileReader(saving_dir + paths.site_name + '_' + paths.deployment + '_QC_report.pdf')
#pdf_bulk_writer = PdfFileWriter()
#output_filename_bulk = "bulk.pdf"
#pdf_TOC_writer = PdfFileWriter()
#output_filename_TOC = "TOC.pdf"
#
#for page in range(PDF_report.getNumPages()):
#    current_page = PDF_report.getPage(page)
#    if page == PDF_report.getNumPages()-1:
#        pdf_TOC_writer.addPage(current_page)
#    if page <= PDF_report.getNumPages()-2:
#        pdf_bulk_writer.addPage(current_page)
#        
## Write the data to disk
#with open(output_filename_TOC, "wb") as out:
#     pdf_TOC_writer.write(out)
#     print("created", output_filename_TOC)       
#
## Write the data to disk
#with open(output_filename_bulk, "wb") as out:
#     pdf_bulk_writer.write(out)
#     print("created", output_filename_bulk)   
#
#pdfs = ['TOC.pdf', 'bulk.pdf']
#
#merger = PdfFileMerger()
#
#for pdf in pdfs:
#    merger.append(pdf)
#    
#merger.write("result.pdf")
#merger.close()

# NOTES: USE PyPDF to REORGANISE THE DOCUMENT AFTERWARDS
# https://pythonhosted.org/PyPDF2/PageObject.html
# https://pythonhosted.org/PyPDF2/PdfFileReader.html
# https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/
# http://fpdf.org/en/doc/

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>









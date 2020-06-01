#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:47:30 2020

@author: Michael
"""

import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
from numpy import loadtxt

# -----------------------------------------------------------------------------------------------
# Load Deployment text information
deployment_filename = "/Users/Michael/Documents/Work/UNSW/Work/QC_reports/text_files/Deployment.txt"
with open(deployment_filename, 'r') as file:
    deployment_info = file.read().replace('\n', '')



# -----------------------------------------------------------------------------------------------
# Title of document
title = 'PH100 Quality Control Report'

# -----------------------------------------------------------------------------------------------
# Define the style of various elements of the document
#class report(FPDF):
#    def header(self):
#        # Arial bold 15
#        self.set_font('Helvetica', 'B', 30)
#        # Calculate width of title and position
#        w = self.get_string_width(title) + 6
#        self.set_x((210 - w) / 2)
#        # Colors of frame, background and text
#        self.set_draw_color(52, 70,110)
#        self.set_fill_color(255, 255, 255)
#        self.set_text_color(52, 70,110)
#        # Thickness of frame (1 mm)
#        self.set_line_width(0)
#        # Title
#        self.cell(w, 9, title, 1, 1, 'C', 1)
#        # Line break
#        self.ln(10)
    

# -----------------------------------------------------------------------------------------------
# Define Document metadata
pdf = FPDF()  
pdf.add_page()
pdf.set_xy(0, 0)
pdf.set_author('NSW-IMOS')  
pdf.set_title(title)  

# -----------------------------------------------------------------------------------------------
# Add content to body of document

pdf.set_font('Helvetica', 'B', 28)
pdf.cell(200, 10, title, 0, 2, 'C')      
pdf.set_font('Helvetica', 'B', 20)
pdf.cell(200, 10, deployment_info, 0, 2, 'C')       


# image example
pdf.image('/Users/Michael/Documents/Work/UNSW/Work/QC_reports/Mooring_diagrams/example.png', x = 30, y = 50, w = 0, h = 100, type = 'PNG')


pdf.output('test.pdf', 'F')
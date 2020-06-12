#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun  4 13:42:02 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au


# %% -----------------------------------------------------------------------------------------------
# Import packages

from fpdf import FPDF
import fpdf
import os
import QCreport_paths as paths

# %% -----------------------------------------------------------------------------------------------
# Create title

title = paths.site_name + '  |  ' + paths.deployment + '  |  Quality Control Report'
title_1 = paths.site_name + ' Deployment ' + paths.deployment
title_2 = 'Quality Control Report'

# %% -----------------------------------------------------------------------------------------------
# define format of report

report = FPDF()  

def format_doc(name_of_reportmaker):
    report.set_xy(0, 0)
    report.set_author('NSW-IMOS | ' + name_of_reportmaker)
    report.set_margins(10,10)
    report.set_keywords('QC, report')
    report.set_font('Helvetica',size=14)
    report.set_title(title)
    return report

def section_header(header_string):
    report.set_font('Helvetica', size=22, style ='B')
    report.cell(200, 10, header_string, 0, 2, 'l') 
    report.ln(3)
    add_line()
    return report

def sub_header(header_string):
    report.ln(12)
    report.set_font('Helvetica', size=18, style ='B')
    report.cell(200, 10, header_string, 0, 2, 'l') 
    return report

def add_line():
    report.cell(100, 10, border='T') 
    report.ln(5)
    return report

def add_space():
    report.ln(5)
    return report

def TOC(TOC_string,TOC_ID):
    report.set_font_size(14)
    report.write(5, TOC_string,TOC_ID) 
    report.ln(10)    
    return report

# %% -----------------------------------------------------------------------------------------------
# get bullet points
fpdf.set_global("SYSTEM_TTFONTS", '/Users/Michael/Documents/Work/UNSW/Work/QC_reports/Code/Fonts/NotoSans-unhinted/')
report.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)    

def bullet_point(bullet_text):
    
    s = str('\u2022')
    report.set_font("NotoSans", size=16)
    report.cell(180,8,s + '   ' + bullet_text,0,0,'L');   

def bullet_point_multi(bullet_text,font_size):
    
    s = str('\u2022')
    report.set_font("NotoSans", size=font_size)
    report.multi_cell(180,5,s + '   ' + bullet_text,0,0,'L');   





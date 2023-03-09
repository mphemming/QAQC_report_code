#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun  4 13:42:02 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au


# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Python Packages
# QC report modules
import QCreport_setup as setup
from pylatex import Document, Section, Hyperref, Subsection, Subsubsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Enumerate, Itemize, Command, Package, NoEscape, \
        StandAloneGraphic, MultiColumn, NewPage, TextColor
from pylatex.utils import escape_latex, NoEscape       
from pylatex.base_classes import Environment 
#------------------------------------------------------------
# Information 
#-------------

# These are the Python and QC report modules required to run 
# this script. The python modules should be installed using 
# 'pip/condo install', the QCreport modules need to be in 
# the same folder as this script.

#------------------------------------------------------------

# %% -----------------------------------------------------------------------------------------------
# Create title
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

title = setup.site_name + '  |  ' + setup.deployment + '  |  Quality Control Report'
title_1 = setup.site_name + ' Deployment ' + setup.deployment
title_2 = 'Quality Control Report'

# %% -----------------------------------------------------------------------------------------------
# define format of report
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


def title_header(doc,title_string):
    doc.create(Section(title_string))
    return doc  

def section_header(header_string):
    doc.create(Subsection(header_string))
    return doc

def sub_header(header_string):
    doc.create(Subsubsection(header_string))
    return doc

def hyperlink(url,text):
        text = escape_latex(text)
        return NoEscape(r'\href{' + url + '}{' + text + '}')

# def add_line():
#     report.cell(100, 10, border='T') 
#     report.ln(5)
#     return report

# def add_space():
#     report.ln(5)
#     return report

def TOC():
    doc.create('\tableofcontents')
    return doc

def noindent():
    doc.create('\tableofcontents')
    return doc

class Appendix(Environment):
    """A class representing the appendix environment."""

    _latex_name = 'appendix'

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
    
# %% -----------------------------------------------------------------------------------------------
# get bullet points
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
    
def bullet_point(doc,bullet_text):
    doc.create(Enumerate(enumeration_symbol='*'))
    doc.create(Enumerate.add_item(bullet_text))
    return doc

# def bullet_point_multi(bullet_text,font_size):
    
#     s = str('\u2022')
#     report.set_font("NotoSans", size=font_size)
#     report.multi_cell(180,5,s + '   ' + bullet_text,0,0,'L');   

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Special characters

degree_symbol = u'\N{DEGREE SIGN}'
vel_units = 'm s¯¹'
O2_units = 'µmol kg¯¹'
chl_units = 'mg m¯³'
turb_units = 'NTU'

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Add page numbers

# class MyFPDFClass(FPDF):
# 	def __init__(this, orientation='P',unit='mm',format='A4'):
# 		self.isCover = False
#         # Override add_page methode
# 	def add_page(this,  same= True, orientation='', isCover= False):
# 		FPDF.add_page(self, same= same, orientation=orientation)

#     # Override footer method
# 	def footer(self):
#          # Page number with condition isCover
#          self.set_y(-15)
#          if self.isCover == False:
#             self.cell(0,10, 'Page  ' + str(self.page_no) + '  |  {nb}', 0, 0, 'C')
        
    




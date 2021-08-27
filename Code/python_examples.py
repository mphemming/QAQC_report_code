#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:38:15 2020

@author: Michael
"""

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


title = 'PH100 Quality Control Report'


class report(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)
        
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name) 
        
    def print_deployment(self, name):
        self.chapter_body(name)         
        
    
pdf = report()
pdf.set_title(title)
pdf.set_author('NSW-IMOS')    
pdf.print_deployment('/Users/Michael/Documents/Work/UNSW/Work/QC_reports/text_files/Deployment.txt')
pdf.cell(60,10)
pdf.cell(40, 10, 'Hello World!')
pdf.print_deployment('/Users/Michael/Documents/Work/UNSW/Work/QC_reports/text_files/Deployment.txt')
#pdf.print_chapter(1, 'A RUNAWAY REEF', '20k_c1.txt')
#pdf.print_chapter(2, 'THE PROS AND CONS', '20k_c2.txt')
    
pdf.output('test.pdf', 'F')


#df = pd.DataFrame()
#df['Question'] = ["Q1", "Q2", "Q3", "Q4"]
#df['Charles'] = [3, 4, 5, 3]
#df['Mike'] = [3, 3, 4, 4]
#
#title("Professor Criss's Ratings by Users")
#xlabel('Question Number')
#ylabel('Score')
#
#c = [2.0, 4.0, 6.0, 8.0]
#m = [x - 0.5 for x in c]
#
#xticks(c, df['Question'])
#
#bar(m, df['Mike'], width=0.5, color="#91eb87", label="Mike")
#bar(c, df['Charles'], width=0.5, color="#eb879c", label="Charles")
#
#legend()
#axis([0, 10, 0, 8])
#savefig('barchart.png')

#pdf = FPDF()
#pdf.add_page()
#pdf.set_xy(0, 0)
#pdf.set_font('arial', 'B', 28)
#pdf.cell(60)
#pdf.cell(75, 10, "PH100 Data Quality Report", 0, 2, 'C')
#pdf.cell(60)



#pdf.cell(90, 10, " ", 0, 2, 'C')
#pdf.cell(-40)
#pdf.cell(50, 10, 'Question', 1, 0, 'C')
#pdf.cell(40, 10, 'Charles', 1, 0, 'C')
#pdf.cell(40, 10, 'Mike', 1, 2, 'C')
#pdf.cell(-90)
#pdf.set_font('arial', '', 12)
#for i in range(0, len(df)):
#    pdf.cell(50, 10, '%s' % (df['Question'].iloc[i]), 1, 0, 'C')
#    pdf.cell(40, 10, '%s' % (str(df.Mike.iloc[i])), 1, 0, 'C')
#    pdf.cell(40, 10, '%s' % (str(df.Charles.iloc[i])), 1, 2, 'C')
#    pdf.cell(-90)
#pdf.cell(90, 10, " ", 0, 2, 'C')
#pdf.cell(-30)
#pdf.image('barchart.png', x = None, y = None, w = 0, h = 0, type = '', link = '')





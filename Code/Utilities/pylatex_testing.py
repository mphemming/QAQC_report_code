# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 10:51:10 2021

@author: mphem
"""

import QCreport_paths as paths
import QCreport_format as form

# %%--------------------------------------
# functions

def generate_cover(doc):
		"""
		Generate a cover for generate_info_report func
		Cover contains name, date and branch info
		:param doc: a Document Class instance
		:return: null
		"""

		## Convert in default command of LaTeX to make title
		## \title{}
		## \author{}
		## \date{}
		doc.preamble.append(form.Command('title', 'RiMEA-Projekt Analyse'))
		doc.preamble.append(form.Command('author', 'me'))
		doc.preamble.append(form.Command('date', 'today'))

		## Use titling package to add line on title
		doc.packages.append(form.Package('titling'))

		branch = r"\begin{center}Branch: \par"
		doc.preamble.append(form.Command('predate', form.NoEscape(branch)))

		commit = r"\par commit: \par\end{center}"
		doc.preamble.append(form.Command('postdate', form.NoEscape(commit)))

		doc.append(form.NoEscape(r'\maketitle'))


# %%--------------------------------------
# create simple doc

geometry_options = {"tmargin": "2cm", "lmargin": "2cm"}
doc = form.Document(geometry_options=geometry_options)

# Latex packages
doc.packages.append(form.Package('rotating'))

# front page
generate_cover(doc)

# new page
doc.append(form.Command('newpage'))

# table of contents
doc.append(form.Command('tableofcontents'))

    
# for this to work need Perl and latexmk installed on computer

with doc.create(form.Itemize()) as itemize:
    itemize.add_item("the first item")
    itemize.add_item("the second item")
    itemize.add_item("the third etc")
    # you can append to existing items
    
with doc.create(form.Tabular('rc|cl')) as table:
    table.add_hline()
    table.add_row((1, 2, 3, 4))
    table.add_hline(1, 2)
    table.add_empty_row()
    table.add_row((4, 5, 6, 7))   

# form.title_header(doc,'using the function')

with doc.create(form.Section('A Section')):
        doc.append('Some regular text and some')
        
with doc.create(form.Section('another section')):
    doc.append('Some regular text and some')
with doc.create(form.Subsection('another section')):
    doc.append('Some regular text and some') 


doc.append(form.Command('begin','sidewaystable'))
# doc.append(form.Command('begin','turn'))
# doc.append(form.Command('includegraphics',None,'scale=0.7',('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\Toolbox_Plots' +
#                '\\IMOS_ANMN-NSW_BMP070_FV01_BMP070-1911_CHECK_DEPTH_vs_NOMINAL' +
#                '_DEPTH_C-20200430T063316Z.png')))
file = ('C:/Users/mphem/Documents/Work/UNSW/QC_reports/Toolbox_Plots' +
                '/IMOS_ANMN-NSW_BMP070_FV01_BMP070-1911_CHECK_DEPTH_vs_NOMINAL' +
                '_DEPTH_C-20200430T063316Z.png')
doc.append(form.StandAloneGraphic(file,'scale=0.4'))
doc.append(form.Command('caption',file))
# doc.append(form.Command('end','turn'))
doc.append(form.Command('end','sidewaystable'))


doc.generate_pdf(paths.savedir() + 'test',compiler='pdflatex')








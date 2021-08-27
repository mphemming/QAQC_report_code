
# %% -----------------------------------------------------------------------------------------------
# Import modules

# QCreport modules
import QCreport_paths as paths
import PyPDF2
import numpy as np

# %% -----------------------------------------------------------------------------------------------
# Code

PDF_PATH = paths.savedir() + 'BMP070_29_QC_report.pdf'
OUTPUT_PATH = paths.savedir() + 'test.pdf'

pdf_reader = PyPDF2.PdfFileReader(open(PDF_PATH, 'rb'))
pdf_writer = PyPDF2.PdfFileWriter()

PDF_START_PAGE = 1
PDF_END_PAGE = pdf_reader.getNumPages()

# pages = list(range(PDF_START_PAGE-1, PDF_END_PAGE+1))
# pages[0], pages[-1] = pages[-1], pages[0]


# pages = list(range(1,PDF_END_PAGE-1))

pa = np.array([0,1,PDF_END_PAGE])
pb = np.array(range(3,PDF_END_PAGE-1))

pages = np.concatenate([pa,pb])

for page in range(PDF_END_PAGE):
    
    p = page   
    if page == 2:
        p = PDF_END_PAGE-1
    if page > 2:
        p = page-1
        
    pdf_writer.addPage(pdf_reader.getPage(p))        

    with open(OUTPUT_PATH, 'wb') as o:
        pdf_writer.write(o)
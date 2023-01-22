
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Tue Jan  10 16:56 2023
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS), Neil Malan (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Creates reports for all sites and deployments

# Instructions:

# o   To complete later..

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Import modules

import runpy
import os
import glob

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Create the reports using a loop

sites = ['BMP070','BMP090','BMP120','SYD140','SYD100','PH100','ORS065','CH050','CH070','CH100']

# account = 'z3526971'
account = 'mphem'
path = 'C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\'
os.chdir(path)


for s in sites:
    # get file identifiers for this site (based on `TEMPERATURE')
    files_avail = glob.glob('Z:\\home\\z3526971\\' + 
                            'sci-maths-ocean\\IMOS\\DATA\\MOORINGS\\PROCESSED_2_5\\' + s + 
                            '\\TEMPERATURE\\*.nc')
    depnumbs = []
    for ndeps in range(4,40):
        f = files_avail[ndeps].find('-Aqualogger')
        depnumbs.append(files_avail[ndeps][f-4:f])
        # # Load in the setup script as a string
        # with open('QCreport_setup.py', 'r') as f:
        #     # Read the contents of the file into a string
        #     script = f.read()
        # # edit the site and deployment identifier for code execution
        # script = script.replace("site_name = ''","site_name = " + "'" + s + "'")
        # script = script.replace("deployment_file_date_identifier = ''",
        #                "deployment_file_date_identifier = " + "'" + depnumbs[ndeps] + "'")
        print('--------------------------')
        print(s + '   |   ' + depnumbs[ndeps])
        print('--------------------------')
        print('Editing setup script .....')
        print('--------------------------')
        edited = open(path + 'QCreport_setup.py', 'a')
        edited.write("site_name = " + "'" + s + "'; \n")
        edited.write("deployment_file_date_identifier = " + "'" + depnumbs[ndeps] + "'; \n")
        edited.write("print(site_name + '   |   ' + deployment_file_date_identifier)")
        edited.close()

        print('--------------------------')
        print('Creating report ..........')
        print('--------------------------')
        #run QC report code
        os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code')
        runpy.run_path('QCreport.py')

        print('--------------------------')
        print('Deleting edits ...........')
        print('--------------------------')
        # delete lines in python script ready for next time
        # list to store file lines
        lines = []
        # read file
        with open(path + "QCreport_setup.py", 'r') as fp:
            # read an store all lines into list
            lines = fp.readlines()
        # Write file
        with open(path + r"QCreport_setup.py", 'w') as fp:
            # iterate each line
            for number, line in enumerate(lines):
                # delete line 5 and 8. or pass any Nth line you want to remove
                # note list index starts from 0
                n_lines = len(lines)
                if number not in [n_lines-3,n_lines-2,n_lines-1]:
                    fp.write(line)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# Code to Create automatic QAQC reports
 
### Installation Steps

1) Install Anaconda here: https://www.anaconda.com/products/distribution
2) Install these Python packages using conda:
   * pylatex (https://jeltef.github.io/PyLaTeX/current/)
   * fpdf (https://pyfpdf.readthedocs.io/en/latest/)
   * aodntools (https://github.com/aodn/python-aodntools)
   * numpy (https://numpy.org/install/)
   * pandas (https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
   * xarray (https://docs.xarray.dev/en/stable/getting-started-guide/installing.html)
   * netcdf4 (https://anaconda.org/anaconda/netcdf4)
   * matplotlib (https://anaconda.org/conda-forge/matplotlib)
3) Download this repository to a local directory (TO DO: NEED TO ENSURE THIS REPOSITORY IS READY TO GO)
4) Run setup_check.py to check if everything is ready (TO CREATE). The .py script when run will output which packages are missing or whether everything is installed correctly. 


### How to run

Before running, you will need:
* Python and packages installed (see above)
* The repository files stored locally
* Access to sci-maths-ocean (You may need to run 'network' to mount sci-maths-ocean')

Steps:

1) Open 'QC_report_paths.py' either using a text editor (e.g. emacs or vi) or python (e.g. Spyder). Check that the paths are correct, and edit if necessary. 
2) Open 'QCreport_setup.py' similarly to step (1). Here, choose the site, deployment, deployment ID, and add your name as report maker. Below add any comments relating to the deployment. 
3) Ensure that toolbox plots are in 'sci-maths-ocean\IMOS\Moorings_Report\Automatic_reporting\Toolbox_Plots\<Site_name>\<dep_number>\'. 
4) Ensure that deployment photographs are in 'sci-maths-ocean\IMOS\Moorings_Report\Automatic_reporting\Deployment_Photographs\<Site_name>\<dep_number>\'.
5) In the terminal write 'blah blah blah'. The code should now produce a QAQC report, deployment figures, and output data files. 

### How the code works

#### QCreport.py

This is the main script to run. It imports all functions required to create a mooring deployment report. Functions are imported from scripts that work similarly to imported python packages. However, unlike python packages, the current path needs to be the same as the script that is being imported. That is why the python package OS is used to change directory to that storing the code. 

QCreport.py imports the following 'packages':

* **QCreport_setup.py** - Contains setup information (e.g. site name, deployment). This package is always reloaded to aid creating multiple QC reports in a loop. 
* **QCreport_format.py** - Contains formatting functions (e.g. subheader, hyperlinks). 
* **QCreport_paths.py** - Contains the paths for data, code, plots, and where to save the reports.
* **QCreport_DeploymentDetails.py** - Contains functions that grab file attributes and presents information as LaTeX tables and text. 
* **QCreport_QualityControl.py** - Contains functions to transfer quality control information from the files to the report. 
* **QCreport_DeploymentPhotographs.py** - Contains functions to add deployment photographs to the report, if available. 
* **QCreport_ToolboxPlots.py** - Contains functions to add plots produced during the toolbox QC process to the report. 
* **QCreport_cover.py** - Contains functions that create the report cover. 
* **QCreport_AdditionalPlots** - Contains functions to add additionally created plots (e.g. climatology, OceanCurrents) to the report, if available.

These 'packages' are described in more detail below:

#### QCreport_setup.py (imported as 'setup')

This script contains setup information used to create the report. Please ensure that 'site_name' and 'deployment_file_date_identifier' is correctly defined, and add any comments (e.g. QC comments) here to be included in the report. 

#### QCreport_format.py (imported as 'form')

Pylatex is imported in this 'package' and is vital for creating the report. Functions to create document items (e.g. table of contents, bullet points, sections) are contained here. Special characters, such as the degree symbol, are edited in this script.

#### QCreport_paths.py (imported as 'paths')

Paths are imported from this 'package'. These are retrieved in the main 'QCreport.py' script as follows: 

* toolbox_dir = paths.tb_dir 
* saving_dir = paths.savedir()
* mooring_dir = paths.md_dir
* depphoto_dir = paths.dpp_dir

The report maker needs to double-check that these paths are correct before proceeding to make a report. 

#### QCreport_DeploymentDetails.py (imported as 'DepDet')

#### QCreport_QualityControl.py (imported as 'QCR')

#### QCreport_DeploymentPhotographs.py (imported as 'DepPhoto')

#### QCreport_ToolboxPlots.py (imported as 'tbp')

#### QCreport_cover.py (imported as 'cover')

#### QCreport_AdditionalPlots.py (imported as 'Addp')

The code first creates LTSP files using all available mooring files. The hourly LTSP is then used for creating the plot_period and plot_deployment figures, and other useful figures used for the report. Other useful files and statistics are then output, and a QAQC report PDF is created. 

The code relies on the aodntools package to create the LTSPs, xarray, numpy, and matplotlib to create figures, and pylatex and fpdf packages to create the report.

### Github

The working directory for my personal Github repository is: 'C:\Users\mphem\OneDrive - UNSW\Work\QC_reports\Code'. There is also a UNSW Maths Github repository that will not be updated, stored in 'C:\Users\mphem\OneDrive - UNSW\Work\QC_reports\QC_reports_Github_UNSW'. I will work on branches for the different report versions (e.g. 'version1','version2'). 


#### Directories of output:

* QAQC report:
* Figures:
* Files

### Tips

If you add your email address to the .py file in step (2) in 'How to run' you will receive an email that the report has been created, a list of directories for the data and figures, and the latest statistics. (TO DO LATER)

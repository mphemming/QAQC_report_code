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
* **QCreport_CreateReports** - Contains functions to create multiple reports, useful for historical deployments.

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

Attributes are obtained from the mooring NetCDF files and concatenated in this 'package'. The attributes are then displayed as tables in the report, including useful deployment information and variables available. Instrument serial numbers and there nominal depths are also displayed.

#### QCreport_QualityControl.py (imported as 'QCR')

QC comments/history are copied into the report using this 'package'. These also include the QC comments included in the setup 'package'.

#### QCreport_DeploymentPhotographs.py (imported as 'DepPhoto')

This is a simple 'package' that loads all deployment photographs available in the path (depphoto_dir) defined in 'QCreport_paths.py' into the report. Only works if deployment photographs are available - many deployments do not have photographs. Loads all photographs in a folder, hence no filtering.  

#### QCreport_ToolboxPlots.py (imported as 'tbp')

This 'package' loads all toolbox plots available in the path (toolbox_dir) defined in 'QCreport_paths.py' into the report. These plots are displayed in sideways mode to fit onto the page.

#### QCreport_cover.py (imported as 'cover')

This 'package' creates the report cover. 

#### QCreport_AdditionalPlots.py (imported as 'Addp')

The code first creates LTSP files using all available mooring files. The hourly LTSP is then used for creating the plot_period and plot_deployment figures, and other useful figures used for the report. Other useful files and statistics are then output, and a QAQC report PDF is created. 

The code relies on the aodntools package to create the LTSPs, xarray, numpy, and matplotlib to create figures, and pylatex and fpdf packages to create the report.

#### QCreport_CreateReports.py

This 'package' essentially runs 'QCreport.py' but first changes the site name and deployment identifier number in 'QCreport_setup.py' within a loop. Hence, multiple reports can be created. It does this by loading in text from 'QCreport_setup.py' as a variable and replacing key text, saving, before then running the code. 

### Other Useful Code


### How the LTSPs are updated

LTSPs = Long Time Series Products

The LTSPs are stored on the server, but the code crashes when trying to work with these files due to their location. Hence, the first thing the QAQC report code does is transfer these files to a temporary folder stored locally. This is done in 'QCreport_checkLTSPs.py', which also determines LTSPs that need updating. LTSPs transferred to the temporary folder are updated if necessary, used for plots for the report, and then transferred back to the server. Older Server LTSPs are then deleted. 

For the aggregated and gridded products, the new data is used to create new products and then concatenated with the initial LTSPs. For the hourly product, it is updated from scratch everytime. TEMP, PSAL, and velocity is updated for the gridded and aggregated products, but all variables are updated for the hourly product. 

#### Main LTSP scripts

* QCreport_checkLTSPs.py
* LTSP_functions.py
* CreateLTSPs.py
* CreateVelGridded.py
* code stored in 'code/LTSPs' and 'Code\LTSPs\python-aodntools-master\aodntools\timeseries_products'

### Environment

The packages used for development can be found in 'requirements.txt'. A Conda environment called 'QAQC' was created and used that includes these packages. 

### Github

The working directory for my personal Github repository is: 'C:\Users\mphem\OneDrive - UNSW\Work\QC_reports\Code'. There is also a UNSW Maths Github repository that will not be updated, stored in 'C:\Users\mphem\OneDrive - UNSW\Work\QC_reports\QC_reports_Github_UNSW'. I will work on branches for the different report versions (e.g. 'version1','version2'). 


#### Directories of output:

* QAQC report:
* Figures:
* Files

### Tips

If you add your email address to the .py file in step (2) in 'How to run' you will receive an email that the report has been created, a list of directories for the data and figures, and the latest statistics. (TO DO LATER)

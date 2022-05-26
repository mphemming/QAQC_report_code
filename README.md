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
* Access to sci-maths-ocean 

Steps:

1) Open 'QC_report_paths.py' either using a text editor (e.g. emacs of vi) or python (e.g. Spyder). Check that the paths are correct, and edit if necessary. 
2) Open 'QCreport_setup.py' similarly to step (1). Here, choose the site, deployment, deployment ID, and add your name as report maker. Below add any comments relating to the deployment. 
3) Ensure that toolbox plots are in 'path here'. 
4) Ensure that seployment photographs are in 'path here'.
5) In the terminal write 'blah blah blah'. The code should now produce a QAQC report, deployment figures, and output data files. 

### How the code works

The code first creates LTSP files using all available mooring files. The hourly LTSP is then used for creating the plot_period and plot_deployment figures, and other useful figures used for the report. Other useful files and statistics are then output, and a QAQC report PDF is created. 

The code relies on the aodntools package to create the LTSPs, xarray, numpy, and matplotlib to create figures, and pylatex and fpdf packages to create the report.

#### Directories of output:

* QAQC report:
* Figures:
* Files

### Tips

If you add your email address to the .py file in step (2) in 'How to run' you will receive an email that the report has been created, a list of directories for the data and figures, and the latest statistics. (TO DO LATER)

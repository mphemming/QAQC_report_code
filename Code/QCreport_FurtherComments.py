# -*- coding: utf-8 -*-

# Created on Fri Jun 12 13:41:11 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Further Comments

# %% -----------------------------------------------------------------------------------------------
# Import packages


# %% -----------------------------------------------------------------------------------------------
# further comments

# tips
# Only use characters in 'latin-q' codec
# e.g. commas copied over from somewhere else may be different to commas in latin-1
# use '' instead

comments = 'Post deployment processing of the data identified significant pressure drift in the top PT logger ' + \
            '(PT8 - Nominally 12m depth, 62m above the bottom). Closer inspection indicates a 0.24m ' + \
            'offset between PT8 (0.117m) and PT7 (0.357m - similar with the other PT sensors) ' + \
            'prior to the instruments being deployed. It also indicates that once deployed, PT7 (21.29m) and PT8 (14.70m) are ' + \
            'actually only separated by 6.59m not the nominal 8m. Inspection of the mooring line indicates that some shrinkage has ' + \
            'occurred and that the loggers were separated by 7m (all other logger positions confirmed to be within spec). Deployment ' + \
            'logs and metadata have been amended accordingly.'




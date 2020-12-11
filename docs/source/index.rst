Welcome to Reduction Pipeline's documentation!
=============================================================
This code was developed in order to reduce data taken by the PESTO imager located a l'Obervatoire de Mont Mégantic (OMM) in Québec. This code is not affiliated with OMM. 

Please use and change this code to fit your specific needs. 

To run the code, please edit the example.i file. Then run the following command:

`python reductionPipeline.py example.i`

The input file takes the following arguments:
    1. home_dir (str): Path (absolute or relative) to the data repo; e.x. '/home/user/OMM/200xxx'

    2. dome_dir (str): Relative path to the dome flats wrt to home_dir; e.x. 'DomeFlat'

    3. target_dir (str): Relative path to the target directory wrt home_dir; e.x. 'Target/M33'

    4. filter (str): Filter name (can be found in header of targets); e.x. "Ha'"

    5. pos_dil (str): Dilimeter for position repository names; e.x. '_pos'

    6. output0_dir (str): Path (absolute or relative) to the output repo; e.x. '/home/user/OMM/200xxx/Outputs'

    7. num_pos (str): Number of positions taken; e.x. 3

    8. api_key (str): Astronomy.net API key


The code works by executing the following steps on each pointing (or position):

    1. Generate Folders for each filter taken
    
    2. Subtracts bias from dome flats and science images
    
    3. Calculate the normalized master dome flat
    
    4. Apply normalized master dome flat to science image
    
    5. Align images using phase cross-correlator
    
    6. Apply astrometric corrections using astrometry.net
    
Unforunately, the astrometric corrections do not always pass. If this is the case, I suggest you follow the instructions in the FinalAlignment.ipynb notebook to manually calculate the correct astrometry. Although this is more manual, it is still highly automated :) 

Pipeline
^^^^^^^^


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   pipeline


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

The software is protected under the :ref:`license`.

If you have any questions, please message me at carter.rhea@umontreal.ca

We acknowledge the work done by Amanda Townsend on the stacking and cleaning portion of the code.

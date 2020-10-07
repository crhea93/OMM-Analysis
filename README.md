OMM-Analysis

The code in this repository was designed to analyse observations taken by the instrument PESTO
located at l'Observatoire de Mont Mégantic.

The code will collect all flats, biases, and target fits files, generate a master
bias and flat, apply them to the science images, align and stack science images.

The output is a series of png images (master flat, master bias, unaligned science image,
  aligned science image).

Before running the code, be sure to have unzipped all Target and DomeFlats. You can
go to their directories and type `gunzip *` to unzip the files. Additionally,
the bias.fits file must be in the home directory!

Simple change the imports at the beginning of the file: sort_filters.py and Clean-and-Stack.py and mosaic.py

to run simply type:
1 - python sort_filters.py
2 - python Clean-and-Stack.py
3 - python mosaic.py

I have created a number of additional Clean-and-Stack files for specific galaxies.
Sometimes, astrometry.net fails to solve for the coordinates for certain tiles in a mosaic. If this
is the case, the code will not create the *corrected* fits files. To create the corrected fits files, use the FinalAlignment.ipynb to manually align and calculate the coordinates :P

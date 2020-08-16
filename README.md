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

Simple change the imports at the beginning of the file: Clean-and-Stack.py

to run simply type: python Clean-and-Stack.py

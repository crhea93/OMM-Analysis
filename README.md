OMM-Analysis

The code in this repository was designed to analyse observations taken by the instrument PESTO
located at l'Observatoire de Mont Mégantic.

The code will collect all flats, biases, and target fits files, generate a master
bias and flat, apply them to the science images, align and stack science images.

The output is a series of png images (master flat, master bias, unaligned science image,
  aligned science image).

Simple change the imports at the beginning of the file: Clean-and-Stack.py

to run simply type: python Clean-and-Stack.py 
.. _example:

Example Pipeline
================

In this example we will go through how to reduce, clean, and combine images taken by the PESTO instrument.


We are going to assume that we have the data downloaded already (if you are interested in this step please write me!).

We will be reducing the data for Arp 94 which has images taken in the Halpha, g, and i bands.

Let's start with Halpha since the others will be nearly identical.

First we need to create an input file

.. code-block::

  home_dir = /export/carterrhea/OMM-Data/210413
  dome_dir = DomeFlat
  target_dir = Target/Arp94
  filter_ = Ha
  pos_dil = _pos
  output_dir = /export/carterrhea/Arp94/Ha
  num_pos = 5
  api_key = vyihgprfjfltyhvv

**Now let's break this down.**

The data is in a directory called '/export/carterrhea/OMM-Data/210413'. Inside this directory,
 the dome flats are in a directory called 'DomeFlat' and the target images are in 'Target/Arp94'.

 Now there may be several filters so we set `filter_ = Ha`. Finally, we know that there are
 5 positions taken for this observation.

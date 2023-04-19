"""
Routine to mosaic images
"""
import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from read_input import read_input_file
from reproject import reproject_interp, reproject_adaptive
from reproject.mosaicking import reproject_and_coadd
from reproject.mosaicking import find_optimal_celestial_wcs
#----------------------------INPUTS-------------------------------#

#-----------------------------------------------------------------#
def mosaic(sys_arg, weights):
    os.chdir('../..')
    inputs = read_input_file(sys_arg)
    name = inputs['target_dir'].split('/')[-1]
    sci_dir = inputs['output_dir']#+'/'+name+'/'+inputs['filter_']
    sci_hdus = []  # List of science images
    sci_weights = []  # List of weights for mosaicing
    for filename in os.listdir(sci_dir):
        if filename.endswith('.fits') and filename.startswith('stacked_correct'):
            hdu = fits.open(sci_dir+'/'+filename)
            sci_hdus.append(hdu)
            weights = fits.open(sci_dir+'/master_flat.fits')[0].data
            weights = np.array(weights)
            sci_weights.append(weights)
    if len(sci_hdus) > 1:

        print("#-----Calculaing WCS-----#")
        wcs_out, shape_out = find_optimal_celestial_wcs(sci_hdus, auto_rotate=True)
        print("#-----Reprojecting-----#")

        array, footprint = reproject_and_coadd(sci_hdus,
            wcs_out, shape_out=shape_out,
            reproject_function=reproject_adaptive,
            match_background=True,
            combine_function='mean',
            input_weights=sci_weights)
        print("#-----Making Image-----#")
        plt.figure(figsize=(10, 8))
        ax1 = plt.subplot(1, 2, 1)
        im1 = ax1.imshow(np.log10(array), origin='lower', vmin=np.min(np.log10(array)), vmax=np.percentile(np.log10(array), 99.5))
        ax1.set_title('Mosaic')
        ax2 = plt.subplot(1, 2, 2)
        im2 = ax2.imshow(footprint, origin='lower')
        ax2.set_title('Footprint')
        plt.savefig(sci_dir+'/mosaic.png')
        print('#-----Making Fits-----#')
        hdu = fits.PrimaryHDU(header=wcs_out.to_header(), data=array)
        hdul = fits.HDUList([hdu])
        hdul.writeto(sci_dir+'/'+name+'_'+inputs['filter_']+'.fits', overwrite=True)
    else:
        print("There is only one image so there is no need to make a mosaic")

    

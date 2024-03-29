"""
Routine to mosaic images
"""
import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from reproject import reproject_interp
from reproject.mosaicking import reproject_and_coadd
from reproject.mosaicking import find_optimal_celestial_wcs
#----------------------------INPUTS-------------------------------#

sci_dir = "/export/carterrhea/"
name = 'SH2-157'
band = 'r'
sci_dir = sci_dir + name + '/'+band+'/'
output_dir = sci_dir
#-----------------------------------------------------------------#
sci_hdus = []  # List of science images
for filename in os.listdir(sci_dir):
    if filename.endswith('.fits') and filename.startswith('stacked_correct'):
        hdu = fits.open(sci_dir+'/'+filename)
        sci_hdus.append(hdu)
print("#-----Calculaing WCS-----#")
wcs_out, shape_out = find_optimal_celestial_wcs(sci_hdus, auto_rotate=True)
print("#-----Reprojecting-----#")
array, footprint = reproject_and_coadd(sci_hdus,
	                               wcs_out, shape_out=shape_out,
	                               reproject_function=reproject_interp,
	                               match_background=True,
	                               combine_function='mean')
print("#-----Making Image-----#")
plt.figure(figsize=(10, 8))
ax1 = plt.subplot(1, 2, 1)
im1 = ax1.imshow(np.log(array), origin='lower', vmin=np.min(np.log(array)), vmax=np.max(np.log(array)))
ax1.set_title('Mosaic')
ax2 = plt.subplot(1, 2, 2)
im2 = ax2.imshow(footprint, origin='lower')
ax2.set_title('Footprint')
plt.savefig(output_dir+'/mosaic.png')

print('#-----Making Fits-----#')
hdu = fits.PrimaryHDU(header=wcs_out.to_header(), data=array)
hdul = fits.HDUList([hdu])
hdul.writeto(output_dir+'/'+name+"_"+band+'.fits', overwrite=True)

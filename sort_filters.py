"""
Python script to sort OMM observations by filter
"""
import os
import shutil
from astropy.io import fits

#---------------------------- Inputs ------------------------------------#
home_dir = '/export/carterrhea/OMM-Data/200815'
target_dir = 'Target/NGC6946_pos6'
#------------------------------------------------------------------------#

# Sort science images by filter


filter_images = {}  # {filter: list of image fits}
for filename in os.listdir(home_dir+'/'+target_dir):  # Step through each fits file
    if filename.endswith('.fits'):  # Only get fits files
        hdu = fits.open(home_dir+'/'+target_dir+'/'+filename)  # Open Fits
        header = hdu[0].header  # Get Header
        filter = header['FILTER']  # Get filter
        if filter in filter_images.keys():  # If we already have the filter in the dictionary
            filter_images[filter].append(filename)  # add to list of filenames with filter
        else:  # filter not in dictionary
            filter_images[filter] = [filename]  # Start list of filenames in filter
print(filter_images.keys())
for filter in filter_images.keys():  # Step through each filter
    # Create new folders for each filter
    try:
        os.mkdir(home_dir+'/'+target_dir+'/'+filter)
    except:
        pass
    for filename in filter_images[filter]:
        shutil.copyfile(home_dir+'/'+target_dir+'/'+filename, home_dir+'/'+target_dir+'/'+filter+'/'+filename)

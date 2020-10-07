import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

import glob
from astropy.io import fits
from scipy.ndimage import interpolation as interp

#from skimage.feature.register_translation import (register_translation, _upsampled_dft)
import skimage.registration as skf
from astroquery.astrometry_net import AstrometryNet

from astropy.wcs import WCS
from astropy import units as u
from astropy.coordinates import Angle
## This turns off warnings: not a great way to code
## But when we show the images, sometimes we're taking the logarithm of zero and it doesn't like that
## Which would matter if we were doing math, but we're just taking a look at images, so we can ignore it.
import warnings
warnings.filterwarnings('ignore')
u.set_enabled_equivalencies(u.dimensionless_angles())
u.deg.to('')
ast = AstrometryNet()
ast.key = 'vyihgprfjfltyhvv'
ast.api_key = 'vyihgprfjfltyhvv'
#---------------------------- Inputs ------------------------------------#
home_dir = '/home/carterrhea/Documents/OMM-Data/180521'
dome_dir = 'Domeflat'
target_dir = 'NGC6995'
filter_ = "g'"
output_dir = '/home/carterrhea/Documents/OMM-Data/NGC6995/'+filter_
#------------------------------------------------------------------------#



os.chdir(home_dir)
for tile_ct in range(0,1):
    print('Tile %i'%(tile_ct+1))

    print('#-----Collecting Data-----#')
    bias_list = glob.glob('bias.fits')


    ## make a list of  flat images:
    flat_list = glob.glob(dome_dir+'/*fits')

    ## make a list of raw science images:
    sci_list = glob.glob(target_dir+'/*fits')


    ## now put all the lists together for a masterlist of all the images:
    all_images_list = bias_list + flat_list + sci_list

    raw_image_data = {}
    for image_name in all_images_list: raw_image_data[image_name] = fits.getdata(image_name)

    ## create an array of bias images
    biascube = np.stack([raw_image_data[bias_frame] for bias_frame in bias_list],axis=0)
    #biascube = biascube[0,:584,:1024]
    #biascube = biascube.reshape(1,584,1024)

    ## create an array of v-flat images
    flatcube = np.stack([raw_image_data[flat_frame] for flat_frame in flat_list],axis=0)

    ## create an array of raw M42 images
    scicube = np.stack([raw_image_data[science_frame] for science_frame in sci_list],axis=0)

    ## create an array of v-flat images
    flatcube = np.stack([raw_image_data[flat_frame] for flat_frame in flat_list],axis=0)

    ## create an array of raw M42 images
    scicube = np.stack([raw_image_data[science_frame] for science_frame in sci_list],axis=0)

    print('#-----Generating Master Bias and Flat-----#')
    master_bias = np.average(biascube, axis=0) ## to combine with an average

    plt.figure(figsize=(15,15))
    plt.imshow(np.log10(master_bias), origin='lower', cmap='gray');
    plt.title('Master Bias')
    plt.savefig(output_dir+'/master_bias_%i.png'%(tile_ct+1))
    plt.clf()

    # filneames of flats and science frames that have not yet been bias-subtracted:
    debias_list_in = sci_list + flat_list

    ## filenames for the corresponding bias-subtracted images:
    debias_list_out = ['debiased_' + im for im in debias_list_in]


    ## subtract the master bias from each of the raw science & flat frames:

    debias_data_out = {} ## dictionary for the debiased images

    for i in range(len(debias_list_in)):
        debias_data_out[debias_list_out[i]] = raw_image_data[debias_list_in[i]] - master_bias


    ## create an array of debiased images
    debiascube = np.stack([debias_data_out[image] for image in debias_list_out],axis=0)


    ## first we need a list of JUST the debiased flat images to work with:
    debias_flat_list = ['debiased_' + image for image in flat_list]

    ## create an array of debiased v-flat images
    flatcube = np.stack([debias_data_out[flat_frame] for flat_frame in debias_flat_list],axis=0)

    ## average the images in the stack
    master_flat = np.average(flatcube, axis=0)

    ## Created normalized master
    normalized_master_flat = master_flat/np.median(master_flat)



    ## normalized master flat:
    plt.figure(figsize=(15,15))
    plt.imshow((normalized_master_flat), origin='lower', cmap='gray', vmin=.95, vmax=1.1)
    plt.title('Normalized Master Flat')
    plt.savefig(output_dir+'/MasterFlat_%i.png'%(tile_ct+1))
    plt.clf()

    ## we'll start with a list of the debiased M42 images:
    debias_sci_list = ['debiased_' + im for im in sci_list]


    ## and we'll make a corresponding list to name the flattened images:
    flat_debias_sci_list = ['flattened_' + im for im in debias_sci_list]

    ## create an empty dictionary to populate with the completely corrected science frames:
    flat_debias_data_out = {}

    ## and populate the dictionary with each corrected image
    ## where the dictionary keys = the images in flat_debias_m42_list
    ## we're iterating over an integer here again because the lists match up
    for i in range(len(debias_sci_list)):
        flat_debias_data_out[flat_debias_sci_list[i]] = \
        debias_data_out[debias_sci_list[i]]/normalized_master_flat

    scicube = np.stack([flat_debias_data_out[science_frame] for science_frame in flat_debias_sci_list],axis=0)

    # Unaligned image
    ## array of images + average combine:
    sci_cube = np.stack(flat_debias_data_out.values(),axis=0)
    sci_stacked = np.average(sci_cube, axis=0)

    ## plotting:
    plt.figure(1);
    plt.figure(figsize=(15,15));
    plt.title('Stacked But Not Aligned');
    plt.imshow(np.log10(sci_stacked), origin='lower', cmap='viridis', vmin=1.5, vmax=3);
    plt.savefig(output_dir+'/Stacked_unaligned_%i.png'%(tile_ct+1))
    plt.clf()


    ## Align images
    print('#-----Aligning Images-----#')
    ## choose an image to define as zero shift:
    zero_shift_image = debias_sci_list[-1]
    hdu = fits.open(sci_list[-1])[0]
    ra = hdu.header['RA']
    dec = hdu.header['DEC']
    header_zero = WCS(fits.open(sci_list[-1])[0].header)
    pixel = Angle(0.459211, u.arcsec)
    header_zero.wcs.crpix = [512, 512] # center pixel

    header_zero.wcs.crval = [hdu.header['RA'], hdu.header['DEC']] # RA and dec values in hours and degrees

    header_zero.wcs.ctype = ["RA", "DEC"]

    header_zero.wcs.cdelt = [pixel.degree, pixel.degree]
    ## find all shifts for other images:
    imshifts = {} # dictionary to hold the x and y shift pairs for each image
    for image in debias_sci_list:
        ## register_translation is a function that calculates shifts by comparing 2-D arrays
        result, error, diffphase = skf.phase_cross_correlation(
            debias_data_out[zero_shift_image],
            debias_data_out[image])
        imshifts[image] = result




    ## new list for shifted image names:
    shifted_sci_list = ['shifted_' + im for im in flat_debias_sci_list]
    ## new dictionary for shifted image data:
    shifted_sci_data = {}
    for i in range(len(shifted_sci_list)):
        shifted_sci_data[shifted_sci_list[i]] = np.roll(debias_data_out[debias_sci_list[i]],
                                                       np.int(np.floor(imshifts[debias_sci_list[i]][0])), axis=0)  # Shift up
        shifted_sci_data[shifted_sci_list[i]] = np.roll(shifted_sci_data[shifted_sci_list[i]],
                                                       np.int(np.floor(imshifts[debias_sci_list[i]][1])), axis=1)  # Shift right


    ## array of aligned arrays:
    scicube  = np.stack(shifted_sci_data.values(),axis=0)

    ## average combined final image:
    sci_stacked = np.average(scicube, axis=0)

    ## show the final image array as an image:
    plt.subplot(projection=header_zero)
    plt.title('Aligned and Stacked');
    plt.imshow(np.log10(sci_stacked), origin='lower', cmap='viridis', vmin=1.5, vmax=3)
    plt.savefig(output_dir+'/Final-image_%i.png'%(tile_ct+1))

    ## Create original fits before astrometry correction
    header = header_zero.to_header()
    hdu = fits.PrimaryHDU(data=sci_stacked)
    hdul = fits.HDUList([hdu])
    hdul.writeto(output_dir+'/stacked_%i.fits'%(tile_ct+1), overwrite=True)

    # Apply Astrometery using astroquery
    try_again = True
    submission_id = None
    print("#-----Astrometric Corrections-----#")
    while try_again:
        if not submission_id:
            try:
                wcs_header = ast.solve_from_image(output_dir+'/stacked_%i.fits'%(tile_ct+1), submission_id=submission_id, solve_timeout=300)#, use_sextractor=True, center_ra=float(ra), center_dec=float(dec))
            except Exception as e:
                print("Timedout")
                submission_id = e.args[1]
            else:
                # got a result, so terminate
                print("Result")
                try_again = False
        else:
            try:
                wcs_header = ast.monitor_submission(submission_id, solve_timeout=300)
            except Exception as e:
                print("Timedout")
                submission_id = e.args[1]
            else:
                # got a result, so terminate
                print("Result")
                try_again = False

    if wcs_header:
        # Code to execute when solve succeeds
        hdu = fits.PrimaryHDU(header=wcs_header, data=sci_stacked)
        hdul = fits.HDUList([hdu])
        hdul.writeto(output_dir+'/stacked_correct_%i.fits'%(tile_ct+1), overwrite=True)

    else:
        # Code to execute when solve fails
        print('BAD ASTROMETRY')

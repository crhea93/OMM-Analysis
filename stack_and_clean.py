import os
import sys
import glob
import numpy as np
from Align import align
from astropy.io import fits
import matplotlib.pyplot as plt
from astrometry import astrometry
from read_input import read_input_file

def stack_and_clean(sys_arg):
    """
    Master routine for cleaning, stacking, and astrometrically correcting images

    This routine assumes that the data are organized by exposure group. For example,
    if there are 3 exposure groups (or positions), the target folder contains three sub-directories
    labeled (in some manner), target_pos1, target_pos2, target_pos3. This format was adopted
    as it is the standard format for OMM PESTO observations. We also assume that the
    bias fits file is in the home directory (home_dir).

    The inputs are read through the input file (.i). The user must supply the following:

    1. home_dir (str): Path (absolute or relative) to the data repo; e.x. '/home/user/OMM/200xxx'

    2. dome_dir (str): Relative path to the dome flats wrt to home_dir; e.x. 'DomeFlat'

    3. target_dir (str): Relative path to the target directory wrt home_dir; e.x. 'Target/M33'

    4. filter (str): Filter name (can be found in header of targets); e.x. "Ha'"

    5. pos_dil (str): Dilimeter for position repository names; e.x. '_pos'

    6. output0_dir (str): Path (absolute or relative) to the output repo; e.x. '/home/user/OMM/200xxx/Outputs'

    7. num_pos (str): Number of positions taken; e.x. 3

    8. api_key (str): Astronomy.net API key

    This code was inspired by a jupyter notebook written by Amanda Townsend which can be found here:
    https://users.astro.ufl.edu/~ajtownsend/OBSTECH_REDUX_2017.html
    """
    # Read in input data
    inputs = read_input_file(sys_arg)
    # Enter home directory
    os.chdir(inputs['home_dir'])
    # Make output directory
    if not os.path.exists(inputs['output_dir']):
        os.makedirs(inputs['output_dir'])
    # Read in bias file
    bias = fits.getdata('bias.fits')
    # We will iterate through each position
    for tile_ct in range(0, int(inputs['num_pos'])):
        print('#-----On Position %i-----#'%tile_ct)
        # Now we need to collect the dome flats and scientific images
        dome_flats = glob.glob(inputs['dome_dir']+'/*fits')
        target_images = glob.glob(inputs['target_dir']+inputs['pos_dil']+str(tile_ct+1)+'/'+inputs['filter_']+'/*fits')
        all_images_list = dome_flats + target_images
        raw_image_data = {}
        for image_name in all_images_list: raw_image_data[image_name] = fits.getdata(image_name)
        ## create an array of v-flat images
        flatcube = np.stack([raw_image_data[flat_frame] for flat_frame in dome_flats],axis=0)
        ## create an array of raw science images
        scicube = np.stack([raw_image_data[science_frame] for science_frame in target_images],axis=0)

        print('  #-----Generating Master Bias and Flat-----#')
        master_bias = bias
        # filneames of flats and science frames that have not yet been bias-subtracted:
        debias_list_in = target_images + dome_flats
        ## filenames for the corresponding bias-subtracted images:
        debias_list_out = [im.strip('.fits') + "_debiased.fits" for im in debias_list_in]
        ## subtract the master bias from each of the raw science & flat frames:
        debias_data_out = {} ## dictionary for the debiased images
        for i in range(len(debias_list_in)):
            debias_data_out[debias_list_out[i]] = raw_image_data[debias_list_in[i]] - master_bias
        ## create an array of debiased images
        debiascube = np.stack([debias_data_out[image] for image in debias_list_out],axis=0)
        ## first we need a list of JUST the debiased flat images to work with:
        debias_flat_list = [image.strip('.fits') + "_debiased.fits" for image in dome_flats]
        ## create an array of debiased v-flat images
        flatcube = np.stack([debias_data_out[flat_frame] for flat_frame in debias_flat_list],axis=0)
        ## average the images in the stack
        master_flat = np.average(flatcube, axis=0)
        ## Created normalized master
        normalized_master_flat = master_flat/np.median(master_flat)
        ## we'll start with a list of the debiased science images:
        debias_sci_list = [im.strip('.fits') + "_debiased.fits" for im in target_images]
        ## and we'll make a corresponding list to name the flattened images:
        flat_debias_sci_list = [im.strip('.fits') + "_flattened.fits" for im in debias_sci_list]
        ## create an empty dictionary to populate with the completely corrected science frames:
        flat_debias_data_out = {}
        for i in range(len(debias_sci_list)):
            flat_debias_data_out[flat_debias_sci_list[i]] = \
            debias_data_out[debias_sci_list[i]]/normalized_master_flat
        scicube = np.stack([flat_debias_data_out[science_frame] for science_frame in flat_debias_sci_list],axis=0)
        # Unaligned image
        ## array of images + average combine:
        sci_cube = np.stack(flat_debias_data_out.values(),axis=0)
        sci_stacked = np.average(sci_cube, axis=0)
        plt.clf()
        ## Align images
        print('  #-----Aligning Images-----#')
        # Choose an image to define as zero shift:
        align(target_images, debias_sci_list, debias_data_out, flat_debias_sci_list, inputs['output_dir'], tile_ct)
        print('  #-----Applying Astrometry-----#')
        # Use astrometry.net to calculate the true wcs
        astrometry(inputs['output_dir'], tile_ct, sci_stacked, inputs['api_key'])

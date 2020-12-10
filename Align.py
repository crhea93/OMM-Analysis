import warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from astropy import units as u
import skimage.registration as skf
from astropy.coordinates import Angle

warnings.filterwarnings('ignore')
u.set_enabled_equivalencies(u.dimensionless_angles())
u.deg.to('')


def align(target_images, debias_sci_list, debias_data_out,flat_debias_sci_list, output_dir, tile_ct):
    """
    Align debiased and master-flat-subtracted science images. We use phase cross-correlation to
    calculate the offset between images. We then apply those offsets using numpy roll.
    Finally, we restack the images (and take their average) to create a final aligned image
    for the position. The output fits is called stacked_%tile_ct.fits

    Args:
        target_images (list): List of science arrays (biased)
        debias_sci_list (list): List of debiased science Data
        debias_data_out (dict): Dictionary of debiased science data
        flat_debias_sci_list (list): List of flat-subtracted, debiased science data
        output_dir (str): Output directory path
        tile_ct (int): Position count

    Returns:
        Creates aligned images using phase cross-correlation
    """
    hdu = fits.open(target_images[-1])[0]  # Choose last unbiased one to get header info
    zero_shift_image = debias_sci_list[-1]
    ra = hdu.header['RA']
    dec = hdu.header['DEC']
    header_zero = WCS(fits.open(target_images[-1])[0].header)
    pixel = Angle(0.459211, u.arcsec)
    header_zero.wcs.crpix = [512, 512] # center pixel
    header_zero.wcs.crval = [hdu.header['RA'], hdu.header['DEC']] # RA and dec values in hours and degrees
    header_zero.wcs.ctype = ["RA", "DEC"]
    header_zero.wcs.cdelt = [pixel.degree, pixel.degree]
    # Find all shifts for other images:
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

    # Create original fits before astrometry correction after alignment
    header = header_zero.to_header()
    hdu = fits.PrimaryHDU(data=sci_stacked)
    hdul = fits.HDUList([hdu])
    hdul.writeto(output_dir+'/stacked_%i.fits'%(tile_ct+1), overwrite=True)

from astroquery.astrometry_net import AstrometryNet
ast = AstrometryNet()


def astrometry(output_dir, tile_ct, sci_stacked, api_key):
    """
    Apply astrometry using astrometry.net

    If the astrometry fails, then you will receive a notice. If that is the case, then
    please use the final alignment notebook to correct the astrometry.

    Args:
        output_dir (str): Path to output
        tile_ct (int): Pointing or position number
        sci_stacked (list): List of stacked science images
        api_key (str): API Key for astrometry.net

    Returns:
        Creates corrected fits files

    Note:
        Requires an astrometry.net account
    """

    ast.key = api_key
    ast.api_key = api_key
    try_again = True
    submission_id = None
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

import os
import shutil
from astropy.io import fits
from read_input import read_input_file


# Sort science images by filter

def sort_filters(sys_arg):
    """
    Python script to sort OMM observations by filter

    Reads in input file containing a home directory and target directory:

    1. home_dir (str): Path (absolute or relative) to the data repo; e.x. '/home/user/OMM/200xxx'

    2. target_dir (str): Relative path to the target directory wrt home_dir; e.x. 'Target/M33'

    3. filter (str): Filter name (can be found in header of targets); e.x. "Ha'"

    4. pos_dil (str): Dilimeter for position repository names; e.x. '_pos'

    5. num_pos (str): Number of positions taken; e.x. 3

    Returns:
        Creates new repos in target directory for each filter
    """
    curr_dir = os.getcwd()
    inputs = read_input_file(sys_arg)
    home_dir = inputs['home_dir']
    target_dir = inputs['target_dir']
    os.chdir(home_dir)
    os.system('gunzip -r *')  # Unzip all zip files if there are any
    for tile_ct in range(0, int(inputs['num_pos'])):
        try:
            filter_images = {}  # {filter: list of image fits}
            if 'central' in inputs['pos_dil']:
                for filename in os.listdir(home_dir+'/'+target_dir+inputs['pos_dil']):  # Step through each fits file
                    if filename.endswith('.fits'):  # Only get fits files
                        hdu = fits.open(home_dir+'/'+target_dir+inputs['pos_dil']+'/'+filename)  # Open Fits
                        header = hdu[0].header  # Get Header
                        try:
                            filter = header['FILTER']  # Get filter
                        except:
                            filter = header['FILTRE']
                        if filter in filter_images.keys():  # If we already have the filter in the dictionary
                            filter_images[filter].append(filename)  # add to list of filenames with filter
                        else:  # filter not in dictionary
                            filter_images[filter] = [filename]  # Start list of filenames in filter
            else:
                for filename in os.listdir(home_dir+'/'+target_dir+inputs['pos_dil']+str(tile_ct+1)):  # Step through each fits file
                    if filename.endswith('.fits'):  # Only get fits files
                        hdu = fits.open(home_dir+'/'+target_dir+inputs['pos_dil']+str(tile_ct+1)+'/'+filename)  # Open Fits
                        header = hdu[0].header  # Get Header
                        try:
                            filter = header['FILTER']  # Get filter
                        except:
                            filter = header['FILTRE']
                        if filter in filter_images.keys():  # If we already have the filter in the dictionary
                            filter_images[filter].append(filename)  # add to list of filenames with filter
                        else:  # filter not in dictionary
                            filter_images[filter] = [filename]  # Start list of filenames in filter
            filters_ = ''
            #print('Filters:')
            for key in filter_images.keys():
                filters_ += key+' '
            print('Position: ' + str(tile_ct+1))
            print('    Filters: ' + filters_)
            # Create target folder
            for filter in filter_images.keys():  # Step through each filter
                # Create new folders for each filter
                if 'central' in inputs['pos_dil']:
                    if os.path.exists(home_dir+'/'+target_dir+inputs['pos_dil']+'/'+filter):
                        pass
                    else:
                        os.mkdir(home_dir+'/'+target_dir+inputs['pos_dil']+'/'+filter)
                    for filename in filter_images[filter]:
                        shutil.copyfile(home_dir+'/'+target_dir+inputs['pos_dil']+'/'+filename, home_dir+'/'+target_dir+inputs['pos_dil']+'/'+inputs['filter_']+'/'+filename)
                else:
                    if os.path.exists(home_dir+'/'+target_dir+inputs['pos_dil']+str(tile_ct+1)+'/'+filter):
                        pass
                    else:
                        os.mkdir(home_dir+'/'+target_dir+inputs['pos_dil']+str(tile_ct+1)+'/'+filter)
                    for filename in filter_images[filter]:
                        shutil.copyfile(home_dir+'/'+target_dir+inputs['pos_dil']+str(tile_ct+1)+'/'+filename, home_dir+'/'+target_dir+inputs['pos_dil']+str(tile_ct+1)+'/'+inputs['filter_']+'/'+filename)
        except:
            pass
        os.chdir(curr_dir)

import sys
import os
from sort_filters import sort_filters
from stack_and_clean import stack_and_clean
from mosaic import mosaic

current_dir = os.getcwd()
# Sort by filter
sort_filters(sys.argv[1])
# Stack and clean the images. Solve for astrometry
stack_and_clean(sys.argv[1])
# Create mosaic
os.chdir(current_dir)
mosaic(sys.argv[1])

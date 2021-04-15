import sys
from sort_filters import sort_filters
from stack_and_clean import stack_and_clean
from mosaic import mosaic

# Sort by filter
sort_filters(sys.argv[1])
# Stack and clean the images. Solve for astrometry
stack_and_clean(sys.argv[1])
# Create mosaic
mosaic(sys.argv[1])

import sys
from sort_filters import sort_filters
from stack_and_clean import stack_and_clean

# Sort by filter
sort_filters(sys.argv[1])
stack_and_clean(sys.argv[1])

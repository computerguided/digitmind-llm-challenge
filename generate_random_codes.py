# -----------------------------------------------------------------------------
# Generate random codes
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import random
import sys
from score_calculators import create_combinations, get_code_as_string

# -----------------------------------------------------------------------------
# Retrieve the number of codes to generate from the second parameter of the 
# command line.
# -----------------------------------------------------------------------------
if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    print("Please provide a number of codes to generate.")
    sys.exit(1)

num_codes = int(sys.argv[1])

# -----------------------------------------------------------------------------
# Generate the codes
# -----------------------------------------------------------------------------
codes = random.sample(create_combinations(), num_codes)

with open('codes.dat', 'w') as file:
    for code in codes:
        file.write(f"{get_code_as_string(code)}")
        # Add a newline character if it's not the last code
        if code != codes[-1]:
            file.write("\n")

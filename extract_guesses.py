import pandas as pd
import re

# -----------------------------------------------------------------------------
# Extract guesses from log file
# -----------------------------------------------------------------------------

# Load the log file
file_path = "log.dat"

# Read the file content
with open(file_path, "r") as file:
    lines = file.readlines()

# Initialize variables
data = []
model = None
code_to_break = None

# Regular expressions to extract data
model_re = re.compile(r"Model:\s*(\S+)")
code_re = re.compile(r"Code to break:\s*(\d+)")
guess_re = re.compile(r"- (\d+) -")
guess_value_re = re.compile(r"Guess:\s*(\d+)[?!]")
combinations_re = re.compile(r"Combinations left:\s*(\d+)")
optimal_guess_re = re.compile(r"Optimal guess:\s*(yes|no)")

# Parse the file
for line in lines:
    model_match = model_re.search(line)
    code_match = code_re.search(line)
    guess_match = guess_re.search(line)
    guess_value_match = guess_value_re.search(line)
    combinations_match = combinations_re.search(line)
    optimal_guess_match = optimal_guess_re.search(line)
    
    if model_match:
        model = model_match.group(1)
    if code_match:
        code_to_break = code_match.group(1)
    if guess_match:
        guess_nr = guess_match.group(1)
    if guess_value_match:
        guess_value = guess_value_match.group(1)
    if optimal_guess_match:
        optimal_guess = optimal_guess_match.group(1)
    if combinations_match:
        combinations_left = combinations_match.group(1)
        data.append([model, code_to_break, guess_nr, guess_value, combinations_left, optimal_guess])

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data, columns=["model", "code", "nr", "guess", "combinations_left", "optimal_guess"])
csv_path = "guesses.csv"
df.to_csv(csv_path, index=False)

# Return CSV path for download
csv_path

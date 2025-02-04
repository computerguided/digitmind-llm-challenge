#imports
from score_calculators import *
from game_result import *
import random

# -----------------------------------------------------------------------------
# Print and log
# -----------------------------------------------------------------------------
def print_and_log(message : str):
    print(message)

# -----------------------------------------------------------------------------
# Game loop
# Return the number of guesses required to break the code
# -----------------------------------------------------------------------------
def do_game(code : list) -> int:
    score_calculator = ScoreCalculator()
    number_of_guesses = 0
    score = Score()

    while not score.right_guess():
        number_of_guesses += 1

        num_combinations_left = len(score_calculator.combinations_left)

        # When there are more than 1 possible combinations left,
        # choose a random combination, not being the code.
        if (num_combinations_left == 1):
            guess = score_calculator.combinations_left[0]
        else:
            # Copy combinations left to guess
            possible_guesses = score_calculator.combinations_left.copy()
            # Remove the code
            possible_guesses.remove(code)
            # Get random guess from possible guesses
            guess = random.choice(possible_guesses)

        score = score_calculator.determine_score(guess, code)
        score_calculator.process_guess(guess, score)

        # Set max combinations left
        if (num_combinations_left > max_combinations_left[number_of_guesses]):
            max_combinations_left[number_of_guesses] = num_combinations_left

    return number_of_guesses

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

print("\n---- Digitmind ----")

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------

# Initialize the histogram
histogram = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0
}

max_combinations_left = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0
}

# All possible codes
all_codes = create_combinations()

# Clear the log file
with open('optimal_guesses_log.txt', 'w') as file:
    file.write('code,nr,guess,combinations_left,correct_position,wrong_position\n')

for i in range(100000):
    code = random.choice(all_codes)
    number_of_guesses = do_game(code)
    histogram[number_of_guesses] = histogram.get(number_of_guesses, 0) + 1

# Write the histogram to a file
with open('optimal_guesses_histogram.csv', 'w') as file:
    for key, value in histogram.items():
        file.write(f"{key},{value}\n")

# Write the max combinations left to a file
with open('optimal_guesses_max_combinations_left.csv', 'w') as file:
    for key, value in max_combinations_left.items():
        file.write(f"{key},{value}\n")


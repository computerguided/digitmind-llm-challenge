#imports
from score_calculators import *
import os
import sys
from dotenv import load_dotenv
import model
from game_result import *

# -----------------------------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------------------------
load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')
# base_url = os.getenv('OPENAI_BASE_URL')
api_key = os.getenv('NVIDIA_API_KEY')
base_url = os.getenv('NVIDIA_BASE_URL')

# -----------------------------------------------------------------------------
# List of models
# -----------------------------------------------------------------------------
model_names = \
{ 
    0: "o1-preview",
    1: "o1-mini",
    2: "o1",
    3: "o3-mini",
    4: "gpt-4o",
    5: "deepseek-ai/deepseek-r1"
}

# Select model
model_index = 5 # Change this to select a different model
model_name = model_names[model_index]

# -----------------------------------------------------------------------------
# Print and log
# -----------------------------------------------------------------------------
def print_and_log(message : str):
    print(message)
    with open('log.dat', 'a') as file:
        file.write(message + "\n")

# -----------------------------------------------------------------------------
# Game loop
# -----------------------------------------------------------------------------
def do_game(model_name : str, code : list) -> GameResult:
    score_calculator = ScoreCalculator()

    print_and_log("--------------------------------")
    print_and_log(f"Model: {model_name}")
    code_as_string = get_code_as_string(code)
    print_and_log(f"Code to break: {code_as_string}")
    print_and_log("--------------------------------\n")

    game_result = GameResult(model_name, code_as_string)

    # -- Init model --
    llm = model.Model(api_key=api_key, base_url=base_url)

    # -- Read and add prompt --
    with open('prompt.md', 'r') as file:
        prompt = file.read()
    messages = []
    llm.add_user_message(messages, prompt)

    score = Score()
    number_of_guesses = 0
    guesses = []

    while not score.right_guess():
        number_of_guesses += 1

        print_and_log(f"- {number_of_guesses} -")

        response = llm.generate_response(messages, model_name)
        if response is None:
            print_and_log("ERROR: No response from model...")
            number_of_guesses -= 1
            continue

        if len(response.content) > 4:
            # Get the last 5 characters
            response.content = response.content[-5:]

        print_and_log(f"Guess:             {response.content}")
        game_result.add_cost(response.input_tokens, 
                             response.reasoning_tokens, 
                             response.output_tokens)

        # Check if response is valid
        error_message = format_error(response.content)
        if error_message:
            print_and_log(error_message)
            llm.add_response(messages, response.content)
            llm.add_user_message(messages, error_message)
            number_of_guesses -= 1
            game_result.add_format_error()
            continue

        guess = get_guess_from_string(response.content)
        certainty_indicator = response.content[-1]
        
        llm.add_response(messages, response.content)

        score = score_calculator.determine_score(guess, code)
        score_as_string = str(score)

        optimal_guess = score_calculator.is_optimal(guess)
        correct_certainty = score_calculator.is_correct_certainty(certainty_indicator)
        guesses.append(Guess(guess, score, optimal_guess, correct_certainty))
        score_calculator.process_guess(guess, score)

        print_and_log(f"Score:             {score_as_string}")
        print_and_log(f"Optimal guess:     {'yes' if optimal_guess else 'no'}")
        print_and_log(f"Correct certainty: {'yes' if correct_certainty else 'no'}")
        print_and_log(f"Combinations left: {len(score_calculator.combinations_left)}")
        print_and_log(f"Reasoning time:    {response.reasoning_time} seconds")
        print_and_log(f"Input tokens:      {response.input_tokens}")
        print_and_log(f"Reasoning tokens:  {response.reasoning_tokens}")
        print_and_log(f"Output tokens:     {response.output_tokens}\n")

        llm.add_user_message(messages, score_as_string)

        game_result.add_guess(response.reasoning_time, optimal_guess, correct_certainty)

    print_and_log(f"Code broken in {number_of_guesses} guesses.\n")
    return game_result

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

print("\n---- Digitmind ----")

# -----------------------------------------------------------------------------
# Main loop
# The following files are used:
# - codes.dat: A file with codes to break.
# - log.dat: A file to log the intermediate output (i.e. the guesses and scores).
# - results.csv: A file to store the final game results.
# - prompt.md: A file to read the prompt for the LLM.
# -----------------------------------------------------------------------------

# Read the codes from the file
codes = []
with open('codes.dat', 'r') as file:
    lines = file.readlines()
    for line in lines:
        code_string = line.strip()
        code = [int(digit) for digit in code_string]
        codes.append(code)

# Do the game for each code
for code in codes:
    game_result = do_game(model_name, code)

    # Open a file to append the results
    with open('results.csv', 'a') as file:
        file.write("\n" + game_result.to_csv_row())
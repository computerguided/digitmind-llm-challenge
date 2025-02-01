#imports
from score_calculators import *
import random
import os
from dotenv import load_dotenv
import model
import argparse
from game_result import *

# -----------------------------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv('OPEN_ROUTER_API_KEY')
base_url = os.getenv('OPEN_ROUTER_BASE_URL')

# -----------------------------------------------------------------------------
# List of models
# -----------------------------------------------------------------------------
model_names = \
{ 
    0: "o1-mini",
    1: "o1",
    2: "o3-mini",
    3: "gpt-4o",
    4: "deepseek/deepseek-r1",
    5: "deepseek/deepseek-r1:nitro"
}

# Select model
model_index = 4 # Change this to select a different model
model_name = model_names[model_index]

# -----------------------------------------------------------------------------
def do_game(model_name : str, code : list) -> GameResult:
    score_calculator = ScoreCalculator()

    # -- Generate code to break --
    if args.code is None:
        all_possible_codes = create_combinations()
        code = random.choice(all_possible_codes)
    else:
        # Retrieve the digits of the code
        code = [int(digit) for digit in args.code]

    code_as_string = ''.join(str(digit) for digit in code)
    print(f"Code to break: {code_as_string}\n")

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

        print(f"- {number_of_guesses} -")

        response = llm.generate_response(messages, model_name)
        if response is None:
            print("ERROR: No response from model...")
            number_of_guesses -= 1
            continue

        print(f"Guess:             {response.content}")
        game_result.add_cost(response.input_tokens, 
                             response.reasoning_tokens, 
                             response.output_tokens)

        # Check if response is valid
        error_message = format_error(response.content)
        if error_message:
            print(error_message)
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

        print(f"Score:             {score_as_string}")
        print(f"Optimal guess:     {'yes' if optimal_guess else 'no'}")
        print(f"Correct certainty: {'yes' if correct_certainty else 'no'}")
        print(f"Combinations left: {len(score_calculator.combinations_left)}")
        print(f"Reasoning time:    {response.reasoning_time} seconds")
        print(f"Input tokens:      {response.input_tokens}")
        print(f"Reasoning tokens:  {response.reasoning_tokens}")
        print(f"Output tokens:     {response.output_tokens}\n")

        llm.add_user_message(messages, score_as_string)

        game_result.add_guess(response.reasoning_time, optimal_guess, correct_certainty)

    print(f"Code broken in {number_of_guesses} guesses.")
    return game_result

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

# Get optional arguments, being the code to break
parser = argparse.ArgumentParser()
parser.add_argument("--code", type=str, default=None, help="Code to break")
args = parser.parse_args()

print( "\n---- Digitmind ----")
print(f"Model: {model_name}")

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
# Repeat the game 10 times
for i in range(10):
    game_result = do_game(model_name, args.code)

    # Open a file to append the results
    with open('results.csv', 'a') as file:
        file.write("\n" + game_result.to_csv_row())



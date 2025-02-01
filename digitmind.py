#imports
from score_calculators import *
import random
import os
from dotenv import load_dotenv
import model
import argparse
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

model_names = { 0: "deepseek/deepseek-r1-distill-qwen-32b", 
                1: "o1-preview", 
                2: "deepseek/deepseek-r1",
                3: "openai/gpt-4o-2024-11-20",
                4: "o1-mini",
                5: "deepseek/deepseek-r1:nitro",
                6: "o1-2024-12-17",
                7: "o1",
                8: "o3-mini"}

# Select model
model_index = 8 # Change this to select a different model
model_name = model_names[model_index]
   
# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

# Get optional arguments, being the code to break
parser = argparse.ArgumentParser()
parser.add_argument("--code", type=str, default=None, help="Code to break")
args = parser.parse_args()

print( "\n---- Digitmind ----")
print(f"Model: {model_name}")

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

    response, response_duration = llm.generate_response(messages, model_name)
    if response is None:
        print("ERROR: No response from model...")
        continue

    print(f"Guess: {response}")
    # Check if response is valid
    error_message = format_error(response)
    if error_message:
        print(error_message)
        llm.add_response(messages, response)
        llm.add_user_message(messages, error_message)
        number_of_guesses -= 1
        continue

    guess = get_guess_from_string(response)
    certainty_indicator = response[-1]
    
    llm.add_response(messages, response)

    score = score_calculator.determine_score(guess, code)
    score_as_string = str(score)

    optimal_guess = score_calculator.is_optimal(guess)
    correct_certainty = score_calculator.is_correct_certainty(certainty_indicator)
    guesses.append(Guess(guess, score, optimal_guess, correct_certainty))

    print(f"Score: {score_as_string}")
    print(f"Optimal guess: {'yes' if optimal_guess else 'no'}")
    print(f"Correct certainty: {'yes' if correct_certainty else 'no'}")
    print(f"Reasoning time: {response_duration} seconds")

    score_calculator.process_guess(guess, score)
    print(f"Combinations left: {len(score_calculator.combinations_left)}\n")

    llm.add_user_message(messages, score_as_string)

print(f"Code broken in {number_of_guesses} guesses.")

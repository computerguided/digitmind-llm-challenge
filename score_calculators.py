
def create_combinations() -> list:
    digits = list(range(10))
    return [[w,x,y,z]           \
        for w in digits         \
        for x in digits         \
        for y in digits         \
        for z in digits         \
        if  w not in (x,y,z)    \
        and x not in (y,z)      \
        and y != z ]

def format_error(guess_string : str) -> str:
    digit_chars = [str(i) for i in range(10)]
    error_message = "Please make sure your guess is formatted correctly. "
    if len(guess_string) < 5:
        error_message += "Your guess is too short. It must be 5 characters long, e.g. `1234?`"
    elif len(guess_string) > 5:
        error_message += "Your guess is too long. It must be 5 characters long, e.g. `1234?`"
    elif guess_string[4] not in ('!', '?'):
        error_message += "Your guess does not end with `!` or `?`, e.g. `1234?` or `1234!`"
    elif not all(c in digit_chars for c in guess_string[:4]) \
        or len(set(guess_string[:4])) != 4:
        error_message += "Your guess does not contain 4 **unique** digits, e.g. `1234?`"
    elif not all(c in digit_chars for c in guess_string[:4]):
        error_message += "Your guess does not contain 4 **digits**."
    else:
        return None
    return error_message + " Please try again."

def get_guess_from_string(guess_string : str) -> list:
    return [int(c) for c in guess_string[:4]]

# -----------------------------------------------------------------------------
# -- Classes --
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
class Score:
    def __init__(self , correct_position : int = 0, wrong_position : int = 0):
        self.correct_position = correct_position
        self.wrong_position = wrong_position

    def __str__(self):
        return f"Correct position: {self.correct_position}, Wrong position: {self.wrong_position}"
    
    def __eq__(self, other):
        return self.correct_position == other.correct_position and self.wrong_position == other.wrong_position
    
    def right_guess(self) -> bool:
        return self.correct_position == 4
    
# -----------------------------------------------------------------------------
class Guess:
    def __init__(self, 
                 guess : list,
                 score : Score, 
                 is_optimal : bool, 
                 is_correct_certainty : bool):
        
        self.guess = guess
        self.score = score
        self.is_optimal = is_optimal
        self.is_correct_certainty = is_correct_certainty

# -----------------------------------------------------------------------------
class ScoreCalculator:
        
    def __init__(self):
        self.combinations_left = create_combinations()
        
    def determine_score(self, guess : list, code : list) -> dict:          
        pairwise = zip(guess, code)
        score = Score()            
        score.correct_position = sum(1 for p in pairwise if p[0] == p[1])
        score.wrong_position = len(set(guess).intersection(set(code))) - score.correct_position
        return score
    
    def process_guess(self, guess : list, score : Score):
        max_index = len(self.combinations_left)-1
        for i, combination in enumerate(reversed(self.combinations_left)):
            if score != self.determine_score(combination, guess):
                del self.combinations_left[max_index-i]

    # Determine if the guess is optimal by checking
    # if it is part of the possible combinations left.
    def is_optimal(self, guess : list) -> bool:
        return guess in self.combinations_left
    
    # Determine if the indicator is correct.
    # This is the case if there is only one combination left and the indicator is '!'
    # or if there are multiple combinations left and the indicator is '?'.
    def is_correct_certainty(self, indicator : str) -> bool:
        if indicator == '!' and len(self.combinations_left) == 1:
            return True
        elif indicator == '?' and len(self.combinations_left) > 1:
            return True
        else:
            return False

# -----------------------------------------------------------------------------
class DifferenceScoreCalculator(ScoreCalculator):

    def __init__(self):
        self.score = None
    
    def reset_score(self):
        self.score = None
    
    def set_score(self, score: int):
        self.score = score

    def determine_score(self, guess : list, code : list) -> int:
        return sum(abs(guess[i] - code[i]) for i in range(len(guess)))

    def right_guess(self) -> bool:
        return self.score == 0
    
    

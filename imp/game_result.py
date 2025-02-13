# -----------------------------------------------------------------------------
# model,
# code,
# num_guesses,
# num_optimal_guesses,
# num_certainty_errors,
# total_reasoning_time,
# num_format_errors,
# total_input_tokens,
# total_reasoning_tokens,
# total_output_tokens
# -----------------------------------------------------------------------------
class GameResult:
    def __init__(self, model : str, code : list):
        self.model = model
        self.code = code
        self.num_guesses = 0
        self.num_optimal_guesses = 0
        self.num_certainty_errors = 0
        self.total_reasoning_time = 0
        self.num_format_errors = 0
        self.total_input_tokens = 0
        self.total_reasoning_tokens = 0
        self.total_output_tokens = 0

    def add_guess(self, 
                  reasoning_time : int,
                  is_optimal : bool,
                  is_correct_certainty : bool):
        self.num_guesses += 1
        self.num_optimal_guesses += 1 if is_optimal else 0
        self.num_certainty_errors += 1 if not is_correct_certainty else 0
        self.total_reasoning_time += reasoning_time

    def add_format_error(self):
        self.num_format_errors += 1
    
    def add_cost(self, 
                 input_tokens : int, 
                 reasoning_tokens : int, 
                 output_tokens : int):
        self.total_input_tokens += input_tokens
        self.total_reasoning_tokens += reasoning_tokens
        self.total_output_tokens += output_tokens

    def to_csv_row(self) -> str:
        return f"{self.model},{self.code},{self.num_guesses},{self.num_optimal_guesses},{self.num_certainty_errors},{self.total_reasoning_time},{self.num_format_errors},{self.total_input_tokens},{self.total_reasoning_tokens},{self.total_output_tokens}"

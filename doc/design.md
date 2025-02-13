# Digitmind Challenge Design

## Introduction

To evaluate the reasoning power of a model, the model will play a number of rounds of the game Digitmind.

Digitmind is a guessing game where the model must guess a _code_, which is a randomly chosen 4-digit number with distinct digits, e.g. "1234".

The model will make guesses and receive a score for each guess. 

A score consists of two numbers: the number of digits that are in the correct position, and the number of digits that are in the wrong position, e.g. "Correct position: 2, Wrong position: 1". 

The model can use the scores for its internal reasoning to generate a new guess.

The model will keep guessing until the code is broken or the maximum number of guesses is reached.

After a number of rounds, the statistics are evaluated.

## Prompt


## Data structures



## Optimal guess

An optimal guess is a guess that is part of the possible combinations left.


## Certainty indicator






### Round

The data for a single round of the game are collected in a `Round` class with the following attributes:

- `num_guesses`: the number of guesses it took to break the code
- `num_format_errors`: the number of format errors
- `num_suboptimal_guesses`: the number of suboptimal guesses
- `num_certainty_errors`: the number of certainty errors
- `reasoning_time`: the time it took the model to make a guess after it received a score
- `guessed_correctly`: whether the model guessed the correct code within 12 guesses

Note that when no suboptimal guesses are made, the maximum number of guesses it can take to break the code is 7. To allow for a few suboptimal guesses, the maximum number of guesses is set to 12. When the model is unable to break the code within 12 guesses, it is considered a failure. This is tracked by the `guessed_correctly` flag.

### Statistics

To evaluate the model, the following s

The data for all rounds are stored in the `Rounds` list.

### Score

The score is calculated by comparing the guess with the code. The score is a class with two attributes:

* **correct_position**: the number of digits that are in the correct position.
* **wrong_position**: the number of digits that are in the wrong position.

```python
class Score:
    def __init__(self):
        self.correct_position = 0
        self.wrong_position = 0
```

The score must be supplied to the model as a string. To be able to do this, the `__str__` operator is implemented:

```python
    def __str__(self):
        return f"Correct position: {self.correct_position}, Wrong position: {self.wrong_position}"
```

For the method [`process_score`](#process-score), the score must be compared with another score. To be able to do this, the `__eq__` operator is implemented:

```python
    def __eq__(self, other):
        return self.correct_position == other.correct_position and self.wrong_position == other.wrong_position
```

## Methods

### Format checker

The format checker is a function that checks whether the guess is a string of 4 distinct digits with a certainty indicator. If not, it returns `False`.

```python
def is_correct_format(guess_string : str) -> bool:
    digit_chars = [str(i) for i in range(10)]
    if len(guess_string) != 5 \
        or guess_string[4] not in ('!', '?') \
        or not all(c in digit_chars for c in guess_string[:4]) \
        or len(set(guess_string[:4])) != 4:
        return False
    return True
```

### Get guess from string

Assuming that the format checker has already been used, the guess is given as a string, e.g. "1234?". This string must be converted to a tuple of 4 distinct digits, e.g. (1,2,3,4).

```python
def get_guess_from_string(guess_string : str) -> tuple:
    return [int(c) for c in guess_string[:4]]
```

### Suboptimal guess

To determine whether a guess is suboptimal, the possible combinations left are compared with the guess. If the guess is not part of the possible combinations left, it is considered a suboptimal guess.

```python
def is_suboptimal_guess(guess, possible_combinations_left) -> bool:
    return guess not in possible_combinations_left
```

### Possible combinations

At the start of the game, the possible combinations left are all 4-digit combinations with distinct digits. This list can be constructed as follows:

```python
def create_combinations() -> list:
    digits = list(range(10))
    return [(w,x,y,z)           \
        for w in digits         \
        for x in digits         \
        for y in digits         \
        for z in digits         \
        if  w not in (x,y,z)    \
        and x not in (y,z)      \
        and y != z ]
```

This function will create 10x9x8x7 = 5040 combinations.

### Process score

During the game, the list of possible combinations left is reduced. This is done by looping through all combinations and removing those that would give a different score. Note that under the hood, this uses the `__eq__` operator of the [`Score`](#score) class.

```python
def process_score(combinations_left : list, guess : list, score : Score):
    max_index = len(combinations_left)-1
    for i, combination in enumerate(reversed(combinations_left)):
        if score != determine_score(combination, guess):
            del combinations_left[max_index-i]
```




## Appendix - OpenAI 




## Appendix - DeepSeek API


https://api-docs.deepseek.com/guides/reasoning_model#api-example

```python
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

# Round 2
messages.append({'role': 'assistant', 'content': content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)
# ...
```
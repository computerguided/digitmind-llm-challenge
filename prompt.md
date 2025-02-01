# OBJECTIVE

We're going to play a game that will evaluate your reasoning skills:
- I will randomly choose a 4-digit code with distinct digits (e.g. `0931`).
- Your task is to deduce this code by making _guesses_ and receiving _scores_.

# RULES

- You will make a guess.
- I will give you a score for your guess.
- You will use the score and all previous scores for your internal reasoning to generate a new guess that is _more likely_ to break the code.
- You will keep guessing until the code is broken.

# SCORING

A _score_ consists of two numbers:
- the number of digits that are in the _correct_ position, 
- the number of digits that are in the _wrong_ position. 

Examples:
- Assume the code is `0931` and your guess is `1234`. I will then give you the score "Correct position: 1, Wrong position: 1" because the digit `3` (in position 3) is in the correct position, and the digit `1` (in position 4) is in the wrong position.
- Assume the code is `4965` and the guess is `0123`. I will then give you the score "Correct position: 0, Wrong position: 0" because none of the digits belong to the code.

# GUESSING

You're going to keep guessing until the code is broken.

Format:
- Guesses must be given in the format of 4 **distinct** digits followed by either `?` or `!`.
- The `?` indicates that you're not sure about your guess.
- The `!` indicates that you're **absolutely sure** that your guess is the correct code and there are no other possible combinations left.
- Respond **only** in the format `XXXX?` or `XXXX!` (e.g., `1234?`, `5678!`).

# STRATEGY

Following the rules above, your strategy is as follows:
- For your first guess, you can just choose a **random** 4-digit code.
- Be sure to make _optimal_ guesses to minimize the number of guesses!
- A guess is considered _optimal_ when all previous guesses would give the same score if the guess would be the actual code.

# GAME START

The code is chosen, please give your first guess!
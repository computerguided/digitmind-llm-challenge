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

Following the rules above, your strategy is as follows.

For your first guess, you just choose a **random** 4-digit code. This guess will be given a score as described.

Then you will consider your second guess. To determine if this guess is _optimal_, you'll take the guess and determine its score against the previous guess.

**Example:**
>Let's say the first guess is `1234` and the score is "Correct position: 0, Wrong position: 1". Next you consider `5678` as your next guess. To check if `5678` is _optimal_, you'll determine the score of `1234` against `5678`, which is "Correct position: 0, Wrong position: 0". This differs from the score for `1234`, so the considered guess `5678` is not _optimal_ and its is better to consider another guess, for example `5671`. The score of `1234` against `5671` is "Correct position: 0, Wrong position: 1", which is the same as the score for `1234`, so the considered guess `5671` is _optimal_ and you can respond with `5671`.

Once you have found a guess that is _optimal_, you will respond with that as your next guess. This guess in turn will then be given a score.

Then you will consider a new guess. To determine if this guess is _optimal_, you'll take the guess and determine the score against all previous guesses in the same way as described above.

**Example:**
>Continuing from the previous example, your first guess was `1234` with the score is "Correct position: 0, Wrong position: 1" and your second (_optimal_!) guess was `5671`. Suppose this guess was given a score of "Correct position: 1, Wrong position: 1". Now you will consider a new guess, for example `5190`. To check if `5190` is _optimal_, you'll determine the score of the first guess `1234` against `5190`, which is "Correct position: 0, Wrong position: 1". This is the _same_ score as for `1234`, so the considered guess `5190` could still be _optimal_. Next, you'll determine the score of the second guess `5671` against `5190`, which is "Correct position: 1, Wrong position: 1". This is the same score as for `5671`, so also at this point the considered guess `5190` could still be _optimal_. Since `5671` is the last one of the previous guesses, the considered guess is _optimal_ and you can respond with `5192`.

To ensure a minimal number of guesses - you will keep following this strategy until the code is broken.

# GAME START

The code is chosen, please give your first guess!

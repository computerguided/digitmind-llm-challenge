## Abstract

Large Language Models (LLMs) are frequently showcased for their reasoning abilities in coding, mathematics, and logical puzzles. However, their fundamental reasoning skills remain limited. This study evaluates the reasoning capabilities of LLMs using **Digitmind**, a numerical variant of Mastermind where a code breaker must deduce a four-digit code using logical deduction. We compare the performance of two models, `o1` and `o3-mini`, across 20 games of Digitmind. Key performance metrics include optimality of guesses, reasoning time, certainty errors, and overall win rates. Furthermore, we explore how prompt engineering affects model performance. Results indicate that `o3-mini` consistently outperforms `o1`, and that a refined prompt significantly improves reasoning capabilities, achieving near-optimal performance.

## Introduction

Recent advancements in Large Language Models (LLMs) have sparked considerable interest in their reasoning abilities. Traditional benchmarks often focus on coding, mathematics, and logical puzzles. However, these assessments may not fully capture the ability of LLMs to employ systematic reasoning and deduction.

To examine this, we introduce **Digitmind**, a variant of Mastermind where the objective is to deduce a four-digit code with no repeating digits. The game requires a logical approach to narrowing down possibilities based on feedback from previous guesses. Unlike standard language-based reasoning tasks, Digitmind presents a structured problem where optimal strategies can be formally defined and evaluated.

This study evaluates the reasoning skills of LLMs `o1` and `o3-mini` by having them play 20 games of Digitmind. Their performance is assessed based on the number of guesses, correctness of certainty markers (`!` or `?`), reasoning efficiency, and adherence to optimal guessing strategies. Additionally, we analyze whether prompt engineering can improve their performance, particularly in making optimal guesses.

## Methodology

### Computational Model

To assess LLM performance in Digitmind, we first establish an optimal computational model. This involves:
- **Generating guesses:** Selecting a guess from the set of remaining possible combinations.
- **Scoring guesses:** Comparing a guess to the actual code and assigning a score.
- **Processing scores:** Eliminating inconsistent possibilities based on the score.

A simple algorithm follows:

```python
combinations = create_all_combinations()
code_to_break = random.choice(combinations)
score = {'correct position': 0, 'wrong position': 0}
number_of_guesses = 0
while score['correct position'] < 4:
    guess = random.choice(combinations)
    score = get_score(guess)
    combinations = process_score(guess, score, combinations)
    number_of_guesses += 1
print(f"Code {code_to_break} guessed in {number_of_guesses} guesses")
```

This ensures that a computational solver always selects an optimal guess from the remaining valid options.

### Experiment Setup

Both `o1` and `o3-mini` played 20 games of Digitmind. The LLMs were prompted with a structured instruction set that dictated:
- Guesses must be four distinct digits followed by `?` or `!`.
- `?` indicates uncertainty; `!` signifies certainty in the guess.
- Optimal guesses should minimize the number of remaining possibilities.

Metrics collected:
- **Win rate:** Number of games won.
- **Average guesses per game.**
- **Reasoning time per guess and per game.**
- **Certainty errors:** Incorrect use of `?` or `!`.
- **Reasoning tokens per game.**
- **Optimality:** Percentage of optimal guesses.

A refined version of the prompt was also tested to evaluate the impact of prompt engineering.

## Results

| Parameter | o1 | o3-mini |
| --- | --- | --- |
| Games Won | 6 | **10** |
| Avg. Guesses per Game | 6.45 | **6.15** |
| Reasoning Time per Guess (s) | 52 | **24** |
| Reasoning Time per Game (s) | 336 | **153** |
| Certainty Errors per Game | 75% | **65%** |
| Reasoning Tokens per Game | 45,491 | **34,982** |
| Optimality | **74%** | 71% |

### Impact of Prompt Engineering

A refined prompt was introduced to explicitly guide the model in making optimal guesses. The revised prompt led to a significant performance boost.

| Parameter | o3-mini | o3-mini (Improved Prompt) |
| --- | --- | --- |
| Avg. Guesses per Game | 6.15 | **5.55** |
| Games Won | 3 | **12** |
| Reasoning Time per Guess (s) | 52 | **22** |
| Reasoning Time per Game (s) | 336 | **124** |
| Certainty Errors per Game | 75% | **40%** |
| Reasoning Tokens per Game | 45,491 | **25,094** |
| Optimality | 74% | **100%** (!) |

## Discussion

The results clearly indicate that `o3-mini` outperforms `o1` across most parameters. Notably, prompt engineering led to substantial improvements in all areas, particularly in optimality and reasoning efficiency. The refined prompt guided `o3-mini` to achieve near-optimal performance, demonstrating the power of structured instructions in improving LLM reasoning.

Although `o3-mini` with the improved prompt closely matches computational strategies, limitations remain. The model occasionally makes suboptimal guesses or incorrect certainty decisions. Further refinement of prompts and iterative feedback mechanisms could enhance reasoning further.

## Conclusion

This study demonstrates that Digitmind serves as an effective benchmark for testing LLM reasoning. The `o3-mini` model consistently outperforms `o1`, particularly when using an improved prompt. Results highlight that prompt engineering can dramatically improve LLM reasoning, pushing performance closer to optimal computational strategies.

Future work could explore:
- Testing on more complex variants of Digitmind.
- Comparing with human performance.
- Evaluating other LLM architectures.

The findings emphasize the importance of structured prompting in guiding LLM reasoning and problem-solving.


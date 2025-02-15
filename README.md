![Digitmind](img/digitmind_header.jpg)

## Abstract

Large Language Models (LLMs) are frequently showcased for their reasoning abilities in coding, mathematics, and logical puzzles. However, their fundamental reasoning skills remain limited. This study evaluates the reasoning capabilities of LLMs using **Digitmind**, a numerical variant of Mastermind where a code breaker must deduce a four-digit code using logical deduction. We compare the performance of two of OpenAI's latest models, `o1` and `o3-mini`, across 20 games of Digitmind. Key performance metrics include optimality of guesses, reasoning time, certainty errors, and overall win rates. Furthermore, we explore how prompt engineering affects model performance. Results indicate that `o3-mini` consistently outperforms `o1`, and that a refined prompt significantly improves reasoning capabilities, achieving near-optimal performance.

**All the code for this study is available in this repository. For instructions on how to run the code, please refer to the [Appendix](#appendix---running-the-code).**

## Introduction

Recent advancements in Large Language Models (LLMs) have sparked considerable interest in their reasoning abilities. Traditional benchmarks often focus on coding, mathematics, and logical puzzles. However, these assessments may not fully capture the ability of LLMs to employ systematic reasoning and deduction.

To examine this, we introduce **Digitmind**, a variant of Mastermind where the objective is to deduce a four-digit code with no repeating digits. 

This study builds further on the work of the implementation of the game in the GitHub repository [digitmind-in-python](https://github.com/computerguided/digitmind-python).

The game Digitmind requires a logical approach to narrowing down possibilities based on feedback from previous guesses. Unlike standard language-based reasoning tasks, Digitmind presents a structured problem where optimal strategies can be formally defined and evaluated.

This study evaluates the reasoning skills of LLMs `o1` and `o3-mini` by having them play 20 games of Digitmind. Their performance is assessed based on the number of guesses, correctness of certainty markers (`!` or `?`), reasoning efficiency, and adherence to optimal guessing strategies. Additionally, we analyze whether prompt engineering can improve their performance, particularly in making optimal guesses.

## Methodology

### Computational model

Before being able to assess the performance of the reasoning LLMs in the context of the Digitmind Challenge, it is important to understand how the game Digitmind works and how the performance of an _optimal computer code breaker_ can be measured. To do this, the following needs to be understood:

- [Generating guesses](#generating-guesses): How the guesses are generated, i.e. chosen from the set of remaining possible combinations.
- [Getting the score](#getting-the-score): How the score is calculated, i.e. how the guess is compared to the actual code to be broken - or more generally, how two combinations can be compared.
- [Processing the score](#processing-the-score): How the score is used to process the list of possible combinations and remove the ones that do not match the score.

### Generating guesses

In an optimal computational code breaker model, a guess is generated by simply taking a random element from the list of _remaining possible combinations_.

For the _first_ guess, this list contains all combinations as described further in the ["Generating the combinations"](#generating-the-combinations) section.

For this guess a _score_ is calculated by comparing it to the actual code to be broken.

The score contains the number of digits in the _correct position_ and the number of digits in the _wrong position_.

For example, if the actual code is '9024' and the guess is '1234', the score is: Correct position: 1, Wrong position: 1.

The score is then used to _process_ the list of possible combinations, removing all combinations that are _not consistent with the score_. This means that each combination in the list is compared with the guess and it is determined how many digits are in the same position and how many digits are in a different position. Only those combinations that match the score are kept.

This process is repeated which will reduce the list of possible combinations until the code to break is found.

A simple algorithm can be used to generate the guesses:

```python
combinations = create_all_combinations();
code_to_break = random.choice(combinations);
score = {'correct position': 0, 'wrong position': 0};
number_of_guesses = 0
while score['correct position'] < 4:
    guess = random.choice(combinations);
    score = get_score(guess);
    combinations = process_score(guess, score, combinations);
    number_of_guesses += 1
print(f"Code {code_to_break} guessed in {number_of_guesses} guesses")
```

The called functions [`create_all_combinations()`](#creating-the-combinations), [`get_score()`](#getting-the-score) and [`process_score()`](#processing-the-score) are defined in the following sections.

### Creating the combinations

The number of possible combinations \( N_C \) of 4 different digits is specified as:

$$
N_C = 10 \times 9 \times 8 \times 7 = 5040
$$

A function can be created to construct the list of combinations:

```python
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
```

### Getting the score

The score is calculated by comparing the guess to the actual code to be broken. More generally, the score can also be used to compare two combinations.

```python
def get_score(code, guess) :
    score = {'correct position':0, 'wrong position':0}
    for i in range(4):
        if guess[i] == code[i]:
            score['correct position'] += 1
        elif guess[i] in code:
            score['wrong position'] += 1    
    return score
```

Besides determining the score, the function can also be used to process the list of remaining possible combinations and remove those combinations that are not consistent with the score as described in the next section.

### Processing the score

The score is used to _process_ the list of possible remaining combinations, removing all combinations that do not match the score.

```python
def process_score(guess, score, combinations_left):
    max_index = len(combinations_left)-1
    for i, combination in enumerate(reversed(combinations_left)):
        if score != get_score(code, guess):
            del combinations_left[max_index-i]
    return combinations_left
```

### Generating optimal guesses

For the game Digitmind, the winning strategy is to make _optimal_ guesses, which ensures that the code is broken in the minimum number of guesses.

For a human (or LLM) Digitmind code breaker, an **optimal guess** is defined as a guess that would give the same score for all the previous guesses if it were the actual code.

For example, suppose the first guess was `1234` and the score is "Correct position: 0, Wrong position: 1" and the second guess was `5671`with a score of "Correct position: 1, Wrong position: 1". Now, suppose that a new guess `5190` is considered. To check if `5190` is _optimal_, the score of the first guess `1234` is determined against `5190`, which is "Correct position: 0, Wrong position: 1". This is the _same_ score as for `1234`, so the considered guess `5190` could still be _optimal_. Next, the score of the second guess `5671` against `5190` is determined, which is "Correct position: 1, Wrong position: 1". This is the same score as for `5671`, so this means that the considered guess is _optimal_ and can be chosen as the next guess.

In a computational code breaker, an optimal guess is also ensured when the guess is chosen from the list of remaining possible combinations. Obviously, this method is not practically possible for a human - or LLM - code breaker and the first method is used.

### Determining the maximum number of guesses

For the game Digitmind, the absolute maximum number of optimal guesses that are theoretically required to break any code is 9.

This can be experimentally verified by generating a large number of random codes and then determining the number of _optimal_ guesses required to break them.

To explicitly use the maximum number of guesses, the algorithm is slightly modified by removing the code to break from the list of combinations. Then, guesses are generated until there are no combinations left and the last guess is the code to break.

The altered algorithm is shown below:

```python
combinations = create_all_combinations();
code_to_break = random.choice(combinations);

combinations.remove(code_to_break); # Prevents guessing the code

score = {'correct position': 0, 'wrong position': 0};
number_of_guesses = 0
while len(combinations) > 0:
    guess = random.choice(combinations);
    score = get_score(guess);
    combinations = process_score(guess, score, combinations);
    number_of_guesses += 1
number_of_guesses += 1 # Add the last guess
print(f"Code {code_to_break} guessed in {number_of_guesses} guesses")
```

The following shows the histogram of the number of optimal guesses for 100,000 games with random codes.

![](/img/max_optimal_guesses.png)

Although no really visible in the histogram, there is a small percentage of games where 9 guesses are required to break a code as can be seen in the table below.

| Guesses | Frequency | [%] |
| ---: | ---: | ---: |
| 1 | 0 | 0.000% |
| 2 | 0 | 0.000% |
| 3 | 54 | 0.054% |
| 4 | 2581 | 2.581% |
| 5 | 21018 | 21.018% |
| 6 | 45660 | 45.660% |
| 7 | 27032 | 27.032% |
| 8 | 3598 | 3.598% |
| 9 | 57 | 0.057% |

The estimation of the average number of guesses \( G \) follows from the equation:

$$
G = \sum_{i=1}^{9} g_i \times f_i = 6.08
$$

where \( g_i \) is the number of guesses and \( f_i \) is the frequency of the number of guesses.


Another interesting metric is the maximum number of combinations left for each guess, with the first guess starting at 5040 combinations. This is shown in the table below.

| Guess nr. | Combinations |
| ---: | ---: |
| 1 | 5040 |
| 2 | 1440 |
| 3 | 378 |
| 4 | 216 |
| 5 | 50 |
| 6 | 18 |
| 7 | 7 |
| 8 | 2 |
| 9 | 1 |

This follows a logarithmic curve as shown in the plot below.
![](/img/combinations_left.png)

## Experiment description

A [Python script](digitmind.py) was used to play the game Digitmind with the LLM.

For both models (o1, o3-mini), a total of 20 games were played for which the code to break was read from a [codes file](./data/codes.dat). For these games, the LLM was configured to use a [prompt](./data/prompt.md) and the results were stored in a [results file](./logs/results.csv).

The game starts by giving the LLM the prompt and asking it to generate a response.

In the prompting the required format of the response is specified:

- Guesses must be given in the format of 4 **distinct** digits followed by either `?` or `!`.
- The `?` indicates that you're not sure about your guess.
- The `!` indicates that you're **absolutely sure** that your guess is the correct code and there are no other possible combinations left.
- Respond **only** in the format `XXXX?` or `XXXX!` (e.g., `1234?`, `5678!`).

The response of the LLM is checked to see if it is in the correct format. If it is not, the LLM is asked to respond in the correct format. However, it turned out that for none of the responses was this necessary.

The following is then determined for each guess:

- **Whether the guess is optimal**: To determine whether the guess is optimal, it is checked whether the guess is part of the remaining possible combinations. When this is the case, the guess is optimal.
<br>
- **Whether the guess is correct in terms of certainty**: To determine whether the guess is correct in terms of certainty, it is checked whether there is only one combination left and the indicator is `!` or whether there are multiple combinations left and the indicator is `?`.
<br>
- **The score of the guess**: After a correctly formatted response has been given, the guess is scored and the list of remaining possible combinations is updated.

The results of the two series of games are stored in a [results file](./logs/results.csv).

The LLM was configured to first use a [prompt](./data/prompt.md) and the results were stored in a [results file](./logs/results.csv).

The results are stored in a [results file](./logs/results.csv).

The prompt used for the LLM is stored in a [prompt file](./data/prompt_v2.md).

### Parameters

The following parameters were used to compare the models:

- **Won**: The number of games won.
- **Guesses**: The average number of guesses per game.
- **Reasoning time per guess**: The average time taken to reason about each guess.
- **Reasoning time per game**: The average time taken to reason about all guesses in a game.
- **Certainty errors per game**: The percentage of games where the model made a mistake in the certainty of its guess.
- **Reasoning tokens per game**: The average number of tokens used to reason about the game.
- **Optimality**: The percentage of guesses that were optimal.

## Prompt Engineering

Considering that the o3-mini model is the best model, it is interesting to investigate if performance might be improved when the prompt is changed.

The area where the reasoning of the model could be improved is obviously that it should not make suboptimal guesses.

In the first version of the prompt, under the ["Strategy"](prompt.md#strategy) section it was only mentioned that:

>- Be sure to make _optimal_ guesses to minimize the number of guesses!
>- A guess is considered _optimal_ when all previous guesses would give the same score if the guess would be the actual code.

While this technically specifies the strategy, apparently it is not clear - or elaborate enough - for the model how to make only optimal guesses.

Therefore, the file [prompt_v2.md](/prompt_v2.md) contains an improved version of the original prompt. Under the ["Strategy"](prompt_v2.md#strategy) section, a more elaborate description of the strategy is given, explaining in elaborate detail how the model can determine whether a guess is optimal or not, using more elaborate examples.

Then the same 20 games were played again (i.e. the same codes were used again) using model o3-mini, but this time the LLM was configured to use an improved [prompt](./data/prompt_v2.md).


## Results

The complete spreadsheet with all the results can be found [here](https://docs.google.com/spreadsheets/d/e/2PACX-1vS9cA0PTOcrUxEoXLn8tLnVTAOQo_rp2iUwqm4y6cVsyvZmt4wiEfnFBKVDizbMHmyIZOVqz9jXheUP/pubhtml#).

The following table shows the results of the two models.

| Parameter | o1 | o3-mini |
| :--- | :---: | :---: |
| Won | 6 | **10** |
| Guesses | 6.45 | **6.15** |
| Reasoning time per guess | 52 | **24** |
| Reasoning time per game | 336 | **153** |
| Certainty errors per game | 75% | **65%** |
| Reasoning tokens per game | 45491 | **34982** |
| Optimality | **74%** | 71% |

The histogram below shows the number of guesses per game for the two models.

![](/img/guesses_histogram.png)

The o3-model won 4 times more games than the o1-model. The 4 games the o1 model lost, were all games in which the o1 model took 8 or 9 guesses. 

If these codes are tried again, there is a chance that the o1 model will take less guesses, as shown in the table below.

| Code | First try | Second try |
| :--- | :---: | :---: |
| 7960 | 9 | 5 |
| 3796 | 8 | 8 |
| 8249 | 8 | 7 |
| 2953 | 8 | 6 |

But this is only if the o1 model doesn't make any mistakes, e.g. 'wander off course'.

The following table shows the guesses of the o1 model when it tried to guess the code `7960` but failed to follow the optimal strategy. In the table the possible combinations are given from which the model should choose the next guess if it would have followed the optimal strategy. If the model chose a combination which was not part of this set, it is marked as not being an optimal guess.

As can be seen, at the 6th guess, there is only one possible combination left, but the model chose `7450` instead of `7960`.

| nr. | Guess | Combinations | Optimal guess | Correct position | Wrong position |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0123 | 5040 | yes | 0 | 1 |
| 2 | 4567 | 1440 | no | 1 | 1 |
| 3 | 4609 | 288 | yes | 0 | 3 |
| 4 | 8640 | 17 | no | 1 | 1 |
| 5 | 9047 | 5 | yes | 0 | 3 |
| 6 | 7450 | 1 | no | 2 | 0 |
| 7 | 6539 | 1 | no | 0 | 2 |
| 8 | 2813 | 1 | no | 0 | 0 |
| 9 | 7960 | 1 | yes | 4 | 0 |

### Results with improved prompt

The results of the previous version of the prompt in comparison with the results of the improved prompt in the following table:

| Parameter | o3-mini | o3-mini v2 |
| :--- | :---: | :---: |
| Guesses | 6.15 | **5.55** |
| Won | 3 | **12** |
| Reasoning time per guess | 52 | **22** |
| Reasoning time per game | 336 | **124** |
| Certainty errors per game | 75% | **40%** |
| Reasoning tokens per game | 45491 | **25094** |
| Optimality | 74% | **100%** (!) |

## Conclusion

The results clearly indicate that `o3-mini` outperforms `o1` across most parameters. Notably, prompt engineering led to substantial improvements in all areas, particularly in optimality and reasoning efficiency. The refined prompt guided `o3-mini` to achieve near-optimal performance, demonstrating the power of structured instructions in improving LLM reasoning.

From the table it is clear that changing the prompt dramatically increased the performance across all parameters!


## Appendix - Running the code

The code is written in Python and uses the `openai` library. To run the code, you need to perform the following steps:

**1. Create a virtual environment**

It works best to use a virtual environment.

```
python -m venv env
```

**2. Activate the virtual environment**

On Windows:
```
env\Scripts\activate
```

On macOS and Linux:
```
source env/bin/activate
```

**3. Install the dependencies**

```
pip install -r requirements.txt
```

**4. Specify the API key**

You need to specify the API key for the LLM you want to use. This can be done by creating changing the name of the `.env_example` file in the root directory to `.env` and adding your API key.

```
OPENAI_API_KEY=<add_your_api_key_here>
OPENAI_BASE_URL=https://api.openai.com/v1
```

**5. Generate the codes**

The application needs a file `codes.dat` with codes to break. You can generate/change this file with a specified number of random codes by running the following command:

```
python generate_random_codes.py 20
```

**6. Run the application**

The application uses the following files:

- `codes.dat`: An input file with codes to break.
- `log.dat`: An output file to log the intermediate output (i.e. the guesses and scores).
- `results.csv`: An output file to store the final game results.
- `prompt.md`: An input file to read the prompt for the LLM.

You can run the application by executing the following command:

```
python digitmind.py
```





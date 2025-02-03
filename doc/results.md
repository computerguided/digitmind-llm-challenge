![](/img/results_header.png)

## Parameters

The following parameters were used to evaluate the models:

- **Won**: The number of games won.
- **Guesses**: The average number of guesses per game.
- **Reasoning time per guess**: The average time taken to reason about each guess.
- **Reasoning time per game**: The average time taken to reason about all guesses in a game.
- **Certainty errors per game**: The percentage of games where the model made a mistake in the certainty of its guess.
- **Reasoning tokens per game**: The average number of tokens used to reason about the game.
- **Optimality**: The percentage of guesses that were optimal.





## Results

The following table shows the results of the two models. Clearly, the o3-mini model is better on all parameters and won the challenge (4 times the game was a tie).

| Parameter | o1 | o3-mini |
| :--- | :---: | :---: |
| Won | 6 | **10** |
| Guesses | 6.45 | **6.15** |
| Reasoning time per guess | 52 | **24** |
| Reasoning time per game | 336 | **153** |
| Certainty errors per game | 75% | **65%** |
| Reasoning tokens per game | 45491 | **34982** |
| Optimality | 74% | **71%** |

The histogram below shows the number of guesses per game for the two models.

![](/img/guesses_histogram.png)

## Conclusion

On all parameters, the o3-mini model seems to be better than the o1 model: it is faster, more optimal, and makes fewer mistakes.

The o3-model won 4 times more games than the o1-model. The 4 games the o1 model lost, were all games in which the o1 model took 8 or 9 guesses.


| Code | First try | Second try |
| :--- | :---: | :---: |
| 7960 | 9 | 5 |
| 3796 | 8 | 8 |
| 8249 | 8 | 7 |
| 2953 | 8 | 6 |




o1,7960,5,4,0,193,0,2750,25920,81
o1,3796,8,7,1,382,0,4664,52800,123
o1,8249,7,7,1,3955,0,4004,55104,146
o1,2953,6,4,0,291,0,3366,37888,83


## Other models

### o1-mini

When running the prompt in "o1-mini", the model is unable to find a solution. It even sometimes gives a statement like:

> It appears there might be a contradiction in the feedback provided based on the previous guesses. Given the constraints and the responses, no valid 4-digit code with distinct digits satisfies all the provided scores. Could you please verify the feedback for the previous guesses to ensure consistency?

This is of course not possible, as the scores are calculated by the program and cannot be incorrect.

### o1

Makes errors by repeating the same guess.

```
- 5 -
Guess:             8194!
Score:             Correct position: 2, Wrong position: 1
Optimal guess:     yes
Correct certainty: no
Combinations left: 1
Reasoning time:    55 seconds
Input tokens:      594
Reasoning tokens:  7680
Output tokens:     13

- 6 -
Guess:             8194?
Score:             Correct position: 2, Wrong position: 1
Optimal guess:     no
Correct certainty: no
Combinations left: 1
Reasoning time:    128 seconds
Input tokens:      616
Reasoning tokens:  16512
Output tokens:     13
```

## o3-mini
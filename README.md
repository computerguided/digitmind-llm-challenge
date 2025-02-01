# Digitmind LLM Challenge

## Introduction
There is a lot of buzz around LLMs and their capabilities for reasoning. We see this demonstrated in demos which mainly focus on coding, math or logical riddles.

While this is impressive - and useful to some extent - it's also clear that most LLMs still lack some basic reasoning skills.

My go-to example to demonstrate this is to have an LLM try to play a game of Digitmind, which is a variant of Mastermind but instead of colors, it uses digits.

This is as basic as it gets, but it's still a good example to demonstrate the reasoning skills of LLMs.

For example, if the code is "0931" and the guess is "1234", the score is "Correct position: 1, Wrong position: 1".

## Installation

1. Create a virtual environment

```
python -m venv env
```

2. Activate the virtual environment

On Windows:
```
env\Scripts\activate
```

On macOS and Linux:
```
source env/bin/activate
```

3. Install the dependencies

```
pip install -r requirements.txt
```






# Digitmind LLM Challenge

## Introduction
There is a lot of buzz around LLMs and their capabilities for reasoning. We see this demonstrated in demos which mainly focus on coding, math or logical riddles.

While this is impressive - and useful to some extent - it's also clear that most LLMs still lack some basic reasoning skills.

My go-to example to demonstrate this is to have an LLM try to play a game of **Digitmind**, which is a variant of **Mastermind** but instead of colors, it uses digits.

For reference, I implemented this game in Python in the [digitmind-in-python](https://github.com/computerguided/digitmind-python) repository.

Using Digitmind is as basic reasoning as it gets, but it's still a good example to demonstrate the reasoning skills of LLMs.

The prompt is given in the file [`prompt.md`](prompt.md), which is read and presented to the LLM at the start of each game.

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

4. Specify the API key

You need to specify the API key for the LLM you want to use. This can be done by creating an `.env` file in the root directory with the following content:

```
OPENAI_API_KEY=<your_api_key>
OPENAI_BASE_URL=https://api.openai.com/v1
```




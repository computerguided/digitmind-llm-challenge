![Digitmind](img/digitmind_header.jpg)

## Overview
There is a lot of buzz around LLMs and their capabilities for _reasoning_. We see this demonstrated in demos which mainly focus on coding, math or logical riddles.

While this is impressive - and useful to some extent - it's also clear that most LLMs still lack some basic reasoning skills.

My go-to example to demonstrate this is to have an LLM try to play a game of **Digitmind**, which is a variant of **Mastermind** but instead of trying to guess a combination of colors, it uses digits.

For reference, I implemented this game in Python in the [digitmind-in-python](https://github.com/computerguided/digitmind-python) repository.

Using Digitmind is as basic reasoning as it gets, so it gives a good indication of the reasoning skills of the LLM.

The prompt is given in the file [`prompt.md`](prompt.md), which is read and presented to the LLM at the start of each game.

A detailed description of the game is given in the file [`game_description.md`](game_description.md).

The application was used to test the reasoning skills of OpenAI's reasoning models `o1` and the newest `o3-mini`.

## Installation

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






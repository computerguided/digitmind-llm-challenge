from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

# Read prompt from file
with open('prompt.md', 'r') as file:
    prompt = file.read()


completion = client.chat.completions.create(
  model="deepseek-ai/deepseek-r1",
  messages=[
    {
      "role":"user",
      "content":prompt
    },
    {
      "role":"assistant",
      "content":"0123?"
    },
    {
      "role":"user",
      "content":"Correct position: 1, Wrong position: 1"
    }
  ],
  temperature=0.6,
  top_p=0.7,
  max_tokens=4096,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")
    
print(completion)


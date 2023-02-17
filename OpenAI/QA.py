import os
import openai

openai.api_key = "sk-9WmAEFEzyHDOcGkietyOiC1VT3A53Ih0v5to86Fd"

response = openai.Completion.create(
  engine="davinci",
  prompt="Q: ¿Quien descubrio Amrica?\nA:",
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)
print(response.choices[0].text)
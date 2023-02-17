import os
import openai

openai.api_key = "sk-9WmAEFEzyHDOcGkietyOiC1VT3A53Ih0v5to86Fd"

response = openai.Completion.create(
  engine="davinci",
  prompt="Hola soy David y me gustan los videojuegos como el de silent hill",
  temperature=0,
  max_tokens=300,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\"\"\""]
)
print(response.choices[0].text)
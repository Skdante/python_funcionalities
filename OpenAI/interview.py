import os
import openai

'''typequestions = "Create a list of questions for my interview with a programmer"'''
typequestions = "Crear una lista de preguntas para mi entrevista con un cantante"
openai.api_key = "sk-9WmAEFEzyHDOcGkietyOiC1VT3A53Ih0v5to86Fd"

response = openai.Completion.create(
  engine="davinci-instruct-beta",
  prompt=typequestions + ":\n\n1.",
  temperature=0.8,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n\n"]
)
print(response.choices[0].text)
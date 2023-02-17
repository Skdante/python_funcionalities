import os
import openai

'''consulta = "Create a SQL request to find all users who live in California and have over 1000 credits"'''
consulta = "Crear una petición SQL para encontrar todos los clientes que compran mas de 5 productos y sus ventas son mayores a 1000 pesos"
openai.api_key = "sk-9WmAEFEzyHDOcGkietyOiC1VT3A53Ih0v5to86Fd"

response = openai.Completion.create(
  engine="davinci",
  prompt=consulta + ":\n\nSELECT",
  temperature=0.3,
  max_tokens=300,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

print("Select ")
print(response.choices[0].text)
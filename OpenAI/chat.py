import os
import openai

'''openai.api_key = os.getenv("sk-9WmAEFEzyHDOcGkietyOiC1VT3A53Ih0v5to86Fd")'''
openai.api_key = "sk-9WmAEFEzyHDOcGkietyOiC1VT3A53Ih0v5to86Fd"

response = openai.Completion.create(
  engine="davinci",
  prompt="Human: ¿COmo te llamas?.\nAI:",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.6,
  stop=["\n", " Human:", " AI:"]
)

print(response.choices[0].text)
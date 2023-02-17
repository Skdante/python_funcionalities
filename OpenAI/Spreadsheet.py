import os
import openai

'''question = "Una hoja de cálculo de tres columnas con lenguajes de programacion, su dificultad y su año"'''
question = "Una hoja de cálculo de tres columnas con frutas, su sabor y sus vitaminas"
#question = "Una hoja de cálculo de tres columnas con nombre, codigo postal y su pais"
openai.api_key = "sk-9WmAEFEzyHDOcGkietyOiC1VT3A53Ih0v5to86Fd"

response = openai.Completion.create(
  engine="davinci",
  prompt="A single column spreadsheet of industry names:\n\n\nIndustry|\nAccounting/Finance\nAdvertising/Public Relations\nAerospace/Aviation\nArts/Entertainment/Publishing\nAutomotive\nBanking/Mortgage\nBusiness Development\nBusiness Opportunity\nClerical/Administrative\nConstruction/Facilities\nConsumer Goods\nCustomer Service\nEducation/Training\nEnergy/Utilities\nEngineering\nGovernment/Military\nGreen\n\n\n###\n\n\nA spreadsheet of top science fiction movies and the year of release:\n\n\nTitle|Year\nStar Wars|1977\nJaws|1975\nThe Exorcist|1973\nET|1982\nAliens|1986\nTerminator|1984\nBlade Runner|1982\nThe Thing|1982\nJurassic Park|1993\nThe Matrix|1999\n\n\n###\n\n\nA spreadsheet of hurricane and tropical storm counts with 13 columns:\n\n\n\"Month\"| \"Average\"| \"2005\"| \"2006\"| \"2007\"| \"2008\"| \"2009\"| \"2010\"| \"2011\"| \"2012\"| \"2013\"| \"2014\"| \"2015\"\n\"May\"|  0.1|  0|  0| 1| 1| 0| 0| 0| 2| 0|  0|  0  \n\"Jun\"|  0.5|  2|  1| 1| 0| 0| 1| 1| 2| 2|  0|  1\n\"Jul\"|  0.7|  5|  1| 1| 2| 0| 1| 3| 0| 2|  2|  1\n\"Aug\"|  2.3|  6|  3| 2| 4| 4| 4| 7| 8| 2|  2|  3\n\"Sep\"|  3.5|  6|  4| 7| 4| 2| 8| 5| 2| 5|  2|  5\n\"Oct\"|  2.0|  8|  0| 1| 3| 2| 5| 1| 5| 2|  3|  0\n\"Nov\"|  0.5|  3|  0| 0| 1| 1| 0| 1| 0| 1|  0|  1\n\"Dec\"|  0.0|  1|  0| 1| 0| 0| 0| 0| 0| 0|  0|  1\n    \n###\n\n\nA single column spreadsheet of days of the week:\n\n\nDay|\nMonday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday\n\n\n###\n\n\n" + question +":",
  temperature=0.3,
  max_tokens=100,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["/n"]
)

print(response.choices[0].text)
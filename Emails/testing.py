string = "Hey! What's up?"
characters = "'!?"

for x in range(len(characters)):
    string = string.replace(characters[x],"")

print(string)
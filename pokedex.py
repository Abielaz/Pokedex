import requests
import json
from rich import print

while True:
  decision = input ("1.Shall You Choose A Pokemon?! \n2. Quit?\n")
  if decision == "1":
    pokemon = input ("Which Pokemon Shall You Search?\n").lower() # takes input and makes it lowercase for API as it's case-senstive
    api = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
    if api.status_code == 200: #checks with API if there is an active page for input
      data = json.loads(api.text) #parses json from API
      print(f"You Chose {data['name'].capitalize()}!")

      for stat in data["stats"] [0:3]: #lists first 3 stats from json
        print (stat["stat"] ["name"].capitalize(), stat["base_stat"])

      moreInfo = input("Want To Learn More? Y or N...\n")
      if moreInfo in ["Y","y"]:
        for ability in data["abilities"]:
          print ("Abilities:", ability ["ability"] ["name"])

    else:
      print(f"{pokemon} Not Found!")

  elif decision =="2":
    print("Thank You For Stopping By!")
    break
  else:
    print("Invalid Input!")

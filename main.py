print("Jay was here ☺")
print("Ismail says hi")
print("Griffin says hey")
print("Wuilmer was here.")
print("John is late, but here")

import requests
import json
# Function one

def get_pokemon_info(pokemon_list):

    try:
        with open("pokedex.json", "r", encoding="utf-8") as read_file:
            pokedex_data = json.load(read_file)
    except:
        print("There was no json file called \"pokedex\" or file was empty, fixed")
        pokedex_data = {}

    for pokemon in pokemon_list:
        if not pokedex_data.get(pokemon):
            print(f"{pokemon} was not in json")
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
            response = requests.get(url)
            if response.status_code == 200:
                pokemon_data = response.json()

                pokedex_data[pokemon_data["name"]] = {
                    "hp": int(pokemon_data["stats"][0]["base_stat"]),
                    "basic_attack": int(pokemon_data["stats"][1]["base_stat"]),
                    "defense": int(pokemon_data["stats"][2]["base_stat"]),
                    "types": [types["type"]["name"] for types in pokemon_data["types"]]}

                    # [type_data["type"]["name"] for type_data in pokemon_data["types"]]
    with open("pokedex.json", 'w', encoding='utf-8') as write_file:
        json.dump(pokedex_data, write_file, indent=2)

pokemons = ["pikachu", "bibarel"]
get_pokemon_info(pokemons)

# Function two

# Function three

# Function Four

# Function Five

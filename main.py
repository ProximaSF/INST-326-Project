import requests
import json
import random

'''print("Jay was here ☺")
print("Ismail says hi")
print("Griffin says hey")
print("Wuilmer was here.")
print("John is late, but here")'''

# Function one
def get_pokemon_info(selected_pokemon, num_pokemon):
    try:
        with open("pokedex.json", "r", encoding="utf-8") as read_file:
            pokedex_data = json.load(read_file)
    except:
        print("There was no json file called \"pokedex\" or file was empty, fixing...")
        pokedex_data = {}

    print("Please wait, gathering data...")
    def moves(moves_list):
        # print(moves_list)
        num_moves = 4
        valid_moves_list = []
        for move_data in moves_list[:num_moves]:  # move_data is a dictionary
            move_name = move_data["move"]["name"]
            move_url = move_data["move"]["url"]
            response = requests.get(move_url)
            if response.status_code == 200:
                power_pokemon_data = response.json()
                if power_pokemon_data["power"]:
                    add_move = {move_name: int(power_pokemon_data["power"])}
                    valid_moves_list.append(add_move)
                else:
                    #print(f"{move_name} deal zero damage")
                    pass
        return valid_moves_list

    def johto_pokemons():
        pokemon_johto_generations_url = "https://pokeapi.co/api/v2/pokedex/3/"
        response = requests.get(pokemon_johto_generations_url)
        if response.status_code == 200:
            johto_data = response.json()
            johto_pokemon_list = [pokemon["pokemon_species"]["name"] for pokemon in johto_data["pokemon_entries"]]
            #pokemon = random.choice(johto_pokemon_list)
            #print(f"chose: {pokemon}")
            return johto_pokemon_list

    selected_pokedex_data = {}
    def selected_pokemon_dict():
        url = f"https://pokeapi.co/api/v2/pokemon/{selected_pokemon.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            pokemon_data = response.json()

            moves_list = pokemon_data["moves"] # list of data for each move
            selected_pokedex_data[pokemon_data["name"]] = {
                "hp": int(pokemon_data["stats"][0]["base_stat"]),
                "basic_attack": int(pokemon_data["stats"][1]["base_stat"]),
                "defense": int(pokemon_data["stats"][2]["base_stat"]),
                "types": [types["type"]["name"] for types in pokemon_data["types"]],
                "moves": moves(moves_list)
            }
        return selected_pokedex_data

    def pokedex_dict():
        other_pokemons = {}
        pokemon_names = johto_pokemons()
        for i in range(num_pokemon):
            picked_pokemon_name = random.choice(pokemon_names)
            pokemon_names.remove(picked_pokemon_name)
            if not pokedex_data.get(picked_pokemon_name):
                #print(f"{picked_pokemon_name} was not in json")
                url = f"https://pokeapi.co/api/v2/pokemon/{picked_pokemon_name.lower()}"
                response = requests.get(url)
                if response.status_code == 200:
                    # print("Passed pokedex_dict response")
                    pokemon_data = response.json()

                    moves_list = pokemon_data["moves"] # list of data for each move

                    pokedex_data[pokemon_data["name"]] = {
                        "hp": int(pokemon_data["stats"][0]["base_stat"]),
                        "basic_attack": int(pokemon_data["stats"][1]["base_stat"]),
                        "defense": int(pokemon_data["stats"][2]["base_stat"]),
                        "types": [types["type"]["name"] for types in pokemon_data["types"]],
                        "moves": moves(moves_list)
                    }
                    other_pokemons[picked_pokemon_name] = pokedex_data[picked_pokemon_name]
            else:
                other_pokemons[picked_pokemon_name] = pokedex_data[picked_pokemon_name]

        with open("pokedex.json", 'w', encoding='utf-8') as write_file:
            json.dump(pokedex_data, write_file, indent=2)
        return other_pokemons

    return selected_pokemon_dict(), pokedex_dict()

selected_pokemon = "pikachu"
num_pokemon = random.randrange(54, 180, step=18)
print(f"{num_pokemon} different Pokemons will fight {selected_pokemon.capitalize()} one at a time")

selected, others = get_pokemon_info(selected_pokemon, num_pokemon)
print(selected)
print("===================================================")
print(others)


# Function two

# Function three

# Function Four

# Function Five

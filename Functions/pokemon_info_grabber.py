import json
import requests
import random

def get_pokemon_info(selected_pokemon, num_pokemon, johto_pokemons):
    try:
        with open("pokedex.json", "r", encoding="utf-8") as read_file:
            pokedex_data = json.load(read_file)
    except:
        print("There was no json file called \"pokedex\" or file was empty, fixing...")
        pokedex_data = {}
    print("Please wait, gathering data...")

    def get_store_pokemon(pokemon_name):
        if not pokedex_data.get(pokemon_name):
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
            response = requests.get(url)
            if response.status_code == 200:
                pokemon_data = response.json()
                moves_list = pokemon_data["moves"]
                pokedex_data[pokemon_name] = {
                    "hp": int(pokemon_data["stats"][0]["base_stat"]),
                    "basic_attack": int(pokemon_data["stats"][1]["base_stat"]),
                    "defense": int(pokemon_data["stats"][2]["base_stat"]),
                    "types": [type["type"]["name"] for type in pokemon_data["types"]],
                    "moves": add_moves(moves_list)
                }
        return pokedex_data.get(pokemon_name, {})


    selected_pokedex_data = {selected_pokemon: get_store_pokemon(selected_pokemon)}

    other_pokemons_data = {}
    pokemon_names = johto_pokemons[:]
    for i in range(num_pokemon):
        picked_pokemon_name = random.choice(pokemon_names)
        pokemon_names.remove(picked_pokemon_name)
        other_pokemons_data[picked_pokemon_name] = get_store_pokemon(picked_pokemon_name)

    with open("pokedex.json", "w", encoding='utf-8') as write_file:
        json.dump(pokedex_data, write_file, indent=2)

    return selected_pokedex_data, other_pokemons_data

def add_moves(moves_list):
    # print(moves_list)
    valid_moves_list = []
    for move_data in moves_list:  # move_data is a dictionary
        if len(valid_moves_list) != 4:
            move_version = move_data["version_group_details"][0]["version_group"]["url"]
            #print(move_version)
            if "version-group/3/" in move_version:
                #print(True)
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

def johto_pokemons_and_types():
    pokemon_list = []
    pokemon_types_list = []
    pokemon_urls = ["https://pokeapi.co/api/v2/pokedex/3/", "https://pokeapi.co/api/v2/type/"]
    for i, link in enumerate(pokemon_urls):
        response = requests.get(link)
        if response.status_code == 200:
            data = response.json()
            if i == 1:
                pokemon_types_list = [type["name"] for type in data["results"]]
                remove_type = ["unknown", "stellar"]
                pokemon_types_list = [type for type in pokemon_types_list if type not in remove_type]
            else:
                pokemon_list = [pokemon["pokemon_species"]["name"] for pokemon in data["pokemon_entries"]]
    return pokemon_list, pokemon_types_list
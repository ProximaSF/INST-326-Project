print("Jay was here ☺")
print("Ismail says hi")
print("Griffin says hey")
print("Wuilmer was here.")
print("John is late, but here")

# Function one
def get_pokemon_info(pokemon_list):
    try:
        with open("pokedex.json", "r", encoding="utf-8") as read_file:
            pokedex_data = json.load(read_file)
    except:
        print("There was no json file called \"pokedex\" or file was empty, fixed")
        pokedex_data = {}

    def moves(moves_list):
        # print(moves_list)
        num_moves = 10
        valid_moves_list = []
        for move_data in moves_list[:num_moves]:  # move_data is a dictionary
            move_name = move_data["move"]["name"]
            move_url = move_data["move"]["url"]
            response = requests.get(move_url)
            if response.status_code == 200:
                power_pokemon_data = response.json()
                if power_pokemon_data["power"] == None:
                    print(f"{move_name} deal zero damage")
                else:
                    add_move = {move_name: int(power_pokemon_data["power"])}
                    valid_moves_list.append(add_move)
        return valid_moves_list

    for pokemon in pokemon_list:
        if not pokedex_data.get(pokemon):
            print(f"{pokemon} was not in json")
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
            response = requests.get(url)
            if response.status_code == 200:
                pokemon_data = response.json()

                moves_list = pokemon_data["moves"] # list of data for each move

                pokedex_data[pokemon_data["name"]] = {
                    "hp": int(pokemon_data["stats"][0]["base_stat"]),
                    "basic_attack": int(pokemon_data["stats"][1]["base_stat"]),
                    "defense": int(pokemon_data["stats"][2]["base_stat"]),
                    "types": [types["type"]["name"] for types in pokemon_data["types"]],
                    "moves": moves(moves_list)
                }

                    # [type_data["type"]["name"] for type_data in pokemon_data["types"]]
    with open("pokedex.json", 'w', encoding='utf-8') as write_file:
        json.dump(pokedex_data, write_file, indent=2)

pokemons = ["pikachu", "bibarel"]
get_pokemon_info(pokemons)

# Function two

# Function three

# Function Four

# Function Five

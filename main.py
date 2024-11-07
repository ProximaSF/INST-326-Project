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
import random

def battle_simulation(selected_pokemon, opponent_pokemon, num_simulations=10):
    selected_data = pokedex_data.get(selected_pokemon.lower())
    opponent_data = pokedex_data.get(opponent_pokemon.lower())
    if not selected_data or not opponent_data:
        print(f"Missing data for {selected_pokemon} or {opponent_pokemon}")
        return None

#Stats for selected pokemon
    selected_hp = selected_data["hp"]
    selected_attack = selected_data["basic_attack"]
    selected_defense = selected_data["defense"]
    selected_moves = selected_data["moves"]

#Stats for opponents pokemon
    opponent_hp = opponent_data["hp"]
    opponent_attack = opponent_data["basic_attack"]
    opponent_defense = opponent_data["defense"]
    opponent_moves = opponent_data["moves"]

#Types for said pokemon
    selected_type = selected_data["types"]
    opponent_type = opponent_data["types"]

#Win Counter
    selected_wins = 0
    opponent_wins = 0
    for _ in range(num_simulations):
        selected_pokemon_hp = selected_hp
        opponent_pokemon_hp = opponent_hp
        
#Start battle set
        while selected_pokemon_hp > 0 and opponent_pokemon_hp > 0:

#Selected Pokémon attacks first
            damage_to_opponent = selected_attack - (opponent_defense / 2)
            opponent_pokemon_hp -= max(damage_to_opponent, 0)
            if opponent_pokemon_hp <= 0:
                selected_wins += 1
                break

#Opponent Pokémon attacks
            damage_to_selected = opponent_attack - (selected_defense / 2)
            selected_pokemon_hp -= max(damage_to_selected, 0)
            if selected_pokemon_hp <= 0:
                opponent_wins += 1
                break

#Calculate win rate
    win_rate = selected_wins / num_simulations
    return win_rate, selected_wins, opponent_wins

#Tracks results against several pokemon
def battle_against_all(selected_pokemon, all_opponents, num_simulations=10):
    types_score = {}
    win_count = 0
    total_battles = 0
    battle_results = []

#Stats for battles
    for opponent in all_opponents:
        print(f"Simulating battles: {selected_pokemon} vs {opponent}")
        win_rate, selected_wins, opponent_wins = battle_simulation(selected_pokemon, opponent, num_simulations)

        battle_results.append({
            "opponent": opponent,
            "win_rate": win_rate,
            "selected_wins": selected_wins,
            "opponent_wins": opponent_wins
        })
        
#Track win or loss to type score
        if selected_wins < opponent_wins:

#If the selected Pokemon lost, update the types_score
            opponent_data = pokedex_data.get(opponent.lower())
            if opponent_data:
                for opponent_type in opponent_data["types"]:
                    if opponent_type not in types_score:
                        types_score[opponent_type] = 0
                    types_score[opponent_type] += 1
            print(f"{selected_pokemon} lost to {opponent}. Type win tally updated.")

#Accumulate win rate and track total battles
        win_count += selected_wins
        total_battles += num_simulations

#Calculate the mean win rate
    mean_win_rate = win_count / total_battles
    print(f"\nThe simulation has finished for {selected_pokemon}. It's overall win rate was {mean_win_rate}")
    
#Determine which type is most effective (based on losses)
    if types_score:
        most_effective_type = max(types_score, key=types_score.get)
        print(f"Most effective type against {selected_pokemon} is {most_effective_type}. Earned a score of {types_score[most_effective_type]})")

    return battle_results, mean_win_rate, types_score
# Function three

# Function Four

# Function Five

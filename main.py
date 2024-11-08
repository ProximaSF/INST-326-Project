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
            #print(len(johto_pokemon_list))
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

    def opponent_pokedex_dict():
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

    return selected_pokemon_dict(), opponent_pokedex_dict()

# Function two
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
type_advantage = {
    "fire": {"grass": 2, "water": 0.5, "fire": 1},
    "water": {"fire": 2, "electric": 0.5, "water": 1},
    "grass": {"water": 2, "fire": 0.5, "grass": 1},
    # Add additional types as needed
}

def calculate_damage(attacker, defender):
    """
    Calculates damage output in a turn-based battle between two Pokemon based on type effectiveness and defense.

    Parameters:
    - attacker (dict): Dictionary with 'basic_attack', 'types', and 'moves' for the attacking Pokemon.
    - defender (dict): Dictionary with 'defense' and 'types' for the defending Pokemon.

    Returns:
    - float: The damage dealt to the defender.
    """
    attacker_attack = attacker["basic_attack"]
    defender_defense = defender["defense"]
    attacker_type = attacker["types"][0] if attacker["types"] else "normal"
    defender_type = defender["types"][0] if defender["types"] else "normal"
    
    # effectiveness multiplier is based on matchup type
    effectiveness = type_advantage.get(attacker_type, {}).get(defender_type, 1)
    
    damage = (attacker_attack - defender_defense / 2) * effectiveness
    return max(damage, 0)  # Prevents negative damage

# Function Four
def probability_calculation(selected_data, opponent_data ):
    hp_prob = selected_data["hp"] / (selected_data["hp"] + opponent_data["hp"])
    attack_prob = selected_data["basic_attack"] / (selected_data["basic_attack"] + opponent_data["basic_attack"])
    defense_prob = selected_data["defense"] / (selected_data["defense"] + opponent_data["defense"])

    combined_prob = (hp_prob + attack_prob + defense_prob) / 3
    return combined_prob
def combined_distrubution_simulation(selected_pokemon, opponent_pokemon, num_simulations = 100):
    selected_data = pokedex_data.get(selected_pokemon.lower())
    opponent_data = pokedex_data.get(opponent_pokemon.lower())
    if not selected_data or not opponent_data:
        raise ValueError (f"Data missing for {selected_data} or {opponent_data}")
    combined_prob = probability_calculation(selected_data, opponent_data)
    win_count = 0 
    for _ in range(num_simulations):
        if random.uniform(0,1) < combined_prob:
            win_count += 1
    win_probability = win_count / num_simulations       
    print(f"The probability for {selected_pokemon.upper()} against {opponent_pokemon.upper()} is :{win_probability}")
    return win_probability
# Function Five

if __name__ == "__main__":
    selected_pokemon = "pikachu"
    num_pokemon = random.randrange(54, 180, step=18)
    print(f"{num_pokemon} different Pokemons will fight {selected_pokemon.capitalize()} one at a time")

    selected_pokemon, opponent_pokemons = get_pokemon_info(selected_pokemon, num_pokemon)
    print(selected_pokemon)
    print("===========================================================================================")
    print(opponent_pokemons)
    print(f"\nPoekmons chosed: {[pokemon.capitalize() for pokemon in opponent_pokemons]}")

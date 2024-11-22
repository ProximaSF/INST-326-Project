import json
import random
import sys
from argparse import ArgumentParser

'''print("Jay was here ☺")
print("Ismail says hi")
print("Griffin says hey")
print("Wuilmer was here.")
print("John is late, but here")'''



# Function One - Jay
from Functions.pokemon_info_grabber import get_pokemon_info, johto_pokemons_and_types

get_pokemon_info_instance = get_pokemon_info
get_type_and_johto_pokemons_instance = johto_pokemons_and_types
# ----------------------------------------------------------------------------------------------------------


# Function Two - Griffin
def battle_simulation(selected_pokemon, opponent_pokemon, num_simulations):
    with open("pokedex.json", 'r', encoding='utf-8') as file:
        pokedex_data = json.load(file)

    # print(selected_pokemon)
    # print(opponent_pokemon)

    selected_data = pokedex_data.get(selected_pokemon)
    opponent_data = pokedex_data.get(opponent_pokemon)
    if not selected_data or not opponent_data:
        print(f"Missing data for {selected_pokemon} or {opponent_pokemon}")
        return None

    # Stats for selected pokemon
    selected_hp = selected_data["hp"]
    selected_defense = selected_data["defense"]
    selected_attack = selected_data["basic_attack"]
    selected_moves = selected_data["moves"]


    # Stats for opponents pokemon
    opponent_hp = opponent_data["hp"]
    opponent_defense = selected_data["defense"]
    opponent_attack = opponent_data["basic_attack"]
    opponent_moves = opponent_data["moves"]

    # Selected combined status for defense, basic_attack and moves
    selected_DBM_stats = (selected_defense, selected_attack, selected_moves)
    # Selected combined status for defense, basic_attack and moves
    opponent_DBM_stats = (opponent_defense, opponent_attack, opponent_moves)

    # Type stats for both opponents
    both_opponent_types = (selected_data["types"], opponent_data["types"])

    # Win Counter
    selected_wins = 0
    opponent_wins = 0
    for _ in range(num_simulations):
        selected_pokemon_hp = selected_hp
        opponent_pokemon_hp = opponent_hp

        # Start battle set
        while selected_pokemon_hp > 0 and opponent_pokemon_hp > 0:

            # Selected Pokémon attacks first
            damage_inflict = damage(selected_DBM_stats, both_opponent_types)
            opponent_pokemon_hp -= damage_inflict
            if opponent_pokemon_hp <= 0:
                selected_wins += 1
                break

            # Opponent Pokémon attacks
            damage_inflict = damage(opponent_DBM_stats, both_opponent_types)
            selected_pokemon_hp -= damage_inflict
            if selected_pokemon_hp <= 0:
                opponent_wins += 1
                break

    # Calculate win rate
    win_rate = selected_wins / num_simulations
    return win_rate, selected_wins, opponent_wins

# Tracks results against several pokemon
def battle_against_all(selected_pokemon, all_opponents, num_simulations=90):
    types_score = {}
    win_count = 0
    total_battles = 0
    battle_results = []

    # Stats for battles
    for opponent in all_opponents:
        # print(f"Simulating battles: {selected_pokemon} vs {opponent}")
        win_rate, selected_wins, opponent_wins = battle_simulation(selected_pokemon, opponent, num_simulations)

        battle_results.append({
            "opponent": opponent,
            "win_rate": round(win_rate, 2),
            "selected_wins": selected_wins,
            "opponent_wins": opponent_wins
        })

        # Track win or loss to type score
        if selected_wins < opponent_wins:

            # If the selected Pokemon lost, update the types_score
            opponent_data = all_opponents.get(opponent)
            if opponent_data:
                for opponent_type in opponent_data["types"]:
                    if opponent_type not in types_score:
                        types_score[opponent_type] = 0
                    types_score[opponent_type] += 1
            # print(f"{selected_pokemon} lost to {opponent}. Type win tally updated.")

        # Accumulate win rate and track total battles
        win_count += selected_wins
        total_battles += num_simulations

    # Calculate the mean win rate
    mean_win_rate = win_count / total_battles
    # print(f"\nThe simulation has finished for {selected_pokemon}. It's overall win rate was {mean_win_rate}")

    # Determine which type is most effective (based on losses)
    if types_score:
        most_effective_type = max(types_score, key=types_score.get)
        # print(f"Most effective type against {selected_pokemon} is {most_effective_type}. Earned a score of {types_score[most_effective_type]})")

    return battle_results, mean_win_rate, types_score
# ----------------------------------------------------------------------------------------------------------


# Function Three - Ismail
type_advantage = {  # Type advantages as of gen 6
    "fire": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2},
    "water": {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5},
    "grass": {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5,
              "rock": 2, "dragon": 0.5, "steel": 0.5},
    "normal": {"rock": 0.5, "ghost": 0, "steel": 0.5},
    "electric": {"water": 2, "grass": 0.5, "electric": 0.5, "ground": 0, "flying": 2, "dragon": 0.5},
    "ice": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "steel": 0.5},
    "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2,
                 "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5},
    "poison": {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2},
    "ground": {"fire": 2, "grass": 0.5, "electric": 2, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
    "flying": {"grass": 2, "electric": 0.5, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5},
    "bug": {"fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5,
            "dark": 2, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5},
    "ghost": {"normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5},
    "dragon": {"dragon": 2, "steel": 0.5, "fairy": 0},
    "dark": {"fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5},
    "steel": {"fire": 0.5, "water": 0.5, "ice": 0.5, "fighting": 2, "rock": 2, "steel": 0.5, "fairy": 2},
    "fairy": {"fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5}
}

def damage(DBM_stats, types_info):
    defence = DBM_stats[0]
    basic_attack = DBM_stats[1]
    moves = DBM_stats[2]

    # Calculate dmg based on type match up and defense
    def calculate_damage(attack, defence):
        pass


    pick_basic_attack = random.random() # Maybe replace it with an energy system later on
    if pick_basic_attack >= 0.6:
        return calculate_damage(basic_attack, defence) or basic_attack/3
    if moves:
        move_type = random.choice(moves)
        move_damage = next(iter(move_type.values()))  # get the first value in iteration
        return calculate_damage(move_damage, defence) or move_damage/3
    else:
        return 0
# ----------------------------------------------------------------------------------------------------------


# Function Four - Wuilmer
def combined_distrubution_simulation(selected_pokemon, opponent_pokemon, pokedex_data, num_simulations=100):
    def probability_calculation(selected_data, opponent_data):
        hp_prob = selected_data["hp"] / (selected_data["hp"] + opponent_data["hp"])
        attack_prob = selected_data["basic_attack"] / (selected_data["basic_attack"] + opponent_data["basic_attack"])
        defense_prob = selected_data["defense"] / (selected_data["defense"] + opponent_data["defense"])

        combined_prob = (hp_prob + attack_prob + defense_prob) / 3
        return combined_prob

    selected_data = pokedex_data.get(selected_pokemon.lower())
    opponent_data = pokedex_data.get(opponent_pokemon.lower())
    if not selected_data or not opponent_data:
        raise ValueError(f"Data missing for {selected_data} or {opponent_data}")
    combined_prob = probability_calculation(selected_data, opponent_data)
    win_count = 0
    for _ in range(num_simulations):
        if random.uniform(0, 1) < combined_prob:
            win_count += 1
    win_probability = win_count / num_simulations
    #print(f"The probability for {selected_pokemon.upper()} against {opponent_pokemon.upper()} is :{win_probability}")
    return win_probability
# ----------------------------------------------------------------------------------------------------------


# Function Five - John
def advantage_probability(selected_pokemon, opponent_pokemon, type_advantage):
    # Type Advantage
    total_multiplier = 1.0
    selected_types = selected_pokemon['types']
    opponent_types = opponent_pokemon['types']
    for s_type in selected_types:
        for o_type in opponent_types:
            multiplier = type_advantage.get(s_type, {}).get(o_type, 1.0)
            total_multiplier *= multiplier
    num_comparisons = len(selected_types) * len(opponent_types)
    average_multiplier = total_multiplier ** (1 / num_comparisons) if num_comparisons > 0 else 1
    type_score = average_multiplier
    type_probability = max(0, min(1, (type_score + 2) / 4))

    # Stat Advantage 
    hp_ratio = selected_pokemon['hp'] / opponent_pokemon['hp']
    defense_ratio = selected_pokemon['defense'] / opponent_pokemon['defense']
    stat_score = (hp_ratio + defense_ratio) / 2
    stat_probability = max(0, min(1, stat_score / 2))

    # Combined
    combined_probability = (0.6 * type_probability) + (0.4 * stat_probability)
    return combined_probability
# ----------------------------------------------------------------------------------------------------------

# Other Functions
def main(selected_pokemon, num_opponents):
    pokemon_list, pokemon_types_list = get_type_and_johto_pokemons_instance()
    pokemon_list_copy = pokemon_list.copy()  # For msg use only to ensure 251 Pokemons for Johto region

    selected_pokemon = selected_pokemon.lower()
    if selected_pokemon not in pokemon_list:
        print(f"{selected_pokemon} is not a Pokemon, check the spelling")
        return

    if int(num_opponents) < 54 or int(num_opponents) > 251:
        print(f"{"-------"*10}\n"
              "Pick a number of Pokemon used in battle between 54-251\n"
              "Don't need to be exact, will be rounded to value that is evenly dividable by 18\n"
              f"{"-------"*10}\n")
        return
    else:
        num_opponents = (int(num_opponents) // 18) * 18

    # selected_pokemon = "pikachu"
    # num_opponents = random.randrange(54, 180, step=18)

    selected_pokemon_pokedex, opponent_pokemons_pokedex = get_pokemon_info_instance(selected_pokemon, num_opponents,
                                                                                    pokemon_list)
    battle_results, mean_win_rate, types_score = battle_against_all(selected_pokemon, opponent_pokemons_pokedex)
    sorted_type_score = sorted(types_score.items(), key=lambda s: s[1], reverse=True)
    most_effective = [type for type in sorted_type_score if
                      type[1] == max(sorted_type_score, key=lambda m: sorted_type_score[1])[1]]
    
    probability_results = []
    for opponent in opponent_pokemons_pokedex:
        win_probability = combined_distrubution_simulation(
            selected_pokemon,
            opponent,
            {**selected_pokemon_pokedex, **opponent_pokemons_pokedex}
        )
        probability_results.append((opponent, win_probability))

    line_break = "↔↔↔↔↔↔" * 18
    msg = (f"Pokemon Types: \n{pokemon_types_list}\n\n"  # Unknown and stellar removed
           f"{line_break}\n"
           f"Selected Pokemon Info: \n{selected_pokemon_pokedex}\n\n"
           f"{line_break}\n"
           f"There are {len(pokemon_list_copy)} Pokemon from Johto\n{pokemon_list_copy}\n\n"  # This should reflect 251
           f"{line_break}\n"
           f"{num_opponents} different Pokemons fought {selected_pokemon.capitalize()} one at a time\n\n"
           f"Pokmons used in battles: \n{[pokemon.capitalize() for pokemon in opponent_pokemons_pokedex]}\n\n"
           f"{line_break}\n"
           f"Simulation Result: \n{battle_results}\n\n"
           f"{line_break}\n"
           f"Won about {round(mean_win_rate*100, 2)}% of the battles.\n{sorted_type_score}\n"
           f"Was least effective against {most_effective}\n"
           f"{line_break}\n"
           f"Win Probabilities:\n")

    #prints msg
    '''for opponent, probability in probability_results:
        msg += f"- Probability of winning against {opponent.capitalize()}: {round(probability * 100, 2)}%\n"'''

    print(probability_results)
    print("---"*30)
    compare_result = {}
    i = 0
    for pokemon in battle_results:
        simulation1_pokemon = pokemon["opponent"]
        simulation1_win_rate = pokemon["win_rate"]
        simulation2_win_rate = probability_results[i][1]
        compare_result[simulation1_pokemon] = f"({round(simulation1_win_rate * 100, 2)}%, {round(simulation2_win_rate * 100, 2)}%)"
        i += 1
    msg += str(compare_result)

    
    with open("result.txt", 'w', encoding="utf-8") as file: 
        file.write(msg)
    print(f"Created/updated result.txt\n{line_break}\n")

def parse_args(arglist):
    parser = ArgumentParser()
    parser.add_argument("selected_pokemon", help="The main Pokemon that will be simulated")
    parser.add_argument("number_opponents", help="The number of unique Pokemons to simulate")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.selected_pokemon, args.number_opponents)

    # Example in the console ↓ (windows):
    # python .\main.py "pikachu" 53

    # https://www.thegamer.com/pokemon-gold-silver-strongest-generation-2-ii-stats/
    # https://www.thegamer.com/weakest-johto-pokemon-ranked/

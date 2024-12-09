""" Two different Pokemon simulation to determine their effectiveness against other Pokemons

Attributes:
    LETTER_TO_NUMBER (dict): a dictionary contains all Pokemon types (keys) from second generation and their effectiveness
    value against certain types (value).
"""
import json
import random
import sys
from argparse import ArgumentParser

from pokemon_info_grabber import get_pokemon_info, johto_pokemons_and_types

TYPE_ADVANTAGES = {
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

class PokemonSimulationOne():
    """ First simulation (parent class) that uses turn-based mechanics to simulate each battle

    Attributes:
        selected_pokemon_name (str): The name of the Pokemon selected by the user to be used in the simulation against
        other Pokemons
        num_opponents (int): The number of unique Pokemons will be used to fight against the selected Pokemon
        num_simulations (int): The number of time(s) each battle will simulate

    Author: Jay Walter, Griffin Biddle & Ismail Touray
    """
    def __init__(self, selected_pokemon, num_opponents, num_simulations):
        """ Initialize the PokemonSimulationOne Class

        Args:
            selected_pokemon (str): The name of the Pokemon will be used in the simulation against others
            num_opponents (int): The number of Pokemons will be used to battle the selected Pokemon
            num_simulations (int): The number of battles for each will occur

        Side effects:
            • Converting the selected_pokemon_name attribute to all lowercase string
            • Assigning attributes (selected_pokemon_name, num_opponents, num_simulations)

        Author: Jay Walter
        """
        self.selected_pokemon_name = selected_pokemon.lower()
        self.num_opponents = num_opponents
        self.num_simulations = num_simulations

    def get_info(self):
        """ Gather and return Pokemon information needed for the simulation

        Returns:
            Pokemon information that will be used for the simulation.
            all_pokemon_list (list): A list of all Pokemon found the PokeAPI for generation two
            all_pokemon_types_list (list): All Pokemon types found in PokeAPI for generation two
            selected_pokemons_data_dict (dict): A dictionary about the selected pokemon (key) and its information gathered

        Author: Jay Walter
        """
        get_johto_pokemons_and_types_instance = johto_pokemons_and_types
        all_pokemon_list, all_pokemon_types_list = get_johto_pokemons_and_types_instance()
        get_pokemon_info_instance = get_pokemon_info
        selected_pokemons_data_dict, opponent_pokemon_names_data_dict = get_pokemon_info_instance(self.selected_pokemon_name, self.num_opponents, all_pokemon_list)
        return all_pokemon_list, all_pokemon_types_list, selected_pokemons_data_dict, opponent_pokemon_names_data_dict

    def battle_simulation(self, opponent_pokemon_name):
        """ Simulate multiples battles between a chosen pokemon and opponent pokemon

        Args: 
            opponent_pokemon_name (str): Opponent pokemons name

        Returns:
            tuple: A tuple that contains:
                • selected_wins (int): The number of wins earned by the chosen pokemon
                • opponent_wins (int): The number of wins earned by the opponent pokemon
                • win_rate (float): The win rate of the chosen pokemon across the simulations
       
        Side effects:
            • Opens and reads the pokedex.json file
            • Prints error messages if pokemon data is missing
        
        Author: Griffin Biddle

        Techniques: f-strings
        """
        with open("pokedex.json", 'r', encoding='utf-8') as file:
            pokedex_data = json.load(file)

        # print(selected_pokemon)
        # print(opponent_pokemon_name)

        selected_data = pokedex_data.get(self.selected_pokemon_name)
        opponent_data = pokedex_data.get(opponent_pokemon_name)
        if not selected_data or not opponent_data:
            print(f"Missing data for {self.selected_pokemon_name} or {opponent_pokemon_name}")
            return None

        # Stats for selected pokemon
        selected_hp = selected_data["hp"]
        selected_defense = selected_data["defense"]
        selected_attack = selected_data["basic_attack"]
        selected_moves = selected_data["moves"]

        # Stats for opponents pokemon
        opponent_hp = opponent_data["hp"]
        opponent_defense = opponent_data["defense"]
        opponent_attack = opponent_data["basic_attack"]
        opponent_moves = opponent_data["moves"]

        # Selected combined status for defense, basic_attack and moves
        selected_DBM_stats = (selected_defense, selected_attack, selected_moves)
        # Selected combined status for defense, basic_attack and moves
        opponent_DBM_stats = (opponent_defense, opponent_attack, opponent_moves)

        # Type stats for both opponents
        both_opponent_types = (selected_data["types"], opponent_data["types"])

        #print("A:" + self.selected_pokemon_name + str(selected_DBM_stats))
        #print("B:" + opponent_pokemon_name + str(opponent_DBM_stats))
        #print("C:" + str(both_opponent_types))

        # Win Counter
        selected_wins = 0
        opponent_wins = 0
        num_simulations = self.num_simulations
        for _ in range(num_simulations):
            selected_pokemon_hp = selected_hp
            opponent_pokemon_name_hp = opponent_hp

            # Start battle set
            while selected_pokemon_hp > 0 and opponent_pokemon_name_hp > 0:

                pokemon_name = self.selected_pokemon_name
                # Selected pokemon attacks first
                damage_inflict = self.damage(pokemon_name, selected_DBM_stats, opponent_defense, both_opponent_types)
                opponent_pokemon_name_hp -= damage_inflict
                if opponent_pokemon_name_hp <= 0:
                    selected_wins += 1
                    break

                pokemon_name = opponent_pokemon_name
                # Opponent pokemon attacks
                damage_inflict = self.damage(pokemon_name, opponent_DBM_stats, selected_defense, both_opponent_types)
                selected_pokemon_hp -= damage_inflict
                if selected_pokemon_hp <= 0:
                    opponent_wins += 1
                    break

        # Calculate win rate
        win_rate = selected_wins / num_simulations
        return win_rate, selected_wins, opponent_wins

    # Tracks results against several pokemon
    def battle_against_all(self, all_opponents):
        """ Simulates battles between the chosen pokemon and a wide range of other pokemon. Gives results of the battle and success/failures

        Args:
            all_opponents (dict): A dictionary containing the opponent pokemon names and all of their stats
            
        Returns:
            tuple: A tuple containing:
                • battle_results (list of dicts): Listed results for each battle. Each list of results has the following:
                    - opponent (str): The name of the opponent
                    - selected_wins (int): The number of wins earned by the chosen pokemon
                    - opponent_wins (int): The number of wins earned by the opponent pokemon
                    - win_rate (float): The win rate of the chosen pokemon across the simulations
                • mean_win_rate (float): The overall win rate of the chosen pokemon across all simulations
                • types_score (dict): A dictionary that showcases which types had the most and/or lease effect against the chosen
                  pokemon. For this, keys are pokemon types and values are the count for times the selected pokemon lost to said type

        Side effects:
            • Calls on battle_simulation for each opponent in list
            • Updates the types_score dictionary based on battle outcomes

        Author: Griffin Biddle

        Techniques: with statements, json.load
        """
        types_score = {}
        win_count = 0
        total_battles = 0
        battle_results = []

        # Stats for battles
        for opponent in all_opponents:
            # print(f"Simulating battles: {selected_pokemon} vs {opponent}")
            win_rate, selected_wins, opponent_wins = self.battle_simulation(opponent)

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
            total_battles += self.num_simulations

        # Calculate the mean win rate
        mean_win_rate = win_count / total_battles
        # print(f"\nThe simulation has finished for {selected_pokemon}. It's overall win rate was {mean_win_rate}")

        # Determine which type is most effective (based on losses)
        if types_score:
            most_effective_type = max(types_score, key=types_score.get)
            # print(f"Most effective type against {selected_pokemon} is {most_effective_type}. Earned a score of {types_score[most_effective_type]})")

        return battle_results, mean_win_rate, types_score

    def damage(self, pokemon_name, DBM_stats, opponent_defence, both_opponent_types):
        basic_attack = DBM_stats[1]
        moves = DBM_stats[2]

        # print(f"A: {pokemon_name, defence, basic_attack, moves, both_opponent_types}")

        # Calculate dmg based on type match up and defense
        def calculate_damage(move_damage):
            meh = True
            level = 1
            attacker_type = both_opponent_types[0] if pokemon_name == self.selected_pokemon_name else both_opponent_types[1]
            attacker_type = next(iter(attacker_type))
            defender_type = both_opponent_types[0] if pokemon_name != self.selected_pokemon_name else both_opponent_types[1]
            defender_type = next(iter(defender_type))

            type_advantage_multiplier = TYPE_ADVANTAGES[attacker_type].get(defender_type, 1)

            if meh:
                output = (((((2*level/5) + 2) * move_damage * (basic_attack / opponent_defence)) / 50) + 2) * type_advantage_multiplier
                #print(f"Output: {output}")
                return int(output)
            else:
                pass

        if moves:
            move_type = random.choice(moves)
            move_damage = next(iter(move_type.values()))  # get the first value in iteration
            return calculate_damage(move_damage) or move_damage / 3
        else:
            return calculate_damage(basic_attack)/4.4


    def print_result(self):
        """ Print information when somthing goes wrong when test simulation and store the final result in a text file

        Returns:
            Returns nothing and exit method if user provides invalid argument in the terminal when starting the simulation

        Side effects:
            • Print information to console when an invalid argument is entered
            • Create a result.txt if do not exist. Update the file in result of each simulation once completed (erase previous simulations)
            • Update attribute num_opponents to a value that's dividable by 18 if not initially.
            • Create a instance of the child class (PokemonSimulationTwo) to run the second simulation

        Author: Jay Walter

        Techniques: Use of lambda in sorted()
        """

        if int(self.num_opponents) < 54 or int(self.num_opponents) > 251:
            print(f"{"-------" * 10}\n"
                  "Pick a number of Pokemon used in battle between 54-251\n"
                  "Don't need to be exact, will be rounded to a value that's dividable by 18\n"
                  f"{"-------" * 10}\n")
            return
        else:
            self.num_opponents = (int(self.num_opponents) // 18) * 18

        all_pokemon_list, all_pokemon_types_list, selected_pokemons_data_dict, opponent_pokemon_data_dict = self.get_info()
        #print(opponent_pokemon_data_dict)
        pokemon_sim_2_instance = PokemonSimulationTwo(self.selected_pokemon_name, self.num_opponents, self.num_simulations)

        pokemon_list_copy = all_pokemon_list.copy()  # For msg use only to ensure 251 Pokemons for Johto region
        selected_pokemon = self.selected_pokemon_name.lower()
        if selected_pokemon not in all_pokemon_list:
            print(f"{selected_pokemon} is not a Pokemon, check the spelling and it's for 2nd gen")
            return

        battle_results, mean_win_rate, types_score = self.battle_against_all(opponent_pokemon_data_dict)
        sorted_type_score = sorted(types_score.items(), key=lambda s: s[1], reverse=True)
        most_effective = [type for type in sorted_type_score if
                          type[1] == max(sorted_type_score, key=lambda m: sorted_type_score[1])[1]]

        probability_results = []
        for opponent in opponent_pokemon_data_dict:
            win_probability = pokemon_sim_2_instance.combined_distrubution_simulation(
                opponent,
                {**selected_pokemons_data_dict, **opponent_pokemon_data_dict})
            probability_results.append((opponent, win_probability))

        line_break = "↔↔↔↔↔↔" * 18
        msg = (f"Pokemon Types: \n{all_pokemon_types_list}\n\n"  # Unknown and stellar removed
               f"{line_break}\n"
               f"Selected Pokemon Info: \n{selected_pokemons_data_dict}\n\n"
               f"{line_break}\n"
               f"There are {len(pokemon_list_copy)} Pokemon from Johto\n{pokemon_list_copy}\n\n"  # This should reflect 251
               f"{line_break}\n"
               f"{self.num_opponents} different Pokemons fought {selected_pokemon.capitalize()} one at a time\n\n"
               f"Pokmons used in battles: \n{sorted([pokemon.capitalize() for pokemon in opponent_pokemon_data_dict])}\n\n"
               f"{line_break}\n"
               f"Simulation 1 Result: \n"
               f"{sorted(battle_results, key=lambda s: s["opponent"])}\n\n"
               f"{line_break}\n"
               f"Won about {round(mean_win_rate * 100, 2)}% of the battles (sim 1).\n{sorted_type_score}\n"
               f"Was least effective against (sim 1) {most_effective}\n\n"
               f"{line_break}\n"
               f"Simulation 2 Result: \n"
               f"{probability_results}\n\n"
               f"{line_break}\n"
               f"Win Probabilities (sim1, sim2):\n")

        #print(probability_results)
        compare_result = {}
        i = 0
        for pokemon in battle_results:
            simulation1_pokemon = pokemon["opponent"]
            simulation1_win_rate = pokemon["win_rate"]
            simulation2_win_rate = probability_results[i][1]
            compare_result[
                simulation1_pokemon] = f"({round(simulation1_win_rate * 100, 2)}%, {round(simulation2_win_rate * 100, 2)}%)"
            i += 1
        msg += str({pokemon_name: compare_result[pokemon_name] for pokemon_name in sorted(compare_result)})

        print(f"Number of Simulations: {self.num_simulations}")
        print(f"Running simulation for {self.selected_pokemon_name}")
        with open("result.txt", 'w', encoding="utf-8") as file:
            file.write(msg)
        print(f"Created/updated result.txt\n{line_break}\n")


class PokemonSimulationTwo(PokemonSimulationOne):
    """ The child class of PokemonSimulationOne, used to simulate the second simulation by using Monte-carlo simulation

    Attributes:
        Same attributes shared from PokemonSimulationOne class

    Authors: John Downes & Wuilmer Palacios
    """
    def combined_distrubution_simulation(self, opponent_pokemon_name, pokedex_data):
        def probability_calculation(selected_data, opponent_data):
            hp_prob = selected_data["hp"] / (selected_data["hp"] + opponent_data["hp"])
            attack_prob = selected_data["basic_attack"] / (
                        selected_data["basic_attack"] + opponent_data["basic_attack"])
            defense_prob = selected_data["defense"] / (selected_data["defense"] + opponent_data["defense"])

            combined_prob = (hp_prob + attack_prob + defense_prob) / 3
            return combined_prob

        selected_data = pokedex_data.get(self.selected_pokemon_name.lower())
        opponent_data = pokedex_data.get(opponent_pokemon_name.lower())
        if not selected_data or not opponent_data:
            raise ValueError(f"Data missing for {selected_data} or {opponent_data}")
        combined_prob = probability_calculation(selected_data, opponent_data)
        win_count = 0
        for _ in range(self.num_simulations):
            if random.uniform(0, 1) < combined_prob:
                win_count += 1
        win_probability = win_count / self.num_simulations
        # print(f"The probability for {selected_pokemon.upper()} against {opponent_pokemon_name.upper()} is :{win_probability}")
        return win_probability


    def advantage_probability(self, opponent_pokemon_name, type_advantage):
        """Determines the advantage probability based on the stats and types of the battling pokemon
        
        Args:
            opponent_pokemon_name (str): the name of the pokemon being battled
            type_advantage (dict): dictionary containing type advantages
        """
        # Type Advantage
        total_multiplier = 1.0
        selected_types = self.selected_pokemon_name['types']
        opponent_types = opponent_pokemon_name['types']
        for s_type in selected_types:
            for o_type in opponent_types:
                multiplier = type_advantage.get(s_type, {}).get(o_type, 1.0)
                total_multiplier *= multiplier
        num_comparisons = len(selected_types) * len(opponent_types)
        average_multiplier = total_multiplier ** (1 / num_comparisons) if num_comparisons > 0 else 1
        type_score = average_multiplier
        type_probability = max(0, min(1, (type_score + 2) / 4))

        # Stat Advantage
        hp_ratio = self.selected_pokemon_name['hp'] / opponent_pokemon_name['hp']
        defense_ratio = self.selected_pokemon_name['defense'] / opponent_pokemon_name['defense']
        stat_score = (hp_ratio + defense_ratio) / 2
        stat_probability = max(0, min(1, stat_score / 2))

        # Combined
        combined_probability = (0.6 * type_probability) + (0.4 * stat_probability)
        return combined_probability

# ----------------------------------------------------------------------------------------------------------

# Other Functions
def main(selected_pokemon, num_opponents, num_simulations):
    """ Main functon that create an instance of PokemonSimulationOne class to initialize

    Args:
        selected_pokemon (str): Name of the selected Pokemon that will be used to battle against other Pokemons
        num_opponents (int): Number of different opponent the selected Pokemon will have to face
        num_simulations (int): Number of time each battle will simulate
    """
    pokemon_sim_1_instance = PokemonSimulationOne(selected_pokemon, num_opponents, num_simulations)
    pokemon_sim_1_instance.print_result()

def parse_args(arglist):
    """ Parse command line arguments.

    Requires two arguments and one optional:
        selected_pokemon (str): Required name of the Pokemon the user wants to use in both of the simulations to find its effectiveness
        against others

        number_opponents (int): Required number of opponents the user wishes to be used in the simulation

        --simulations or -s (int): An optional number of simulations the user wishes each battle will occur.
        The default value will be 50 if left ignored

    Args:
        arglist (list of str): command-line arguments

    Returns:
        namespace: an object with one attribute, file, containing a string.

    Author: Jay Walter
    """
    parser = ArgumentParser()
    parser.add_argument("selected_pokemon", help="The main Pokemon that will be simulated")
    parser.add_argument("number_opponents", type=int, help="The number of unique Pokemons to simulate")
    parser.add_argument("-s", "--simulations", type=int, default=50, help="The number of battles to simulate")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.selected_pokemon, args.number_opponents, args.simulations)

    # Example in the console ↓ (windows):
    # python .\main.py "pikachu" 54
    # python .\main.py "Typhlosion" 54 -s 100

    # https://www.thegamer.com/pokemon-gold-silver-strongest-generation-2-ii-stats/
    # https://www.thegamer.com/weakest-johto-pokemon-ranked/
    # https://bulbapedia.bulbagarden.net/wiki/Damage damage calculator
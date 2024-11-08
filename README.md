# Pokemon Battle Simulation Probability

Find Pokemon that will have a high chance (greater than 75%) of losing against a selected Pokemon. 

- Using the PokeAPI database for all the Pokemon values
  - Will only use Pokemons from 2nd generation (might change)

- Two required inputs in console:
  1. The main Pokemon that will be used to battle
  2. Number of different kind of Pokemon that will face the selected Pokemon 
     - Since there's 18 types, the min is 54 Pokemon and max is 180
       - (`54 <= num_pokemon <= 180`) 

## Side Functions/Methods:

### 1. Main Function

- Read console input and run the simulation.
- Calls some functions

### 2. Command line Argument Function

- Handle two required arguments in the console <a name="required" ></a>:
  - `selected_pokemon`: the main Pokemon it will be used in the simulation
  - `num_pokemon`: number of Pokemon that will battle the `selected_pokemon`

### 4. **Print Statements**

- Print the result in the console once all simulation is done.



------

## Five Main Functions/Methods Algorithms

### 1. *Grabbing Data**

Grab the necessary Pokemon stats needed to run the simulation.

- [Required attributes/parameters)](#required):

  - `selected_pokemon`, `num_pokemon`, `johto_pokemons`
    - `selected_pokemon`: The main Pokemon used to fight all other Pokemons
    - `num_pokemon`: Number of different Pokémon's it will fight
    - `johto_pokemons`: List of all Pokemon from the Johto region or 2nd generation

- Will return two dictionaries:

  - `selected_pokemon_dict`: of all the attribute data for the selected Pokemon
  - `opponent_pokedex_dict`: of all the attributes data for each Pokemon selected

- It will grab:

  - `name (str)`, `types (list)`, `basic_attack (int)`, `moves (dict)`, `defense (int)` & `hp (int)` 
  - For moves (up to 3), find moves where `power > 0` so it can deal damage.

    - `name:` `damage output`

    - One basic moves (most Pokemon share), different from `basic_attack (deafult)`
    - Two unique moves (Unique to the specific Pokemon)

- Catch any new Pokemon that will be used for future simulations to reduce API request

  - Stored in JSON file

    ```json
    {
      "pikachu": {
        "hp": 35,
        "basic_attack": 55,
        "defense": 40,
        "types": ["electric"],
        "moves": [{"mega-punch": 80}, {"pay-day": 40}, ...]
      },
       "Charmander" {
          ... 
      }
    }
    ```

### 2. **Test for Win Probability Part 1.0**

A turn based simulation to see which Pokemon will win.

- Uses all the data in the returned dictionary `pokedex` from the data grabber function/method

- The simulation will repeat each Pokemon battle multiple times to increase sample size

  - Ex: If 10 simulations per each Pokemon battle and Pikachu is the `selected_pokemon`:
    - `10 sample size for Pikachu vs Charmander`, `10 sample size for Pikachu vs Nidoking`, etc. 

- Repeat each time once one of the Pokemon's `hp <= 0`  
  - Once a battle has ended, append the Pokemon that won and lost in the appropriate list 
    - Also add a score to the `types_score` if the chosen Pokemon lost
    
      - `types_score` will prob be a dictionary
    
        ```json
        {"normal": 1, "electric": 2, "fire": 0, ...}
        ```

- Once iteration ends, calculate the mean based win or loss
  - Determine the likelihood of the selected Pokemon winning against all the Pokemon it battled and which type is most effective against.

### 3. **Test for Win Probability Part 1.1**

A algorithm to calculate the damage output based on `type` and `defense`

- Use one of the `moves` or `basic_attack` to deal damage.
  - Some kind of algorithm to decide which attack to use 

- If `water` vs. `fire`: `water` will deal more damage by a certain amount
  - If  both are same element, use base damage based on the move in `pokedex_dict` or `selected_pokemon_dict`
- If a Pokemon have high defense, it will take less damage

### 4. **Test for Win Probability Part Two (Conditional Distribution) Part 2.0**

Another simulation used to find the win probability of each battle against a certain Pokemon. This will compare the result of the **first simulation** to check for a relationship (hopefully both agree on which Pokemon will likely win).

1. Find the likelihood of winning based on combined probability (`types`, `defense`, `hp`, etc.) 

   - Use the same variable stats as in the first simulation.
   - Apply an advantage probability system to identify which Pokemon has a higher chance of winning (combined probability).
2. Then simulate using the combined probability and random values from 0-1 to see if the random value falls within the combined probability.
   - Simulate the random value multiple times and calculate the mean.

### 5. **Determine the Advantage Probability Part 2.1**

Calculate the advantage probability (`types`, `defense`, `hp`, etc.) between the two Pokemon that will be facing each other.

- This will be used in the conditional distribution simulation method/function (part 2.0)

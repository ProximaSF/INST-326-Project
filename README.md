# Pokemon Battle Simulations

Two simulations to determine the mean win rate of the specific Pokemon against other randomly selected Pokemons

## File Purposes

1. `main.py`:
   
   - The main script to execute Pokemon simulations. 
   
2. `pokemon_info_getter.py`
   
   - Script contain 3 functions, 2 used in `main.py` to grab all the necessary Pokemon information (hp, defense, attacks, etc) from [PokeAPI](https://pokeapi.co/) to run each simulation.
   
3. `pokedex.json`
   
   - `json `file where all Pokemon status is stored after grabbed new data from PokeAPI to reduce API calls and run code faster.
   
4. `README.md`
   
   - Markdown file containing information related to the project from instructions, file purpose, attribution and etc.
   
     

## Instructions

Uses the command line argument in the console to run simulations.

- Requires two arguments: `selected_pokemon` & `number_opponents`
  - `selected_pokemon`: the name of the Pokemon from generation 2 to be used in both simulation
  - `number_opponents`: a number (integer) of other Pokemons that will be used to battle against the selected Pokemon. 
    - Value must be `>= 54` or `<= 251`: Will be rounded to a value that's divisible by 18
- One optional argument: `simulations`
  - `simulations`: a number (integer) of times each battle will occur. The default value is 50 and there is no limit. 
  - Flags are `-s` or `--simulations`
- In the terminal, type `main.py` as the first argument, than the name of a Pokemon (`Pikachu`) you want to use and than the number of Pokemons you want to use to fight against the first Pokemon you picked.
  - To set a simulation limit occurrence for each battle, than type `-s` or `-simulations` follow by a number
  - <u>Example inputs for WindowOS:</u>
    - `python main.py "Pikachu" 100`
    - `python main.py "Charmander" 54 -s 10`
    - `python main.py "magikarp" 54 --simulations 10`


## Output/ Interpretation

## Annotated Bibliography

1. Hallett, P. (2014, December). Pokemon API. Pokéapi. https://pokeapi.co/ 

   **Explanation:** Massive datafile that contains pokemon data that we used for our simulations. Data includes, but is not limited to, hp, defense, attacks, types, and more. 

2. Wikipedia. (2024, December 6). [Gameplay of pokémon](https://en.wikipedia.org/wiki/Gameplay_of_Pok%C3%A9mon#:~:text=Pok%C3%A9mon%20uses%20a%20turn%2Dbased,is%20automatically%20sent%20into%20battle)

   **Explanation:** This doesn't factor into the actual code, its just how the Pokemon game is played, and something worth noting. Some of our team members weren't familiar with how the game was played, so we referred to this for an exact explanation.

3. Bulbapedia. “Damage - Bulbapedia, the Community-driven Pokémon Encyclopedia.” *Bulbapedia*, 22 Nov. 2024, [bulbapedia.bulbagarden.net/wiki/Damage](https://bulbapedia.bulbagarden.net/wiki/Damage).

   **Explanation:** Used the damage formula provided in Bulbapedia for first generation in the function `damage` to calculate the damage output of each Pokemon. Some variables like `STBD` & `random` was not included in the code but the structure is the same. 

## Attribution

| **Method/function                  | **Primary author** | **Techniques demonstrated**   |
| ---------------------------------- | ------------------ | ----------------------------- |
| `parse_args`                       | Jay Walter         | `ArgumentParser` class        |
| `print_result`                     | Jay Walter         | Use of `lambda` in `sorted()` |
| `damage`                           | Ismail Touray      | keyword arguments             |
| `calculate_damage`                 | Ismail Touray      | Dictionary lookup             |
| `battle_against_all`               | Griffin Biddle     | with statements, json.load    |
| `battle_simulation`                | Griffin Biddle     | f-strings with expressions    |
| `advantage_probability`            | John Downes        | conditional expressions       |
| `get_info`                         | John Downes        | Sequence unpacking            |
| `combined_distrubution_simulation` | Wuilmer Palacios   |                               |

## Concepts:

- [x] conditional expressions
- [x] optional parameters and/or keyword arguments
- [x] f-strings containing expressions
- [x] `with` statements
- [x] `ArgumentParser` class
- [x] Sequence unpacking
- [ ] set operations (union, intersection, etc)
- [x] Comprehensions or generator expressions
- using `lambda` with these functions
  - [ ] `list.sort()`
  - [x] ``sorted()`,
  - [ ]  `min()` or `max()`:

- [ ] `super()` : method override
- [ ] composition of two custom classes
- [x] `json.dumps()`, `json.loads()`, `json.dump()`, or `json.load()`
- [ ] Use of `re`
- [ ] magic methods beside`__init__()`
- [ ] operations on `Pandas` 
- [ ] Data visualization

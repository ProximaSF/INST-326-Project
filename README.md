# Pokemon Battle Simulations

Find Pokemon that will have a high chance (greater than 75%) of losing against a selected Pokemon. 

- Using the PokeAPI database for all the Pokemon values
  - Will only use Pokemons from 2nd generation (might change)

- Two required inputs in console:
  1. The main Pokemon that will be used to battle
  2. Number of different kind of Pokemon that will face the selected Pokemon 
     - Since there's 18 types, the min is 54 Pokemon and max is 180
       - (`54 <= num_pokemon <= 180`) 

## File Purposes

1. `main.py`:
   - The main script that will execute the Pokemon simulations. 
2. `pokemon_info_getter.py`
   - Script contain 3 functions, 2 used in `main.py` to grab all the necessary Pokemon information (hp, defense, attacks, etc) [PokeAPI](https://pokeapi.co/) to run each simulation.
3. `pokedex.json`
   - `json `file where all Pokemon status is stored after grabbed from PokeAPI. Used to reduce API calls to make simulation run faster. 
4. `README.md`
   - Markdown file on instruction how to use the script and run the simulation in the console. It also contain other information's relate to the project.

## Instructions

## Output

## Attribution

| **Method/function                                    | **Primary author** | **Techniques demonstrated**    |
| ---------------------------------------------------- | ------------------ | ------------------------------ |
| functions in `pokemon_info_grabber.py`, `parse_args` | Jay Walter         | ArgumentParser class, Sorted() |
|                                                      | Wuilmer Palacios   |                                |
|                                                      | Ismail Touray      |                                |
|                                                      | Griffin Biddle     |                                |
|                                                      | John Downes        |                                |

## Concepts:

- [ ] conditional expressions
- [ ] optional parameters and/or keyword arguments
- [ ] f-strings containing expressions
- [ ] `with` statements
- [x] `ArgumentParser` class
- [ ] Sequence unpacking
- [ ] set operations (union, intersection, etc)
- [ ] Comprehensions or generator expressions
- [x] `list.sort()`, `sorted()`, `min()`, or `max()`: using `lambda` with those functions
- [ ] `super()` : method override
- [ ] composition of two custom classes
- [ ]  `json.dumps()`, `json.loads()`, `json.dump()`, or `json.load()`
- [ ] Use of `re`
- [ ] magic methods beside`__init__()`
- [ ] operations on `Pandas` 
- [ ] Data visualization

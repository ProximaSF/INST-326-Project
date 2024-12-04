# Pokemon Battle Simulations

Two simulations to determine the mean win rate of the specific Pokemon against other randomly selected Pokemons

## File Purposes

1. `main.py`:
   - The main script that will execute the Pokemon simulations. 
2. `pokemon_info_getter.py`
   - Script contain 3 functions, 2 used in `main.py` to grab all the necessary Pokemon information (hp, defense, attacks, etc) [PokeAPI](https://pokeapi.co/) to run each simulation.
3. `pokedex.json`
   - `json `file where all Pokemon status is stored after grabbed from PokeAPI. Used to reduce API calls to make initial simulation run faster. 
4. `README.md`
   - Markdown file on instruction how to use the script and run the simulation in the console. It also contain other information's relate to the project.

## Instructions

Uses the command line argument in the console to run simulations.

- Requires two arguments: `selected_pokemon` & `number_opponents`
  - `selected_pokemon`: the name of the Pokemon from generation 2 that will be used in both simulation
  - `number_opponents`: a number (integer) of other Pokemons that will be used to battle against the selected Pokemon. 
    - Value must be `>= 54` or `<= 251` because there are 251 Pokemon provided for 2nd gen in the API and 54 is the minimum to run the simulation with adequate sample size. 
- One optional argument: `simulations`
  - `simulations`: a number (integer) of times each battle will occur. The default value is 50 and there is no limit. 
  - Flags are `-s` or `--simulations`
- Example inputs:
  -  `python main.py "Pikachu" 100`
  -  `python main.py "Charmander" 54 -s 10`
  -  `python main.py "magikarp" 54 --simulations 10`

## Output

## Attribution

| **Method/function                          | **Primary author** | **Techniques demonstrated**   |
| ------------------------------------------ | ------------------ | ----------------------------- |
| All functions in `pokemon_info_grabber.py` | Jay Walter         | List comprehensions           |
| print_result                               | Jay Walter         | Use of `lambda` in `sorted()` |
|                                            | Wuilmer Palacios   |                               |
|                                            | Ismail Touray      |                               |
| battle_against_all                         | Griffin Biddle     | with statements, json.load    |
| battle_simulation                          | Griffin Biddle     | f-strings with expressions    |
|                                            | John Downes        |                               |

## Concepts:

- [ ] conditional expressions
- [ ] optional parameters and/or keyword arguments
- [x] f-strings containing expressions
- [x] `with` statements
- [ ] `ArgumentParser` class
- [ ] Sequence unpacking
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



Damage formula (sim 1):


$$
damage = (\frac{((\frac{2*level}{5}) * move\ damage * \frac{basic\ attack}{opponenet\ defence})}{50} + 2) * (type\ advanatge)
$$

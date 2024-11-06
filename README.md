# Pokemon Battle Simulation Probability

Find Pokemons that will have a high chance (greater than 75%) of losing against a selected Pokemon

## Functions/Methods:

### 1. <u>Grabing data</u>

Grab the necessary Pokemon stats needed to run the simulation. 

- Using the PokeAPI dataset
- Catch any new coming Pokemon that will be used to future simulation
  - Probably store in a json file 

### 2. <u>Test For Win Probability Part One</u>

A turn-based simulation to see which Pokémon will win.

-  The simulation will repeat a few times to increase sample size
  - Repeat each time once one the Pokémon's `hp <= 0`  
- Find the mean-based win or loss
  - Determine which Pokémon tend to win more

### 3. <u>Test For Win Probability Part Two (Conditional Distribution)</u>

Another simulation that will be used to find the win probability of each battle against a certain Pokémon. It Will be used to compare the result of the <u>first simulation</u> to see if they share a relationship (hopefully both agree which Pokémon will likely win).

1. Find the likelihood of winning based on a combined probability (`types`, `defense`, `hp`, etc) 

   - Will use the same variable stats used in the first simulation.
   - Will use an advantage probability system to see which Pokemon have a high chance of winning (combined probability)

   2. Then simulate using the combined probability and the random values from 0 to 1 to see if the random value falls within the combined probability.
      - Simulate the random value a few times and find the mean

### 4. <u>Determine the Advantage Probability</u>

Find the advantage probability (`types`, `defense`, `hp`, etc) between the two Pokemon that will be facing

- It Will be used in the conditional distribution simulation method/function

### 5. <u>Find Pokemon That Would Lose</u>

Using the probability from simulation 1 and 2 to determine which Pokemon have a probability of losing against the selected Pokemon (loss rate >= 75%)

- The method/function will likely be called inside the simulation methods

- Will return a list all possible Pokemons
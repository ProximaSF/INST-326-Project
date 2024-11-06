# Pokemon Battle Simulation Probability

Find Pokemon that will have a high chance (greater than 75%) of losing against a selected Pokemon.

## Functions/Methods:

### 1. **Grabbing Data**

Grab the necessary Pokemon stats needed to run the simulation.

- Using the PokeAPI dataset
- Catch any new Pokemon that will be used for future simulations
  - Possibly store in a JSON file

### 2. **Test for Win Probability Part One**

A turn based simulation to see which Pokemon will win.

- The simulation will repeat multiple times to increase sample size
  - Repeat each time once one of the Pokemon's `hp <= 0`  
- Calculate the mean based win or loss
  - Determine which Pokemon tends to win more

### 3. **Test for Win Probability Part Two (Conditional Distribution)**

Another simulation used to find the win probability of each battle against a certain Pokemon. This will compare the result of the **first simulation** to check for a relationship (hopefully both agree on which Pokemon will likely win).

1. Find the likelihood of winning based on combined probability (`types`, `defense`, `hp`, etc.) 

   - Use the same variable stats as in the first simulation.
   - Apply an advantage probability system to identify which Pokemon has a higher chance of winning (combined probability).

2. Then simulate using the combined probability and random values from 0-1 to see if the random value falls within the combined probability.
   - Simulate the random value multiple times and calculate the mean.
3. Calls the method that will store the Pokemon in a list

### 4. **Determine the Advantage Probability**

Find the advantage probability (`types`, `defense`, `hp`, etc.) between the two Pokemon that will be facing each other.

- This will be used in the conditional distribution simulation method/function.

### 5. **Find Pokemon That Would Lose and Print Statments**

1. Using the probability from simulations 1 and 2, determine which Pokemon have a probability of losing against the selected Pokemon (loss rate >= 75%).

   - The method/function will likely be called within the second simulation methods.

   - Return a list of all possible Pokemon.

2. Once all simulation is done and the data is gathered, print the result in the console.
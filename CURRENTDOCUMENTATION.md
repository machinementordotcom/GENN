# Documentation as of March 9th 2020 

### Current Models:
- [FSM](https://github.com/dbinnion/AdaptableAITesting/tree/master/FSMPlayers) (Finite State Machine)
  * [Short](https://github.com/dbinnion/AdaptableAITesting/blob/master/FSMPlayers/ShortRangeSim.py)
  * [Mid Range](https://github.com/dbinnion/AdaptableAITesting/blob/master/FSMPlayers/MidRangeSim.py)
  * [Range](https://github.com/dbinnion/AdaptableAITesting/blob/master/FSMPlayers/RangePlayerSim.py)
- [DC](https://github.com/dbinnion/AdaptableAITesting/blob/master/DynamicController/DynamicControllerSim.py) (Dynamic Controller)
- [GENN](https://github.com/dbinnion/AdaptableAITesting/blob/master/GENN/GENN.py) (Genetically Evolved Neural Network)

### Current game progression: 
1. Main.py 
	* Controls the main game and any multiprocessing that will be created. 
2. Sim.py or MyGame.py
	* Depending on if simulation is requested or a visual representation of the game is requested one of the two versions will be created. 
	* This will control the players and be the interface that will allow them to update throughout the game. 
3. Two versions of players: 
	* This would be the interface for any of the above models. All models have a similar structure: Initilization, functions to attack and use a shield, then an update function. The update function is called every turn and provides the player with the ability to move and when the time is correct the ability to attack. 

### Player Understanding 
* Players will all have equal health and speed. Damages are constant across the three attacks (short, mid range, and range) (These are also referred to as knife, fireball, and arrow) 
* Players can move every turn, however they can only attack once every 30 turns, this is tracked using the variable currtime 

### Game interface:
1. How many games would you like played at the same time? -- This corresponds to how many games do you want run in this generation and this number will be distributed via multiprocessing 
2. Enter the amount of generations to be played? -- This is how many generations will be played in total, you can think of the total amount of games to be this number and the first one multiplied together. 
3. Would you like to track trends? -- This will create a textual output of the programs that can be seen in the main directory
4. Would you like to create graphical outputs? -- This will turn those trends into graphical output using matplotlib
5. What type of simulation do you want for player N? -- This is how you set the players that will battle against each other 
6. Run Graphically? -- This will decide if the game will run visually or not, it runs much faster not in visual mode
### Miscellaneous
* All useful constants such as speed, damage, health, etc. are kept in utils/constants.py
* The visual interpretation of the models has been on the back burner and the current most important thing is the creation of the models in a simulated version
* [More information on the models and creation](https://github.com/dbinnion/AdaptableAITesting/blob/master/SIMULATIONTYPES.md)

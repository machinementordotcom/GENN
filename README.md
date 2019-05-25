# Adaptable AI Testing 
A fully custom simulation environment that interchangeably compares reinforcement learning models. Has a full blown API for modularity of algorithms, built in general genetic neural network library, and other utilities for training and testing.

# General Info

### Versions:
- Built in [python3](https://www.python.org/downloads/).

### Libraries Required:
- [Arcade](http://arcade.academy/)

### Usage:
- Clone this repository. `git clone https://github.com/dbinnion/AdaptableAITesting.git`
- To run any simulation, run `python3 main.py` inside the main directory.
- Follow the terminal instructions to run any type of simulation.


### Simulation Types:
- **Freeplay** Freeplay let’s you play against a character of any type.
- **FSM**: Finite State Machine allows you to select from three character types (range, mid,short). These are trained with profile based logic




### Indicators:
- Shield: If a player’s color and shape changes it means that have enabled their shield. 
- Bar below Character: Every character has a bar above below their image that displays their health percentage. 
    - Green = health
    - Red = health lost 
- New Placement of characters: The game has ended and the next simulation has started.

- Arrow: Long range attack
- Fireball: Mid-range attack.
- Knife: A Short-range attack.

<br>

# Main Simulation Keys
|Key(s)|Description|Context|
|---|---|---|
|W, A, S, D|Movement|Player|
|LEFT, UP, RIGHT, DOWN|Directional movement|Player|
|Q|Shield|Player|
|SPACE|Long-range arrow|Player|
|E|Mid-range fireball|Player|
|R|Short-range knife|Player|
|esc|End The Game|Global|
<br>


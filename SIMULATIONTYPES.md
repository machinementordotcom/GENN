# Simuatlion Styles

### Finite State Machine
- Long-range: Also know as long Range, this player's main goal is to increase the distance between the opponent and himself. It will back up using a speed of 1 to escape the opponent and any projectile coming its way. It will fire it's arrow once every 30 updates and use it's shield when it goes below 50 percent health and only has one shield.
- Mid-Range: Also know as Mid, this player's main goal is to keep a distance of 250 from the opponent, once in this "sweet spot" it will throw fireballs (that only last for a given range of 200) every 30 updates. It moves with a speed of 1 and in a manner to make sure his opponent cannot circle away from him. It only attempts to get closer to his opponent when he has above 70 percent health and is farther than 250, once it's health goes below 70 percent it will attempt to dodge any projectiles headed it's way, then attempt to maintain (or reach) the sweet spot. It uses it's shield when it goes below 50 percent health and only has one shield. 
- Close-Range: Also know as short, this player's main goal is to get as close as possible to his opponent, once within 50 distance he will use his knife every 30 updates. It moves with a speed of .955 in the fastest way to possible to the opponent. It only attempts to get closer to his opponent when he has above 45 percent health, once it's health goes below 45 percent it will attempt to dodge any projectiles headed it's way first then move closer. It uses it's shield when it goes below 50 percent health and only has one shield. 

Currently the players are balanced as the following: short > range > mid > short . This is with around a 75% win rate for each player.
#### Figure 1 FSM image:
![Figure 1](https://github.com/dbinnion/AdaptableAITesting/blob/master/imagesAndGraphs/FSMImage.png)

### Dynamic Controllers

The Dynamic controllers are made up of two groups of weights, shooting and movement weights. The shooting weights change the angle and type of shot, there are 7 different angles for each of the three attacks (long, mid, and short). The movement weights have groups within the weights. The first 7 weights correspond to the distance that a player will not move away from the enemy at, the second 7 weights correspond to the distance that a player will move towards the enemy at. The next two weights correspond to how a player will move (toward or away from the opponent), the next two weight correspond to how a player will dodge an incoming projectile within the x direction and the last two weights correspond to how a player will dodge an incoming projectile within the y direction. 

- Master: The master was trained against the 3 FSM's with a set of pre-trained weights, it was trained tracking individual weights and looking for any interactions within the movement and shooting weights. As the master plays it will not update the weights, it will just use the weights that are already set to fight its opponent. 
- Average: The average was trained against the 3 FSM’s with a set of pre-trained weights, it was trained tracking individual weights and looking for any interactions within the movement and shooting weights. As the average plays it will update the weights, learning from the opponent that it is currently facing and adapting to strategies that help the FSM win. This starts with the same weights that the Master uses but adapts them to the game.
- Random: The random starts out with equal weights across the categories (not trained at all) and learns from the current opponent it is playing against. 

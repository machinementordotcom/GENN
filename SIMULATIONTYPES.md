# Simuatlion Styles

### Finite State Machine
- Long-range: Also know as long Range, this player's main goal is to increase the distance between the opponent and himself. It will back up using a speed of 1 to escape the opponent and any projectile coming its way. It will fire it's arrow once every 30 updates and use it's shield when it goes below 50 health and only has one shield.
- Mid-Range: Also know as Mid, this player's main goal is to keep a distance of 250 from the opponent, once in this "sweet spot" it will throw fireballs (that only last for that given range) every 30 updates. It moves with a speed of .9 and in a manner to make sure his opponent cannot circle away from him. It only attempts to get closer to his opponent when he has above 70 health and is farther than 250, once it's health goes below 70 it will attempt to dodge and projectiles headed it's way, then attempt to maintain (or reach) the sweet spot. It uses it's shield when it goes below 50 health and only has one shield. 
- Close-Range: Also know as short, this player's main goal is to get as close as possible to his opponent, once within 50 distance he will use his knife every 30 updates. It moves with a speed of .9 in the fastest way to possible to the opponent. It only attempts to get closer to his opponent when he has above 45 health, once it's health goes below 45 it will attempt to dodge and projectiles headed it's way first then move closer. It uses it's shield when it goes below 50 health and only has one shield. 
#### Figure 1 FSM image:
[Figure 1] (graphsAndImages/FSMimage.png)

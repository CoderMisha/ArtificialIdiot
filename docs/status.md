---
layout: default
title: Status
---
# {{ page.title }}

## Video Summary
\[Youtube link\]

## Project Summary

We are planning to train an AI to play a minigame integrated with features in Beat-Saber and Dancing-Line in Minecraft (similar to the map in this YouTube video: Zedd & Jasmine Thompson - Funny (Minecraft Music Video | Beat Synchronized!) but also included features similar to dancing line (reference to this YouTube video: Dancing Line | The Piano %100 10/10 Gems)).

The task of the AI is trying to hit the block along the railroad while riding on it with swords in the same color with the block at the proper time (i.e. right before the block is passing the agent). A correct and precise hit will increase the AI's score, and a miss or hitting with a sword in wrong color would decrease the score. The AI should take the game frame as input and perform "aim" (including turn, look / pitch), "switch tools", and "attack" actions correspondingly.

To make this task more challenging, the AI will encounter multiple rail ways and have to choose the correct one (other wrong ones will lead to lava). The AI should hit the lever at proper time to switch railways to ride on correct one.


## Approach

At current stage, we are using reinforcement learning and Q-Learning algorithm. For the QNetwork model, we keep using torch and use a 5-layer forward-feeding neural network, but we consider to switch to Keras in the future. The structure of our model is as following: linear, ReLu, linear, ReLu, linear. The model has 9 final states. As we further increase the difficulty of the project problem and add more choices to the agent's inventory, we will also increase the number of states. 

We change the usage of the default reward system in Malmo because we need to consider whether the agent hits the block with the tool in the same color. When the agent successfully hits the block, it will collect the item mined from the block. Therefore, we use RewardForCollectingItem handler as a signal sender. When the agent collects different items, we programmed the Malmo system to give different rewards, respectively. In the function that gets the rewards and process them, we use these rewards as signals, and check whether the signals are the same with the tool in the agent's hand, which is stored in a global variable. For the beginning stage, the reward function is simply adding rewards or substracting penalties, and the final score will be returned when one action ends. For future stages, we might make it more complicated and change the time the agent knows the score.

The QNetwork will be updated after each frame. [?


## Evaluation

## Remaining Goals and Challenges

## Resources Used

---
layout: default
title: Final Report
---
# {{ page.title }}

## Video

[Demo Video](https://www.ics.uci.edu/~tongjiew/cs175/status_report_vid.mp4)

## Project Summary

We are planning to train an AI to play a minigame integrated with features in Beat-Saber (similar to the map in this YouTube video: Zedd & Jasmine Thompson - Funny (Minecraft Music Video \| Beat Synchronized!) but also included features similar to dancing line (similar to this YouTube video: Dancing Line \| The Piano %100 10/10 Gems)).

The task of the AI is trying to hit the block along the railroad while riding on it with swords in the same color with the block. A correct hit will increase the AI's score, and a miss or hitting with a sword in wrong color would decrease the score. The AI should take the game frame as input and perform "switch tools" and "attack at the right side" actions correspondingly.

To make this task more challenging, the AI will encounter multiple rail ways and have to choose the correct one (other wrong ones will lead to lava). The AI should hit the controling redstone at proper time to switch railways to ride on correct one. The AI will get rewards when it lives, and be punished when it falls into lava.

This problem / setting needs AI/ML algorithm to solve it because it is quite hard for humans to manually play this game perfectly in Minecraft, while the cart drives relatively fast and features and blocks appear frequently. For an AI to play such gemes, it will need convolutional neural networks and reinforcement learning to learn when blocks are approaching and where and when it needs to hit the blocks to earn scores and keep living.

## Approach

### Rewards
- Safely complete the mission without falling into the lava (which means the AI correctly hits all the lever redstones): 10000
- Fall into the lava: -100
- Reward for living (per tick): 0.1
- Hit blocks correctly (hit the block with the tool in the same color): 10
- Hit blocks incorrectly (hit the block with the tool in a different color): -1
- Die for whatever reason: -100

### Action spaces
- 0: No action
- 1: Attack left
- 2: Attack right
- 3: Switch tool


### Observation / Information for the AI

- the center (396x314) of the current frame (960x540)

### Model

- Deep Q Network
-> Framework: rllib <br>
-> Library: torch <br>
-> Neural network structure <br>
    --> 3-layer Convolutional Neural Network <br>
        ---->> nn.Conv2d(3, 6, 3) -> relu -> max_pool -> nn.Conv2d(6, 16, 3) -> relu -> max_pool -> nn.Conv2d(16, 32, 3) -> relu -> max_pool <br>
        ---->> Input: the resized frame (shape=(314, 396, 3)) <br>
        ---->> Activation: relu, max_pool <br>
    --> 3-layer Fully Connected Neural Network <br>
        ---->> nn.Linear(32 * 37 * 47, 120) -> nn.Linear(120, 84) -> nn.Linear(84, 4) <br>
        ---->> Output: action index <br>
        

### Comparisons with the past approaches

- Structure changes <br>
-> At the beginning: QNetwork model: a 6-layer forward-feeding neural network. No framework. <br>
    -->> Advantages: Easy to program, manage and debug. <br>
    -->> Disadvantage: Not as efficiency as later models. <br>
-> Later: PPO in default setting. Framework: rllib. <br>
    -->> Advantages: Better performance compared to the previous QNetwork model. With the framework rllib, we can complete more tasks and use more powerful functions by following the API and don't need to worry about many details. <br>
    -->> Disadtages: The AI learns slowly and seems not learning the frame very efficiently. This model takes a long time but not accomplish much. <br>
-> Present: DQN model with CNN and FNN layers. Framework: rllib. <br>
    -->> Advantages: With CNN layers, the AI is able to more efficiently learn the frames and make more correct decisions based on that. <br>
        

## Evaluation

### Quantitative Evaluation
The total score the agent receives after completing each episode is one evaluation criteria. The higher the score, the longer the agent lives, and the better its performance is. Scores will consist of different parts including living (penalty for not hitting lever and ride into lava), correct hitting (hit the block with the tool in the same color), and hitting timing. We will use random agents as the first baseline, human-player score as the second baseline, and train the agent to perform better than act randomly and manually. In next stages, more tools and levers will be added to the map, and the evaluation process will start again.

### Qualitative Evaluation
We will check the final result and check how the agent makes decisions. Decisions includes turn, attack, pitch, and hotbar switch. If the agent mostly makes necessary decisions, then it will pass qualitative evalutaion perfectly. If not, then it might need improvements besides of quatitative evaluations. 


## Resources Used

- Project Malmo - [https://microsoft.github.io/malmo/0.14.0/Documentation/classmalmo_1_1_agent_host.html#ac1421c4ed9ababff1300ea58a37859bc](https://microsoft.github.io/malmo/0.14.0/Documentation/classmalmo_1_1_agent_host.html#ac1421c4ed9ababff1300ea58a37859bc)
- XML Schema Documentation - [https://microsoft.github.io/malmo/0.30.0/Schemas/MissionHandlers.html#element_ContinuousMovementCommands](https://microsoft.github.io/malmo/0.30.0/Schemas/MissionHandlers.html#element_ContinuousMovementCommands)
- DQN - [https://blog.csdn.net/war3gu/article/details/90641076](https://blog.csdn.net/war3gu/article/details/90641076)
- Gitter Microsoft/Malmo - [https://gitter.im/Microsoft/malmo?at=5a5ddf51290a1f456194c199](https://gitter.im/Microsoft/malmo?at=5a5ddf51290a1f456194c199)
- UCI CS 175 HW2 (Due to copyright, we will not include the link to Canvas page here)
- Malmo Platform Tutorial - [https://microsoft.github.io/malmo/0.17.0/Python_Examples/Tutorial.pdf](https://microsoft.github.io/malmo/0.17.0/Python_Examples/Tutorial.pdf)
- Redstone Logic Circuit - [https://minecraft.gamepedia.com/Mechanics/Redstone/Logic_circuit](https://minecraft.gamepedia.com/Mechanics/Redstone/Logic_circuit)
- Redstone Transmission Circuit - [https://minecraft.gamepedia.com/Mechanics/Redstone/Transmission_circuit](https://minecraft.gamepedia.com/Mechanics/Redstone/Transmission_circuit)

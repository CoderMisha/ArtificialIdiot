---
layout: default
title: Status
---
# {{ page.title }}

## Video Summary

[Demo Video](https://www.ics.uci.edu/~tongjiew/cs175/status_report_vid.mp4)

<video controls width="560">
    <source src="https://www.ics.uci.edu/~tongjiew/cs175/status_report_vid.mp4"
            type="video/mp4">

    Sorry, your browser doesn't support embedded videos.
</video>

## Project Summary

We are planning to train an AI to play a minigame integrated with features in Beat-Saber (similar to the map in this YouTube video: [Zedd & Jasmine Thompson - Funny (Minecraft Music Video \| Beat Synchronized!)](https://youtu.be/Wm0wFAJr1Xo) but also included features similar to dancing line (similar to this YouTube video: [Dancing Line \| The Piano %100 10/10 Gems](https://youtu.be/FeSOAljGR80)).

The task of the AI is trying to hit the block along the railroad while riding on it with swords in the same color with the block at the proper time (i.e. right before the block is passing the agent). A correct and precise hit will increase the AI's score, and a miss or hitting with a sword in wrong color would decrease the score. The AI should take the game frame as input and perform "aim" (including turn, look / pitch), "switch tools", and "attack" actions correspondingly.

To make this task more challenging, the AI will encounter multiple rail ways and have to choose the correct one (other wrong ones will lead to lava). The AI should hit the controling redstone at proper time to switch railways to ride on correct one.

## Approach

At current stage, we are using reinforcement learning and Q-Learning algorithm. For the QNetwork model, we keep using torch and use a 6-layer forward-feeding neural network, but we consider to switch to Keras and frameworks such as RLib in the future. The structure of our model is as following: linear, ReLu, linear, ReLu, linear, Softmax. The observation the agent can get is nine nearby blocks of the agent that one block above the ground. These blocks will cover redstones for controlling railroads and wool block for hitting. As we optimize the design of our map, we might change the range of the observations. The model has 9 final states, corresponding to the actions the agent can choose. As we further increase the difficulty of the project problem and add more choices to the agent's inventory, we will also increase the number of states.

We change the usage of the default reward system in Malmo because we need to consider whether the agent hits the block with the tool in the same color. When the agent successfully hits the block, it will collect the item mined from the block. Therefore, we use RewardForCollectingItem handler as a signal sender. When the agent collects different items, we programmed the Malmo system to give different rewards, respectively. In the function that gets the rewards and process them, we use these rewards as signals, and check whether the signals are the same with the tool in the agent's hand, which is stored in a global variable. For the beginning stage, the reward function is simply adding rewards or substracting penalties, and the final score will be returned when one action ends. For future stages, we might make it more complicated and change the time the agent knows the score.

The QNetwork will be updated after every 200 frames. Gradient-descending and backpropagating are applied and change weights in the state_dict correspondingly.

## Evaluation

Quantitatively, the total score the agent receives after completing each episode is one evaluation criteria. The higher the score, the longer the agent lives, and the better its performance is. Scores will consist of different parts including living (penalty for not hitting lever and ride into lava), correct hitting (hit the block with the tool in the same color), and hitting timing. We will use random agents as the first baseline, human-player score as the second baseline, and train the agent to perform better than act randomly and manually. In next stages, more tools and levers will be added to the map, and the evaluation process will start again.

For qualitative evaluation, we will check the final result and check how the agent makes decisions. Decisions includes turn, attack, pitch, and hotbar switch. If the agent mostly makes necessary decisions, then it will pass qualitative evalutaion perfectly. If not, then it might need improvements besides of quatitative evaluations. 

## Remaining Goals and Challenges

For challenges:

- (C1) It is quite hard to start the project with a scene in which the agent is sitting inside of the minecart and makes it hit the lever and start riding. DrawItem fails to draw minecart on the railroad, and the "use" command fails in discrete command mode.
- (C2) Moving and turning are relatively simple in discrete command mode, but hard in continuous mode, because it needs a stop signal to stop moving or turning. When to send the stop signal and how to make the agent learn to stop are quite difficult.
- (C3) The default reward system can't tell whether the agent hits the block with the tool in the same color.
- (C4) The current observation is limited. Since the cart goes fast, it might not be enough for the agent to learn.
- (C5) The current QNetwork sometimes makes the agent trap in turning and pitching.
- (C6) Due to the design of the map, sometimes the agent fails to collect the items after hitting blocks, because the items might fell down to the ground.

For solutions we have currently:

- (C1) We designed a group of initialization missions to ask the agent to put the cart on the railroad, take the cart, and turn around first. After initialization missions are completed, normal training will start. Because "use" command fails in discrete mode, we will consider to use continuous command mode.
- (C2) This problem will occur because we try to solve C1. Temporarily to complete latter parts of our project, we might consider to manually make the agent ride the cart, and let it learn by itself. In this case, we can continue to use discrete mode. In this case, we can continue to use discrete mode.
- (C3) As described in Approach part, we will use user-defined reward functions and use the default reward system as a signal system.

Therefore, for goals and future plans:

- Fix command mode and allows for a random agent to ride on the cart and explore the world smoothly rather than trap in one same spot repetitively turning or pitching.
- Improve implementation of reward systems and corresponding handlers.
- Finish implementation of a basic QNetwork in torch and record performance.
- Search for other reinforcement learning frameworks and libraries to further improve the performance of the agent, time to train, and the resources the agent receives.

## Resources Used

- Project Malmo - [https://microsoft.github.io/malmo/0.14.0/Documentation/classmalmo_1_1_agent_host.html#ac1421c4ed9ababff1300ea58a37859bc](https://microsoft.github.io/malmo/0.14.0/Documentation/classmalmo_1_1_agent_host.html#ac1421c4ed9ababff1300ea58a37859bc)
- XML Schema Documentation - [https://microsoft.github.io/malmo/0.30.0/Schemas/MissionHandlers.html#element_ContinuousMovementCommands](https://microsoft.github.io/malmo/0.30.0/Schemas/MissionHandlers.html#element_ContinuousMovementCommands)
- DQN - [https://blog.csdn.net/war3gu/article/details/90641076](https://blog.csdn.net/war3gu/article/details/90641076)
- Gitter Microsoft/Malmo - [https://gitter.im/Microsoft/malmo?at=5a5ddf51290a1f456194c199](https://gitter.im/Microsoft/malmo?at=5a5ddf51290a1f456194c199)
- UCI CS 175 HW2 (Due to copyright, we will not include the link to Canvas page here)
- Malmo Platform Tutorial - [https://microsoft.github.io/malmo/0.17.0/Python_Examples/Tutorial.pdf](https://microsoft.github.io/malmo/0.17.0/Python_Examples/Tutorial.pdf)
- "use 1" command does not work with DiscreteMovementCommand - [https://github.com/microsoft/malmo/issues/887](https://github.com/microsoft/malmo/issues/887)
- Redstone Logic Circuit - [https://minecraft.gamepedia.com/Mechanics/Redstone/Logic_circuit](https://minecraft.gamepedia.com/Mechanics/Redstone/Logic_circuit)
- Redstone Transmission Circuit - [https://minecraft.gamepedia.com/Mechanics/Redstone/Transmission_circuit](https://minecraft.gamepedia.com/Mechanics/Redstone/Transmission_circuit)

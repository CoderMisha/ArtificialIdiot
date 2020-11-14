---
layout: default
title:  Home
---
# {{ page.title }}

## Topics

Minecraft, Reinforcement Learning, Beat-Saber, Dancing-Line

## Summary

We are planning to train an AI to play a minigame integrated with features in Beat-Saber and Dancing-Line in Minecraft (similar to the map in this YouTube video: Zedd & Jasmine Thompson - Funny (Minecraft Music Video \| Beat Synchronized!) but also included features similar to dancing line (reference to this YouTube video: Dancing Line \| The Piano %100 10/10 Gems)). 

![algorithm visualize](https://raw.githubusercontent.com/WendyWjt/ArtificialIdiot/main/docs/_images/on_cart_20201113.png)

The task of the AI is trying to hit the block along the railroad while riding on it with swords in the same color with the block at the proper time (i.e. right before the block is passing the agent). A correct and precise hit will increase the AI's score, and a miss or hitting with a sword in wrong color would decrease the score. The AI should take the game frame as input and perform "aim" and "attack" action correspondingly.

![algorithm visualize](https://raw.githubusercontent.com/WendyWjt/ArtificialIdiot/main/docs/_images/choice_20201113.png)

To make this task more challenging, the AI will encounter multiple rail ways and have to choose the correct one (other wrong ones will lead to lava).

## Source Code

[https://github.com/WendyWjt/ArtificialIdiot](https://github.com/WendyWjt/ArtificialIdiot)

## Reference

- Zedd \& Jasmine Thompson - Funny (Minecraft Music Video \| Beat Synchronized!) - [https://www.youtube.com/watch?v=Wm0wFAJr1Xo](https://www.youtube.com/watch?v=Wm0wFAJr1Xo)
- Dancing Line \| The Piano %100 10/10 Gems - [https://www.youtube.com/watch?v=FeSOAljGR80](https://www.youtube.com/watch?v=FeSOAljGR80)

---
layout: default
title: Proposal
---

# {{ page.title }}

## Summary

We are planning to train an AI to play a *Beat-Saber-like* minigame in *Minecraft* (similar to the map in this YouTube video: [Zedd & Jasmine Thompson - Funny (Minecraft Music Video | Beat Synchronized!)](https://youtu.be/Wm0wFAJr1Xo)). The task of the AI is trying to hit the block along the railroad while riding on it with swords in the same color with the block. A correct hit will increase the AI's score, and a miss or hitting with a sword in wrong color would decrease the score. The AI should take the game frame as input and perform "attack" action correspondingly.

## AI/ML Algorithms

Object Detection? Neural Network?

## Evaluation Plan

As described in summary, the score that the AI earns can be used as metric. More specifically, a miss should decrease more score than a wrong color hit, since the later should be easier to improve on.

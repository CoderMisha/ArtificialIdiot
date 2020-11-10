# QNetwork && Rewards

import time
from tqdm import tqdm
from collections import deque
import numpy as np
from numpy.random import randint
import json
import random

import torch
import torch.nn as nn

import cs175_utils
import cs175_hyperparameter

# Hyperparameters
SIZE = 50
REWARD_DENSITY = .1
PENALTY_DENSITY = .02
OBS_SIZE = 5
MAX_EPISODE_STEPS = 100000000000000000000000000000000000000 # 100
MAX_GLOBAL_STEPS = 100000000000000000000000000000000000000 # 10000
REPLAY_BUFFER_SIZE = 10000
EPSILON_DECAY = .999
MIN_EPSILON = .1
BATCH_SIZE = 128
GAMMA = .9
TARGET_UPDATE = 100
LEARNING_RATE = 1e-4
START_TRAINING = 500
LEARN_FREQUENCY = 1
ACTION_DICT = {
    0: 'move 1',  # Turn right (?
    1: 'turn 1',  # Turn left (?
    # The slots are 0-indexed but the key commands are 1-indexed
    2: 'hotbar.2 1',  # Hotbar No.1: diamond pickaxe
    3: 'hotbar.3 1',  # Hotbar No.2: golden pickaxe
}

#####
current_tool = None


# Q-Value Network
class QNetwork(nn.Module):
    def __init__(self, obs_size, action_size, hidden_size=100):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(np.prod(obs_size), hidden_size),
                                 nn.ReLU(),
                                 nn.Linear(hidden_size, 32),
                                 nn.ReLU(),
                                 # nn.Linear(hidden_size, action_size)
                                 nn.Linear(32, action_size)
                                 )

    def forward(self, obs):
        """
        Estimate q-values given obs

        Args:
            obs (tensor): current obs, size (batch x obs_size)

        Returns:
            q-values (tensor): estimated q-values, size (batch x action_size)
        """
        batch_size = obs.shape[0]
        obs_flat = obs.view(batch_size, -1)
        return self.net(obs_flat)


def get_action(obs, q_network, epsilon, allow_break_action):
    """
    Select action according to e-greedy policy

    Args:
        obs (np-array): current observation, size (obs_size)
        q_network (QNetwork): Q-Network
        epsilon (float): probability of choosing a random action

    Returns:
        action (int): chosen action [0, action_size)
    """
    # Prevent computation graph from being calculated
    with torch.no_grad():
        # Calculate Q-values fot each action
        obs_torch = torch.tensor(obs.copy(), dtype=torch.float).unsqueeze(0)
        action_values = q_network(obs_torch)

        # Remove attack/mine from possible actions if not facing a diamond
        if not allow_break_action:
            action_values[0, 3] = -float('inf')

            # Select action with highest Q-value
        # action_idx = torch.argmax(action_values).item()
        argmax_idx = torch.argmax(action_values).item()
        prob = [0, 0, 0, 0]
        for i in range(4):
            if i == argmax_idx:
                prob[i] = 1 - epsilon
            else:
                prob[i] = epsilon / 3
        action_idx = np.random.choice([0, 1, 2, 3], 1, p=prob)[0]
        # action_idx = torch.argmax(action_values).item()
    #return action_idx
    return random.choice([2, 3])


def get_observation(agent_host, world_state):
    """
    Use the agent observation API to get a 2 x 5 x 5 grid around the agent.
    The agent is in the center square facing up.

    Args
        world_state: <object> current agent world state

    Returns
        observation: <np.array>
    """
    obs = np.zeros((2, OBS_SIZE, OBS_SIZE))

    while world_state.is_mission_running:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:
            # First we get the json from the observation API
            msg = world_state.observations[-1].text
            observations = json.loads(msg)

            # Get observation
            grid = observations['nearby']
            grid_binary = [1 if x == 'diamond_ore' or x == 'lava' else 0 for x in grid]
            obs = np.reshape(grid_binary, (2, OBS_SIZE, OBS_SIZE))

            # Rotate observation with orientation of agent
            yaw = observations['Yaw']
            if yaw == 270:
                obs = np.rot90(obs, k=1, axes=(1, 2))
            elif yaw == 0:
                obs = np.rot90(obs, k=2, axes=(1, 2))
            elif yaw == 90:
                obs = np.rot90(obs, k=3, axes=(1, 2))

            break

    return obs


def prepare_batch(replay_buffer):
    """
    Randomly sample batch from replay buffer and prepare tensors

    Args:
        replay_buffer (list): obs, action, next_obs, reward, done tuples

    Returns:
        obs (tensor): float tensor of size (BATCH_SIZE x obs_size
        action (tensor): long tensor of size (BATCH_SIZE)
        next_obs (tensor): float tensor of size (BATCH_SIZE x obs_size)
        reward (tensor): float tensor of size (BATCH_SIZE)
        done (tensor): float tensor of size (BATCH_SIZE)
    """
    batch_data = random.sample(replay_buffer, BATCH_SIZE)
    obs = torch.tensor([x[0] for x in batch_data], dtype=torch.float)
    action = torch.tensor([x[1] for x in batch_data], dtype=torch.long)
    next_obs = torch.tensor([x[2] for x in batch_data], dtype=torch.float)
    reward = torch.tensor([x[3] for x in batch_data], dtype=torch.float)
    done = torch.tensor([x[4] for x in batch_data], dtype=torch.float)

    return obs, action, next_obs, reward, done


def learn(batch, optim, q_network, target_network):
    """
    Update Q-Network according to DQN Loss function

    Args:
        batch (tuple): tuple of obs, action, next_obs, reward, and done tensors
        optim (Adam): Q-Network optimizer
        q_network (QNetwork): Q-Network
        target_network (QNetwork): Target Q-Network
    """
    obs, action, next_obs, reward, done = batch

    optim.zero_grad()
    values = q_network(obs).gather(1, action.unsqueeze(-1)).squeeze(-1)
    target = torch.max(target_network(next_obs), 1)[0]
    target = reward + GAMMA * target * (1 - done)
    loss = torch.mean((target - values) ** 2)
    loss.backward()
    optim.step()

    return loss.item()


def _hit_reward(reward_signal: int):
    if reward_signal in (2, 3):
        if reward_signal == current_tool:
            return 2    # reward for correct hits
        else:
            return -2
    else:
        return 0


def _switch_tool(command):
    if command in (2, 3):
        current_tool = command


def train(agent_host, mission_xml):
    """
    Main loop for the DQN learning algorithm

    Args:
        agent_host (MalmoPython.AgentHost)
    """
    q_network = QNetwork((2, OBS_SIZE, OBS_SIZE), len(ACTION_DICT))
    target_network = QNetwork((2, OBS_SIZE, OBS_SIZE), len(ACTION_DICT))
    target_network.load_state_dict(q_network.state_dict())

    # Init optimizer
    optim = torch.optim.Adam(q_network.parameters(), lr=LEARNING_RATE)

    # Init replay buffer
    replay_buffer = deque(maxlen=REPLAY_BUFFER_SIZE)

    # Init vars
    global_step = 0
    num_episode = 0
    epsilon = 1
    start_time = time.time()
    returns = []
    steps = []

    # Begin main loop
    loop = tqdm(total=MAX_GLOBAL_STEPS, position=0, leave=False)
    while global_step < MAX_GLOBAL_STEPS:
        episode_step = 0
        episode_return = 0
        episode_loss = 0
        done = False

        # Setup Malmo
        agent_host = cs175_utils.init_malmo(agent_host, mission_xml)
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)
        # obs = get_observation(agent_host, world_state)

        # Run episode
        while world_state.is_mission_running:
            # Get action
            # allow_break_action = obs[1, int(OBS_SIZE / 2) - 1, int(OBS_SIZE / 2)] == 1
            action_idx = random.choice([0]) #, 2, 3]) # get_action(obs, q_network, epsilon, allow_break_action)
            command = ACTION_DICT[action_idx]
            _switch_tool(command)
            print("command:", command)
            # time.sleep(10)

            # Take step
            agent_host.sendCommand(command)

            # If your agent isn't registering reward you may need to increase this
            time.sleep(.2)

            # We have to manually calculate terminal state to give malmo time to register the end of the mission
            # If you see "commands connection is not open. Is the mission running?" you may need to increase this
            episode_step += 1
            '''
            if episode_step >= MAX_EPISODE_STEPS or \
                    (obs[0, int(OBS_SIZE / 2) - 1, int(OBS_SIZE / 2)] == 1 and \
                     obs[1, int(OBS_SIZE / 2) - 1, int(OBS_SIZE / 2)] == 0 and \
                     command == 'move 1'):
                done = True
                time.sleep(3)
            '''

            # Get next observation
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:", error.text)
            # next_obs = get_observation(world_state)

            # Get reward
            reward = 0
            time.sleep(3)
            for r in world_state.rewards:
                print("reward:", r.getValue())
                reward += _hit_reward(r.getValue())
            episode_return += reward

            # Store step in replay buffer
            # replay_buffer.append((obs, action_idx, next_obs, reward, done))
            # obs = next_obs

            # Learn
            global_step += 1
            '''
            if global_step > START_TRAINING and global_step % LEARN_FREQUENCY == 0:
                batch = prepare_batch(replay_buffer)
                loss = learn(batch, optim, q_network, target_network)
                episode_loss += loss

                if epsilon > MIN_EPSILON:
                    epsilon *= EPSILON_DECAY

                if global_step % TARGET_UPDATE == 0:
                    target_network.load_state_dict(q_network.state_dict())
            '''

        num_episode += 1
        returns.append(episode_return)
        steps.append(global_step)
        avg_return = sum(returns[-min(len(returns), 10):]) / min(len(returns), 10)
        loop.update(episode_step)
        loop.set_description(
            'Episode: {} Steps: {} Time: {:.2f} Loss: {:.2f} Last Return: {:.2f} Avg Return: {:.2f}'.format(
                num_episode, global_step, (time.time() - start_time) / 60, episode_loss, episode_return, avg_return))

        if num_episode > 0 and num_episode % 10 == 0:
            cs175_utils.log_returns(steps, returns)
            print()

# Rllib docs: https://docs.ray.io/en/latest/rllib.html

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import enum
import matplotlib.pyplot as plt
import numpy as np

import gym
import ray
from gym.spaces import Discrete, Box
from ray.rllib.agents import ppo
import pyautogui

# pyautogui
# Moving mouse with a distance of 100 pixels is equivalent to
# moving 15 degrees in game (at least on my computer)

import cs175_drawing


class NoobSaberAction(enum.Enum):
    NOP = 0
    ATTACK_LEFT = 1
    ATTACK_RIGHT = 2

    def short_name(self):
        if self == NoobSaberAction.NOP:
            return 'NOP'
        if self == NoobSaberAction.ATTACK_LEFT:
            return 'ATK_L'
        
        return 'ATK_R'  # ATTACK_RIGHT


class NoobSaber(gym.Env):
    def __init__(self, env_config):
        # Static Parameters
        self.size = 50
        self.reward_density = .1
        self.penalty_density = .02
        self.obs_size = 5
        self.max_episode_steps = 100
        self.log_frequency = 10
        self.action_list = list(NoobSaberAction)
        self.video_width = 640
        self.video_height = 480

        # Rllib Parameters
        self.action_space = Discrete(len(self.action_list))
        self.observation_space = Box(0, 1, shape=(np.prod([2, self.obs_size, self.obs_size]), ), dtype=np.int32)

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        try:
            self.agent_host.parse(sys.argv)
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # DiamondCollector Parameters
        self.obs = None
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def reset(self):
        """
        Resets the environment for the next episode.

        Returns
            observation: <np.array> flattened initial obseravtion
        """
        # Reset Malmo
        world_state = self.init_malmo()

        # Reset Variables
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        # Log
        if len(self.returns) > self.log_frequency and len(self.returns) % self.log_frequency == 0:
            self.log_returns()

        # Get Observation
        self.obs = self.get_observation(world_state)

        return self.obs.flatten()

    def step(self, action_idx):
        """
        Take an action in the environment and return the results.

        Args
            action_idx: <int> index of the action to take

        Returns
            observation: <np.array> flattened array of obseravtion
            reward: <int> reward from taking action
            done: <bool> indicates terminal state
            info: <dict> dictionary of extra information
        """

        # Get Action
        action = self.action_list[action_idx]
        self._make_action(action)
        time.sleep(.1)
        self.episode_step += 1

        # Get Done
        done = False
        if self.episode_step >= self.max_episode_steps:
            done = True
            time.sleep(2)

        # Get Observation
        world_state = self.agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
        self.obs = self.get_observation(world_state)

        # Get Reward
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()
        self.episode_return += reward

        return self.obs.flatten(), reward, done, dict()

    def get_mission_xml(self):
        return f'''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>CS 175 World Drawing</Summary>
            </About>

            <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>1000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;128*0;1;" />
                    <DrawingDecorator>
                        {cs175_drawing.map_generated}
                    </DrawingDecorator>
                </ServerHandlers>
            </ServerSection>

            <AgentSection mode="Survival">
                <Name>Artificial Idiot</Name>
                <AgentStart>
                    <Placement x="3.5" y="11" z="0.5" yaw="90" pitch="65"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_pickaxe"/>
                        <InventoryItem slot="1" type="golden_pickaxe"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <DiscreteMovementCommands/>
                    <ObservationFromFullStats/>
                    <ObservationFromHotBar/>
                    <ObservationFromFullInventory/>
                    <ObservationFromRay/>
                    <ObservationFromGrid>
                        <Grid name="floorAll">
                            <min x="-{int(self.obs_size/2)}" y="-1" z="-{int(self.obs_size/2)}"/>
                            <max x="{int(self.obs_size/2)}" y="0" z="{int(self.obs_size/2)}"/>
                        </Grid>
                    </ObservationFromGrid>
                    <InventoryCommands/>
                    <ColourMapProducer>
                        <Width>{self.video_width}</Width>
                        <Height>{self.video_height}</Height>
                    </ColourMapProducer>
                    <AgentQuitFromReachingCommandQuota total="{self.max_episode_steps + 1}" />
                </AgentHandlers>
            </AgentSection>
        </Mission>'''

    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        # add Minecraft machines here as available
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000))
        time.sleep(10)

        for retry in range(max_retries):
            try:
                self.agent_host.startMission(
                    my_mission,
                    my_clients,
                    my_mission_record,
                    0,
                    'NoobSaber'
                )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)

        pyautogui.press('enter')
        pyautogui.rightClick()

        # head's up
        pyautogui.move(0, -200)
        pyautogui.move(0, -200)
        pyautogui.move(0, -50)

        # turn around
        for _ in range(6):
            pyautogui.move(-200, 0)
        
        # hit redstone to start
        pyautogui.move(200, 0)
        self.agent_host.sendCommand('attack 1')
        pyautogui.move(-200, 0)

        pyautogui.press('enter')

        return world_state

    def get_observation(self, world_state):
        """
        Use the agent observation API to get a 2 x 5 x 5 grid around the agent. 
        The agent is in the center square facing up.

        Args
            world_state: <object> current agent world state

        Returns
            observation: <np.array>
        """
        obs = np.zeros((2, self.obs_size, self.obs_size))

        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                # First we get the json from the observation API
                msg = world_state.observations[-1].text
                observations = json.loads(msg)

                # Get observation
                grid = observations['floorAll']
                grid_binary = [1 if x == 'diamond_ore' or x == 'lava' else 0 for x in grid]
                obs = np.reshape(grid_binary, (2, self.obs_size, self.obs_size))

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

    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns, box, mode='same')
        plt.clf()
        plt.plot(self.steps, returns_smooth)
        plt.title('Diamond Collector')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns.png')

        with open('returns.txt', 'w') as f:
            for step, value in zip(self.steps, self.returns):
                f.write("{}\t{}\n".format(step, value))

    def _make_action(self, action: NoobSaberAction):       
        if action == NoobSaberAction.NOP:
            pass
        elif action == NoobSaberAction.ATTACK_LEFT:
            pyautogui.press('enter')
            pyautogui.move(-200, 0)
            self.agent_host.sendCommand('attack 1')
            pyautogui.move(200, 0)
            pyautogui.press('enter')
        elif action == NoobSaberAction.ATTACK_RIGHT:
            pyautogui.press('enter')
            pyautogui.move(200, 0)
            self.agent_host.sendCommand('attack 1')
            pyautogui.move(-200, 0)
            pyautogui.press('enter')


if __name__ == '__main__':
    ray.init()
    trainer = ppo.PPOTrainer(env=NoobSaber, config={
        'env_config': {},           # No environment parameters to configure
        'framework': 'torch',       # Use pyotrch instead of tensorflow
        'num_gpus': 0,              # We aren't using GPUs
        'num_workers': 0            # We aren't using parallelism
    })

    while True:
        print(trainer.train())

# Rllib docs: https://docs.ray.io/en/latest/rllib.html
# PPO: https://docs.ray.io/en/master/rllib-algorithms.html#ppo

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import enum
import matplotlib.pyplot as plt
import numpy as np

import gym
import ray
from gym.spaces import Discrete, Box
from ray.rllib.models import ModelCatalog
from ray.rllib.agents import ppo, dqn, trainer
import pyautogui
from PIL import Image

# pyautogui
# Moving mouse with a distance of 100 pixels is equivalent to
# moving 15 degrees in game (at least on my computer)

import cs175_drawing
from cs175_model import NoobSaberTorchModel
ModelCatalog.register_custom_model('my_model', NoobSaberTorchModel)


class NoobSaberAction(enum.Enum):
    NOP = 0
    ATTACK_LEFT = 1
    ATTACK_LEFT_DOWN = 2
    ATTACK_LEFT_UP = 3
    ATTACK_UP = 4
    ATTACK_RIGHT = 5
    ATTACK_RIGHT_DOWN = 6
    ATTACK_RIGHT_UP = 7
    SWITCH = 8

    def short_name(self):
        return ['NOP', '←', '↙', '↖', '↑', '→', '↘', '↗', 'SWITCH'][self.value]


class NoobSaber(gym.Env):
    def __init__(self, env_config):
        # Static Parameters
        self.size = 50
        self.reward_density = .1
        self.penalty_density = .02
        self.obs_size = 5
        self.max_episode_steps = 500
        self.log_frequency = 5
        self.action_list = list(NoobSaberAction)

        self.obs_height = 314
        self.obs_width = 396

        # Rllib Parameters
        self.action_space = Discrete(len(self.action_list))
        self.observation_space = Box(0, 255, shape=(self.obs_height, self.obs_width, 3), dtype=np.int32)

        # Malmo Parameters
        self.video_width = 960
        self.video_height = 540
        self.agent_host = MalmoPython.AgentHost()
        try:
            self.agent_host.parse(sys.argv)
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # Parameters
        self.obs = None
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []
        self.pickaxe = 0 # 0: hotbar.1 ; 1:hotbar.2

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
        cur_frames = self.get_color_map_frames(world_state)
        if len(cur_frames) <= 0:
            return self._empty_obs()
        else:
            cur_frame = self._resize_frame_pixels(cur_frames[0])
            return cur_frame

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
        #pyautogui.press('enter')
        # Get Action
        # if action_idx == 2: # change "do nothing" to "switch pickaxe"
        #    action_idx = 3
        # action_idx = 2 if action_idx < 4 else 6
        action = self.action_list[action_idx]
        self._make_action(action)
        # print("action: ", action.short_name(), self.pickaxe)
        self.episode_step += 1
        # print("====New Step====", self.episode_step)

        world_state = self.agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
        #pyautogui.press('enter')

        # Get Done
        done = False
        if self.episode_step >= self.max_episode_steps or not world_state.is_mission_running:
            pyautogui.press('enter')
            done = True
            time.sleep(2)
            print("====Done==== Step:", self.episode_step, "|", self.returns, self.episode_return)
        
        # Get Observation
        cur_frames = self.get_color_map_frames(world_state)
        if len(cur_frames) <= 0:
            cur_frame = self._empty_obs()
        else:
            cur_frame = self._resize_frame_pixels(cur_frames[0])

        # Get Reward
        reward = 0
        # print("world state,", world_state)
        for r in world_state.rewards:
            # print(r, "+++",r.getValue())
            reward += self.apply_reward(r.getValue())
        self.episode_return += reward
        # print("Reward:", reward)
        return cur_frame, reward, done, dict()
    
    def apply_reward(self, reward):
        good_score, bad_score = 10, -1
        if reward == 55: # "blue block"
            return good_score if self.pickaxe == 0 else bad_score
        elif reward == 66: # "yellow block"
            return good_score if self.pickaxe != 0 else bad_score
        else:
            return reward


    def get_mission_xml(self):
        return f'''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>CS 175</Summary>
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
                    <ChatCommands/>
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
                    <RewardForTouchingBlockType>
                        <Block type="water" reward="10000" />
                        <Block type="lava" reward="-1000" />
                    </RewardForTouchingBlockType>
                    <RewardForTimeTaken initialReward="0" delta="0.1" density="PER_TICK" />
                    <RewardForCollectingItem>
                        <Item type="redstone_block" reward="100" />
                        <Item reward="55" type="wool" colour="LIGHT_BLUE" />
                        <Item reward="66" type="wool" colour="YELLOW" />
                    </RewardForCollectingItem>
                    <RewardForMissionEnd rewardForDeath="-1000">
                        <Reward reward="0" description="Mission End"/>
                    </RewardForMissionEnd>
                    <ColourMapProducer>
                        <Width>{self.video_width}</Width>
                        <Height>{self.video_height}</Height>
                    </ColourMapProducer>
                    <!-- <AgentQuitFromReachingCommandQuota total="{self.max_episode_steps}" /> -->
                    <AgentQuitFromTouchingBlockType>
                        <Block type="water" description="success" />
                        <Block type="lava" description="dead end" />
                    </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
            </AgentSection>
        </Mission>'''

    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(self.video_width, self.video_height)
        my_mission.setViewpoint(0)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        # add Minecraft machines here as available
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000))

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

        self.agent_host.sendCommand('hotbar.1 1')
        self.pickaxe = 0

        pyautogui.press('enter')
        pyautogui.rightClick()
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
        time.sleep(0.1)
        self.agent_host.sendCommand('attack 1')
        time.sleep(0.1)
        pyautogui.move(-200, 0)

        #pyautogui.press('enter')

        return world_state

    def get_color_map_frames(self, world_state):
        frames = []

        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()

            if len(world_state.errors) > 0:
                for idx, e in enumerate(world_state.errors):
                    print(f'error #{idx}: {e.text}', file=sys.stderr)
                raise RuntimeError('Could not load color map frame(s).')

            if world_state.number_of_video_frames_since_last_state > 0:
                for frame in world_state.video_frames:
                    if frame.frametype == MalmoPython.FrameType.COLOUR_MAP:
                        frames.append(frame)
                break
        #print("cur_frame:", len(frames), end = " | ")
        return frames

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
        plt.title('NoobSaber')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns.png')

        with open('returns.txt', 'w') as f:
            for step, value in zip(self.steps, self.returns):
                f.write("{}\t{}\n".format(step, value))

    def _make_action(self, action: NoobSaberAction):
        delay = 0.05
        if action == NoobSaberAction.NOP:
            self.agent_host.sendCommand('chat .')
        elif action == NoobSaberAction.ATTACK_LEFT:
            pyautogui.move(-225, 0)
            self.agent_host.sendCommand('attack 1')
            time.sleep(delay)
            pyautogui.move(225, 0)
        elif action == NoobSaberAction.ATTACK_RIGHT:
            pyautogui.move(225, 0)
            self.agent_host.sendCommand('attack 1')
            time.sleep(delay)
            pyautogui.move(-225, 0)
        elif action == NoobSaberAction.SWITCH:
            pyautogui.press('enter')
            if self.pickaxe == 0:
                self.agent_host.sendCommand('hotbar.2 1')
                time.sleep(delay)
                self.pickaxe += 1
            else:
                self.agent_host.sendCommand('hotbar.1 1')
                time.sleep(delay)
                self.pickaxe = 0
            pyautogui.press('enter')
        elif action == NoobSaberAction.ATTACK_LEFT_DOWN:
            pyautogui.move(-225, 225)
            self.agent_host.sendCommand('attack 1')
            time.sleep(delay)
            pyautogui.move(225, -225)
        elif action == NoobSaberAction.ATTACK_LEFT_UP:
            pyautogui.move(-225, -225)
            self.agent_host.sendCommand('attack 1')
            time.sleep(delay)
            pyautogui.move(225, 225)
        elif action == NoobSaberAction.ATTACK_UP:
            pyautogui.move(0, -225)
            self.agent_host.sendCommand('attack 1')
            time.sleep(delay)
            pyautogui.move(0, 225)
        elif action == NoobSaberAction.ATTACK_RIGHT_DOWN:
            pyautogui.move(225, 225)
            self.agent_host.sendCommand('attack 1')
            time.sleep(delay)
            pyautogui.move(-225, -225)
        elif action == NoobSaberAction.ATTACK_RIGHT_UP:
            pyautogui.move(225, -225)
            self.agent_host.sendCommand('attack 1')
            time.sleep(delay)
            pyautogui.move(-225, 225)
        

    def _resize_frame_pixels(self, frame):
        img = Image.frombytes(
            'RGB',
            (self.video_width, self.video_height),
            bytes(frame.pixels)
        )

        resized = img.resize((self.obs_width, self.obs_height))

        resized_arr = np.array(resized)

        img.close()
        resized.close()
        return resized_arr

    def _empty_obs(self):
        return np.zeros((self.obs_height, self.obs_width, 3), dtype=np.uint8)

if __name__ == '__main__':
    ray.init()
    # trainer = ppo.PPOTrainer(env=NoobSaber, config={
    #     'env_config': {},           # No environment parameters to configure
    #     'framework': 'torch',         # Use tensorflow
    #     'num_gpus': 0,              # ? If possible, use GPUs
    #     'num_workers': 0,           # We aren't using parallelism
    #     'model': {
    #         'custom_model': 'my_model',
    #         'custom_model_config': {},
    #     }
    # })

    trainer = dqn.DQNTrainer(env=NoobSaber, config={
        'env_config': {},
        'framework': 'torch',
        'num_gpus': 0,
        'num_workers': 0,
        'model': {
            'custom_model': 'my_model',
            'custom_model_config': {},
        }
    })

    while True:
        print("======Start======")
        #print("Train:", trainer.train())
        trainer.train()

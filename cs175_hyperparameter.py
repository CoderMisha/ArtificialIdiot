import cs175_drawing

SIZE = 50
REWARD_DENSITY = .1
PENALTY_DENSITY = .02
OBS_SIZE = 3
MAX_EPISODE_STEPS = 100
MAX_GLOBAL_STEPS = 10000
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
    # Discrete
    0: 'turn 1',    # Turn right (?
    1: 'turn -1',   # Turn left (?
    2: 'look 1',    # Look down
    3: 'look -1',   # Look up
    4: 'attack 1',  # Destroy block
    # The slots are 0-indexed but the key commands are 1-indexed
    5: 'hotbar.1 1',  # Hotbar No.1: diamond pickaxe
    6: 'hotbar.2 1'  # Hotbar No.2: golden pickaxe
    # Continuous
    # 0: 'turn 0.1',      # Turn right
    # 1: 'turn -0.1',     # Turn left
    # 2: 'turn 0',        # Stop turning
    # 3: 'pitch 0.1',     # Look down
    # 4: 'pitch -0.1',    # Look up
    # 5: 'pitch 0',       # Stop tilting head
    # 2: 'attack 1',  # Destroy block; -> attack 0
    # # The slots are 0-indexed but the key commands are 1-indexed
    # 3: 'hotbar.1 1',  # Hotbar No.1: diamond pickaxe; -> hotbar.1 0
    # 4: 'hotbar.2 1',  # Hotbar No.2: golden pickaxe; -> hotbar.2 0
}


reward_signal = '''
                    <Item reward="5" type="wool" colour="LIGHT_BLUE" />
                    <Item reward="6" type="wool" colour="YELLOW"/>
                '''


MISSION_XML = f'''<?xml version="1.0" encoding="UTF-8" ?>
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
                    
                    <ContinuousMovementCommands/>
                    <ObservationFromFullStats/>
                    <ObservationFromHotBar/>
                    <ObservationFromFullInventory/>
                    <ObservationFromRay/>
                    <InventoryCommands/>
                    <ObservationFromGrid>
                        <Grid name="nearby">
                            <min x="-1" y="0" z="-1" />
                            <max x="1" y="1" z="1" />
                        </Grid>
                    </ObservationFromGrid>
                    <RewardForCollectingItem>
                        {reward_signal}
                    </RewardForCollectingItem>
                </AgentHandlers>
            </AgentSection>

        </Mission>'''
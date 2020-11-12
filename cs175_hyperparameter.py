import cs175_drawing

SIZE = 50
REWARD_DENSITY = .1
PENALTY_DENSITY = .02
OBS_SIZE = 5
MAX_EPISODE_STEPS = 100000000000000000000000000000000000000 # 100
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
    # 0: 'move 1',  # Turn right (?
    # 1: 'turn 1',  # Turn left (?
    # The slots are 0-indexed but the key commands are 1-indexed
    2: 'hotbar.1 1',  # Hotbar No.1: diamond pickaxe
    3: 'hotbar.2 1',  # Hotbar No.2: golden pickaxe
}

reward_signal = '''
                    <Item reward="2" type="wool" colour="LIGHT_BLUE" />
                    <Item reward="3" type="wool" colour="YELLOW"/>
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
                    <Placement x="0" y="12" z="0" />
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_pickaxe"/>
                        <InventoryItem slot="1" type="golden_pickaxe"/>
                        <InventoryItem slot="2" type="minecart"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <DiscreteMovementCommands/>
                    <ObservationFromFullStats/>
                    <ObservationFromHotBar/>
                    <ObservationFromRay/>
                    <InventoryCommands/>
                    <ObservationFromGrid>
                        <Grid name="nearby">
                            <min x="-1" y="-1" z="-1" />
                            <max x="1" y="-1" z="1" />
                        </Grid>
                        <Grid name="far" absoluteCoords="true">
                            <min x="12" y="79" z="417" />
                            <max x="14" y="79" z="419" />
                        </Grid>
                        <Grid name="very_far" absoluteCoords="true">
                            <min x="-10711" y="55" z="347" />
                            <max x="-10709" y="55" z="349" />
                        </Grid>
                    </ObservationFromGrid>
                    <RewardForCollectingItem>
                        {reward_signal}
                    </RewardForCollectingItem>
                </AgentHandlers>
            </AgentSection>

        </Mission>'''
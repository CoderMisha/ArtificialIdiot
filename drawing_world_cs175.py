import MalmoPython
import malmoutils
import random
import time


def generate_beats(x1, x2, y, z, prob=0.67):
    ret = ''

    for x in range(x1 + 1, x2):
        if random.random() <= prob:
            ret += f'<DrawBlock type="air" x="{x}" y="{y}" z="{z}"/>'
    
    return ret


malmoutils.fix_print()

AGENT_HOST = MalmoPython.AgentHost()

MISSION_XML = f'''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>CS 175 World Drawing</Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;minecraft:bedrock,2*minecraft:dirt,minecraft:grass;1;" />
                <DrawingDecorator>
                    <DrawLine x1="-10" y1="4" z1="0" x2="150" y2="4" z2="0" type="air"/>

                    <DrawLine x1="-10" y1="4" z1="0" x2="-1" y2="4" z2="0" type="rail"/>
                    <DrawLine x1="121" y1="4" z1="0" x2="150" y2="4" z2="0" type="rail"/>

                    <DrawLine x1="0" y1="3" z1="0" x2="120" y2="3" z2="0" type="redstone_block"/>
                    <DrawLine x1="0" y1="4" z1="0" x2="120" y2="4" z2="0" type="golden_rail"/>

                    <DrawLine x1="5" y1="5" z1="1" x2="115" y2="5" z2="1" type="wool" colour="LIGHT_BLUE"/>
                    <DrawLine x1="5" y1="5" z1="-1" x2="115" y2="5" z2="-1" type="wool" colour="YELLOW"/>

                    {generate_beats(5, 115, 5, 1)}
                    {generate_beats(5, 115, 5, -1)}
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="1000" description="out_of_time" />
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Creative">
            <Name>Artificial Idiot</Name>
            <AgentStart>
                <Placement x="5" y="5" z="5" />
                <Inventory>
                    <InventoryItem slot="0" type="diamond_pickaxe"/>
                    <InventoryItem slot="1" type="golden_pickaxe"/>
                    <InventoryItem slot="2" type="minecart"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullStats/>
                <ContinuousMovementCommands turnSpeedDegs="180"/>
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
            </AgentHandlers>
        </AgentSection>

    </Mission>'''


MISSION = MalmoPython.MissionSpec(MISSION_XML, True)
MISSION_RECORD = MalmoPython.MissionRecordSpec()

MAX_RETRIES = 3
for retry in range(MAX_RETRIES):
    try:
        AGENT_HOST.startMission(MISSION, MISSION_RECORD)
        break
    except RuntimeError as e:
        if retry == MAX_RETRIES - 1:
            print("Error starting mission",e)
            print("Is the game running?")
            exit(1)
        else:
            time.sleep(2)

world_state = AGENT_HOST.peekWorldState()
while not world_state.has_mission_begun:
    time.sleep(0.1)
    world_state = AGENT_HOST.peekWorldState()

while world_state.is_mission_running:
    world_state = AGENT_HOST.peekWorldState()

print('Drawing is over - feel free to explore the world.')

import MalmoPython
import malmoutils

import time

import cs175_drawing

malmoutils.fix_print()

AGENT_HOST = MalmoPython.AgentHost()

MISSION_XML = f'''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>CS 175 World Drawing</Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;128*0;1;" />
                <DrawingDecorator>
                    {cs175_drawing.map_generated}
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="5000" description="out_of_time" />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Creative">
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
                <ObservationFromFullStats/>
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

print("Waiting for the mission to start ", end=' ')
world_state = AGENT_HOST.peekWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = AGENT_HOST.peekWorldState()

print()
print("Mission running ", end=' ')

while world_state.is_mission_running:
    print(".", end="")
    time.sleep(1)
    world_state = AGENT_HOST.peekWorldState()

print()
print('Drawing is over - feel free to explore the world.')

import MalmoPython
import malmoutils
import time
from tqdm import tqdm
from collections import deque

import cs175_QNetwork
import cs175_hyperparameter

def main():
    malmoutils.fix_print()
    AGENT_HOST = MalmoPython.AgentHost()
    cs175_QNetwork.train(AGENT_HOST, cs175_hyperparameter.MISSION_XML)
    '''
    MISSION = MalmoPython.MissionSpec(cs175_hyperparameter.MISSION_XML, True)
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
    '''


if __name__ == "__main__":
    main()

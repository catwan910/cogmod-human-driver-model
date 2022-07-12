# from prompt_toolkit import prompt
from research import ResearchFactory
from lib import MapNames
import research
import logging
from lib.SimulationMode import SimulationMode


def ResearchVisual():
    max_ticks = 100
    host = "127.0.0.1"
    port = 2000
    defaultLogLevel = logging.INFO
    output_dir = "logs"
    map = MapNames.straight_road_with_parking
    simulationMode = SimulationMode.ASYNCHRONOUS
    act_id = 'setting1'

    research = ResearchFactory.createResearchVisual(maxTicks=max_ticks,
                                                    host=host,
                                                    port=port,
                                                    defaultLogLevel=defaultLogLevel,
                                                    output_dir=output_dir,
                                                    map=map,
                                                    simulationMode=simulationMode,
                                                    act_id=act_id)


    

if __name__ == '__main__':
   ResearchVisual()

   
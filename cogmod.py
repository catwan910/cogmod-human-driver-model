# from prompt_toolkit import prompt
from research import ResearchFactory
from lib import MapNames
import research
import logging
from lib.SimulationMode import SimulationMode


def ResearchCogMod():

    max_ticks = 100
    host = "127.0.0.1"
    port = 2000
    defaultLogLevel = logging.INFO
    output_dir = "logs"
    map = MapNames.t_junction
    simulationMode = SimulationMode.ASYNCHRONOUS
    act_id = 'setting1'

    research = ResearchFactory.createResearchCogMod(maxTicks=max_ticks,
                                                    host=host,
                                                    port=port,
                                                    defaultLogLevel=defaultLogLevel,
                                                    output_dir=output_dir,
                                                    map=map,
                                                    simulationMode=simulationMode,
                                                    act_id=act_id)


if __name__ == '__main__':
    ResearchCogMod()



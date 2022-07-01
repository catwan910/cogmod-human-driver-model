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
    map = MapNames.t_junction
    simulationMode = SimulationMode.ASYNCHRONOUS

    

if __name__ == '__main__':
   ResearchVisual()
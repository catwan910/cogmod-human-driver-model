# from prompt_toolkit import prompt
from research import ResearchFactory
from lib import MapNames
import research
import logging


def ResearchCogMod(max_ticks=100):

    host = "127.0.0.1"
    port = 2000
    defaultLogLevel = logging.INFO
    output_dir = "logs"
    map = MapNames.straight_road_with_parking
    simulation_id = 'setting1'

    research = ResearchFactory.createResearchCogMod1()


if __name__ == '__main__':
    ResearchCogMod(100)



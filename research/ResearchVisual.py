from asyncio.log import logger
import logging
import math
from random import random
import time
from unittest import result
import carla

from lib.MapManager import MapNames

from .BaseResearch import BaseResearch
from settings.ExtendedSettingsManager import CogModSettingsManager
from agents.pedestrians import PedestrianFactory
from agents.vehicles import VehicleFactory
from lib import Simulator, SimulationMode
from lib import Utils

class ResearchVisual(BaseResearch):
    def __init__(self, name: str, 
                 client: carla.Client, 
                 mapName: MapNames, 
                 logLevel: logging, 
                 outputDir: str, 
                 simulationMode: SimulationMode):
        self.name = 'Research Visual'
        super().__init__(name, 
                         client, 
                         mapName, 
                         logLevel, 
                         outputDir, 
                         simulationMode)
        print('research visual')
        self.vehicleFactory = VehicleFactory(self.client, visualizer=self.visualizer)

        self.spawn_points = self.mapManager.spawn_points

        for sp in self.spawn_points:
            print(sp.location)
            try:
                self.vehicleFactory.spawn(sp)
            except Exception as e:
                print(e)
                pass

        
        


    


    


    
        

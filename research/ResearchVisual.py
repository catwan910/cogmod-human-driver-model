# from asyncio.log import logger
import logging
# import math
from random import choice
# import time
# from unittest import result
import carla

from lib.MapManager import MapNames
# from lib.SimulationVisualization import SimulationVisualization

from .BaseResearch import BaseResearch

from settings.ExtendedSettingsManager import CogModSettingsManager
from settings.visual_setting import visual_settings
from agents.vehicles import VehicleFactory
from lib import Simulator, SimulationMode
# from lib import Utils

class ResearchVisual(BaseResearch):
    def __init__(self, name: str, 
                 client: carla.Client, 
                 mapName: MapNames, 
                 logLevel: logging, 
                 outputDir: str, 
                 simulationMode: SimulationMode,
                 act_id: str):
        self.name = 'Research Visual'
        super().__init__(name, 
                         client, 
                         mapName, 
                         logLevel, 
                         outputDir, 
                         simulationMode)

        self.act_id = act_id
        self.simulator = None

        self.settingsManager = CogModSettingsManager(self.client, visual_settings)  
        self.vehicleFactory = VehicleFactory(self.client, visualizer=self.visualizer)

        self.cogmod_agent_settings = {}
        self.static_elements_settings = []

        self.cogmod_agent = None
        self.static_element_list = []

        # self.bpLib = self.world.get_blueprint_library()
        # self.staticBps = self.bpLib.filter('static.prop.barrel')
        self.setup()



    def setup(self):
        self.settingsManager.load(self.act_id)
        self.cogmod_agent_settings, self.static_elements_settings = self.settingsManager.getVisualModuleSettings()

        # spawn_points = self.map.get_spawn_points()
        # increment = 3
        # start_valX = -100

        # for Bps in self.staticBps:
        #     start_valX = start_valX + increment
        #     start = carla.Location(x=-start_valX, y=8, z=1)
        #     start_transform = carla.Transform(start, carla.Rotation(0, 0, 0))
        #     static_elem  = self.world.spawn_actor(Bps, start_transform)






        # for spawn_point in spawn_points:
        #     staticBp = choice(self.staticBps)
        #     static_elem  = self.world.spawn_actor(staticBp, spawn_point)
        



        # for Bps in self.staticBps:
        #     if Bps.has_attribute('role_name'):
        #         print('has attribute ', Bps.id)
            # print('role name ', Bps.role_name)

        # self.cogmod_agent_settings, self.static_elements_settings = self.settingsManager.getVisualModuleSettings()

        
        
        
        

        
        

        


        
        

        
        


    


    


    
        

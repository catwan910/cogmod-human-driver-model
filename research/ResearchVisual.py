# from asyncio.log import logger
import logging
# import math
from random import choice
import time
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

        self.cogmod_agent_setting = {}
        self.static_elements_setting = []

        self.cogmod_agent = None
        self.static_element_list = []

        # self.bpLib = self.world.get_blueprint_library()
        # self.staticBps = self.bpLib.filter('static.prop.barrel')
        self.setup()

    def destroyCogModAgent(self):
        self.logger.warn('destroying CogMod agent')
        self.cogmod_agent.get_vehicle().destroy()
        self.cogmod_agent = None
        pass

    def destroyStaticElements(self):
        self.logger.warn('destroying static elements')
        for static_elem in self.static_element_list:
            self.logger.info(f"Need to destroying static element {static_elem}")
        pass

    def destroyAll(self):
        self.destroyCogModAgent()
        self.destroyStaticElements()
        pass

    def setup(self):
        self.settingsManager.load(self.act_id)
        self.cogmod_agent_setting, self.static_elements_setting = self.settingsManager.getVisualModuleSettings()
        # self.logger.info(f"cogmod agent setting: {self.cogmod_agent_setting}")
    
    def onTick(self, world_snapshot):
        if self.cogmod_agent is None:
            self.logger.error("cogmod agent is None")
            return
        
        # print('agent location ', self.cogmod_agent.get_vehicle().get_location())

        cogmod_control = self.cogmod_agent.update_agent([])
        if cogmod_control is not None:
            self.cogmod_agent.vehicle.apply_control(cogmod_control)
            # print('cogmod control ', cogmod_control)
        else:
            print('control is None')
        pass

    def updateSpectator(self, world_snapshot):
        spectator = self.world.get_spectator()
        vehicle_location = self.cogmod_agent.get_vehicle().get_location()
        spectator_location = carla.Location(vehicle_location.x, 
                                            vehicle_location.y, 
                                            50)
        spectator.set_transform(carla.Transform(spectator_location, carla.Rotation(pitch=-90)))
        
        pass

    def onEnd(self):
        self.logger.info('onEnd: destroying all static elements and cogmod agent')
        self.destroyAll()
        self.cogmod_agent = None
        self.static_element_list = []
        pass



    def run(self, maxTicks=5000):
        
        self.logger.info('running the simulation with maxTicks: {}'.format(maxTicks))
        self.spawnCogModAgent()
        self.spawnStaticElements()
        self.world.wait_for_tick()
        time.sleep(1)

        onTickers = [self.onTick, self.updateSpectator]
        onEnders = [self.onEnd]

        self.simulator = Simulator(self.client, 
                                   onTickers=onTickers,
                                   onEnders=onEnders,
                                   simulationMode=self.simulationMode)
        self.simulator.run(maxTicks)
        pass


    def spawnCogModAgent(self):
        spawn_transform = self.cogmod_agent_setting["spawn_transform"]
        destination_transform = self.cogmod_agent_setting["destination_transform"]
        driver_profile = self.cogmod_agent_setting["driver_profile"]

        vehicle = self.vehicleFactory.spawn(spawn_transform)
        if vehicle is None:
            self.logger.error("Could not spawn a vehicle")
            exit("cannot spawn cogmod vehicle")
        else:
            self.logger.info(f"successfully spawned cogmod actor {vehicle.id}")

        self.cogmod_agent = self.vehicleFactory.createCogModAgent(1, vehicle, destination_transform, driver_profile)
        pass


    def spawnStaticElements(self):
        bpLib = self.world.get_blueprint_library()
        for setting in self.static_elements_setting:
            spawn_transform = setting[0]
            type = setting[1]
            bp = bpLib.filter('static.prop.'+type)[0]
            static_elem  = self.world.spawn_actor(bp, spawn_transform)
            self.static_element_list.append(static_elem)
            pass
        self.logger.info(f"spawning static elements {self.static_element_list}")
        pass


        

        


        
        

        
        


    


    


    
        

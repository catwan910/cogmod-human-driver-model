from asyncio.log import logger
import logging
import math
from random import random
import time
from unittest import result
import carla

from lib.MapManager import MapNames
from lib.SimulationVisualization import SimulationVisualization

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
        

        self.spawnLocation = (-55, 11)
        self.spawnLocation = self.convert_coordinates_to_transform(self.spawnLocation)

        self.vehicle = self.spawn_vehicle(self.spawnLocation)

        self.visualizer = SimulationVisualization(self.client, self.mapManager)

        self.visualizer.drawPoint(location=self.vehicle.get_location(), size=1, life_time=100)


        

        

    def draw_circle(self):

        pass
    def spawn_vehicle(self, location):
        # print(location)
        self.vehicleFactory = VehicleFactory(self.client, visualizer=self.visualizer)
        vehicle = self.vehicleFactory.spawn(location)
        return vehicle
        pass
        

    def convert_coordinates_to_transform(self, coordinates, z = 0.0):

        location = carla.Location(x = coordinates[0], y = coordinates[1], z = z)

        waypoint = self.map.get_waypoint(location, project_to_road=True, lane_type=carla.LaneType.Driving)
        if waypoint is None:
            msg = f"{self.name}: Cannot create way point near {location}"
            self.error(msg)
        transform = carla.Transform(location = waypoint.transform.location + carla.Location(z=1), rotation = waypoint.transform.rotation)
        
        return transform

        
        

        
        


    


    


    
        

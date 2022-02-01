import carla
from lib import ActorManager, ObstacleManager, Utils, LoggerFactory
from .GapModel import GapModel
from .PedestrianAgent import PedestrianAgent
import random

class PedGapModel(GapModel):

    def __init__(self, agent: PedestrianAgent, actorManager: ActorManager, obstacleManager: ObstacleManager, factors = None) -> None:

        super().__init__(agent, actorManager, obstacleManager)
        self.name = f"PedGapModel #{agent.id}"
        self.logger = LoggerFactory.create(self.name)

        self.factors = factors
        self.initFactors()

        pass

    
    def initFactors(self):
        if self.factors is None:
            self.factors = {}
        
        if "desired_gap" not in self.factors:
            self.factors["desired_gap"] = 15 
        
        pass

    @property
    def desiredGap(self):
        return self.factors["desired_gap"]

    def calculateForce(self):

        if self.agent.isCrossing():
            # random will not work. The force should be off while pedestrian is not on road
            # idea: if nearest waypoint is too far, that means pedestrian is not worried about on coming vehicle. But carla waypoint calculation is not reliable
            return Utils.createRandomVector(0, 0.5) # TODO implement force based on distance
        return carla.Vector3D() # in othe states this model does not produce force

    
    def canCross(self):

        if self.agent.isCrossing():
            True
        
        d = self.distanceFromOncomingVehicle()
        if d is None:
            return True

        # TODO implement the actual gap model. This is very straight forward
        if d > self.desiredGap:
            return True

        self.logger.info(f"Cannot cross as distance distance to oncoming vehicle {d} <= {self.desiredGap}")
        return False

    
    def distanceFromOncomingVehicle(self):
        # TODO we are now just measuring distance from all actors
        vehicle = self.actorManager.getNearestOnComingVehicle()
        if vehicle is None:
            self.logger.info(f"No oncoming vehicle")
            return None
        distance = self.actorManager.getCurrentDistance(vehicle)
        self.logger.debug(f"Distance from nearest oncoming vehicle = {distance}")
        return distance
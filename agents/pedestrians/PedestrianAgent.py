from msilib.schema import Error
import time
import carla
import logging
from .InfoAgent import InfoAgent
from lib import SimulationVisualization

class PedestrianAgent(InfoAgent):
    
    def __init__(self, walker, desired_speed=1.5, time_delta=0.1, visualizer=None, config=None):
        """
        Initialization the agent paramters, the local and the global planner.

            :param walker: actor to apply to agent logic onto
            :param desired_speed: speed (in m/s) at which the vehicle will move range is (0.7-5.7) Pedestrian acceleration and speeds, 2012
            :param opt_dict: dictionary in case some of its parameters want to be changed.
                This also applies to parameters related to the LocalPlanner.
        """

        self.name = f"PedestrianAgent #{walker.id}"
        super().__init__(self.name, walker, desired_speed=desired_speed, config=config)
        self._world = self._walker.get_world()
        self._map = self._world.get_map()

        self.skip_ticks = 0
        self.time_delta = time_delta
        self.tickCounter = 0

        self.visualizer = visualizer


        self._last_jumped = time.time_ns()

        self.collisionSensor = None
        self.obstacleDetector = None

        self._localPlanner = None

        # config parameters

    

    def canClimbSideWalk(self):

        if self.done():
            return False
        if self.timeSinceLastJumpMS() < 1000:
            return False

        distance = self.distanceToNextSideWalk() 
        if distance is None:
            return False
        self.logger.debug(f"current distance is {distance}")
        distance -= self.getOldSpeed() * self.time_delta
        
        self.logger.debug(f"future distance is {distance}")
        walkerSpeed = self.getOldSpeed()

        # if distance < walkerSpeed * 2 and distance > walkerSpeed:
        if distance < 0.2 and distance > 0.1:
            self.logger.debug(f"future distance is {distance}. Can jump")
            return True
        return False

    def updateJumped(self):
        self._last_jumped = time.time_ns()

    def timeSinceLastJumpMS(self):
        diff = (time.time_ns() - self._last_jumped) // 1_000_000 
        return diff


    def done(self):
        if self.getDistanceToDestination() < 0.1:
            return True
        return False

    def canUpdate(self):
        if self.skip_ticks == 0:
            return True
        self.tickCounter += 1
        if self.tickCounter >= self.skip_ticks:
            self.tickCounter = 0
            return True
        return False
    
    # def updateControl(self):
    #     "we should not call this. apply batch control"
    #     self._walker.apply_control(self.calculateControl())


    def printLocations(self):
        print("Agent location", self._walker.get_location())
        print("Collision location", self.collisionSensor.get_location())
        print("Obstacle detector location", self.obstacleDetector.get_location())

    def calculateControl(self):
        if self._destination is None:
            raise Error("Destination is none")

        # self.printLocations()
        # self.distanceToNextSideWalk()

        location = self.feetLocation
        self.logger.debug(f"Calculating control for Walker {self._walker.id}")
        direction = self.directionToDestination()
        self.visualizer.drawDirection(location, direction, life_time=0.1)
        speed = self.calculateNextSpeed(direction)

        self.logger.info(f"Walker {self._walker.id}: distance to destination is {self.getDistanceToDestination()} meters, and next speed {speed}")
        self.logger.info(f"next speed {speed}")
        self.logger.info(f"direction {direction}")


        self.climbSidewalkIfNeeded()

        control = carla.WalkerControl(
            direction = direction,
            speed = speed,
            jump = False
        )

        self._needJump = False

        return control


    def calculateNextSpeed(self, direction):

        # TODO make a smooth transition
        # oldControl = self._walker.get_control()
        # currentSpeed = oldControl.speed
        # nextSpeed = max()
        return self.desired_speed

    def climbSidewalkIfNeeded(self):

        location = self.feetLocation

        if self.canClimbSideWalk():
            self.updateJumped()
            self.logger.info(f"{self.name} climbing up a sidewalk.")
            # self._walker.add_force(carla.Vector3D(0, 0, 10))
            # velocity = self.getOldVelocity() # sometimes old velocity is too low due to collision with the sidewalk..
            
            velocity = self.speedToVelocity(self.desired_speed)

            self._walker.set_location(
                carla.Location(
                    location.x + velocity.x * self.time_delta * 5,
                    location.y + velocity.y * self.time_delta * 5,
                    location.z + 0.5
            ))

    #region sidewalk


    def getObstaclesToDistance(self):
        actorLocation = self._walker.get_location()
        actorXYLocation = carla.Location(x = actorLocation.x, y = actorLocation.y, z=0.05)
        destinationXYLocation = carla.Location(x = self._destination.x, y = self._destination.y, z=0.05)
        labeledObjects = self._world.cast_ray(actorXYLocation, destinationXYLocation)
        # for lb in labeledObjects:
        #     print(f"Labeled point location {lb.location} and semantic {lb.label} distance {actorLocation.distance(lb.location)}")
        return labeledObjects
    
    def distanceToNextSideWalk(self):
        actorLocation = self._walker.get_location()
        actorXYLocation = carla.Location(x = actorLocation.x, y = actorLocation.y, z=0.)
        labeledObjects = self.getObstaclesToDistance()
        for lb in labeledObjects:
            if lb.label == carla.CityObjectLabel.Sidewalks:
                if self.visualizer is not None:
                    self.visualizer.drawPoint(carla.Location(lb.location.x, lb.location.y, 1.0), color=(0, 0, 255), life_time=1.0)
                sidewalkXYLocation = carla.Location(x = lb.location.x, y = lb.location.y, z=0.)
                distance = actorXYLocation.distance(sidewalkXYLocation)
                print(f"Sidewalk location {lb.location} and semantic {lb.label} XY distance {distance}")
                return distance
        return None

    #endregion
    #region sensor handlers

    def handleWalkerCollision(self, data):
        if self.isSidewalk(data.other_actor):
            self.logger.info(f"{self.name} hits a sidewalk")
        else:
            self.logger.info(f"{self.name} hits a non-sidewalk")


    def handWalkerObstacles(self, data):
        # self.logger.info(f"{self.name} sees a obstackle {data.distance}m away with semantic tag {data.other_actor.semantic_tags}")
        # self.logger.info("semantic tag", data.other_actor.semantic_tags)
        # if self.isSidewalk(data.other_actor):

        #     if data.distance < 0.1:
        #         self.logger.info(f"{self.name} is on a sidewalk {data.distance}m away")
        #     else:
        #         self.logger.info(f"{self.name} sees a obstackle {data.distance}m away")

        #     # self._needJump = True
        return
    
    def isSidewalk(self, actor):
        if 8 in actor.semantic_tags:
            return True
        return False

    #endregion
    # region planning

    def setLocalPlanner(self, planner):
        self._localPlanner = planner

    
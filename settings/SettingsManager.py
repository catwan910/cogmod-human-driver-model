import carla
import logging

from matplotlib import transforms
from lib.ClientUser import ClientUser
from .SourceDestinationPair import SourceDestinationPair
from typing import List

class SettingsManager(ClientUser):

    def __init__(self, client, settingsDict) -> None:
        super().__init__(client)
        self.name = "SettingsManager"

        self.settingsDict = settingsDict
        self.currentSetting = None
        self._walkerSettings:List[SourceDestinationPair] = None
        self._walkerTransforms = None

        self._vehicleSettings: List[SourceDestinationPair] = None
        self._vehicleTransforms = None

        pass


    def load(self, settingsId):
        self.currentSetting = self.settingsDict[settingsId]

        self._walkerSettings = None
        self._walkerTransforms = None

        self._vehicleSettings = None
        self._vehicleTransforms = None

    def _assertCurrentSetting(self):
        if self.currentSetting is None:
            msg = f"{self.name}:currentSetting is None"
            self.error(msg)
    
    
    
    def _pointToLocation(self, point, z=1):
        
        location = carla.Location(
            x = point[0],
            y = point[1],
            z = z
        )

        return location

    
    def locationToVehicleSpawnPoint(self, location: carla.Location) -> carla.Transform:

        # find a way point
        waypoint = self.map.get_waypoint(location, project_to_road=True, lane_type=carla.LaneType.Driving)
        if waypoint is None:
            msg = f"{self.name}: Cannot create way point near {location}"
            self.error(msg)
        transform = carla.Transform(location = waypoint.transform.location + carla.Location(z=1), rotation = waypoint.transform.rotation)
        # print(waypoint.transform)
        # print(transform)
        # exit(1)
        return transform


    # def getEgoSpawnpoint(self) -> carla.Transform:
    #     self._assertCurrentSetting()
        
    #     point = self.currentSetting["ego_setting"]
    #     location = self._pointToLocation(point)
    #     return self.locationToVehicleSpawnPoint(location)

    
    def getVehicleSettings(self):
        self._assertCurrentSetting()

        if self._vehicleSettings is None:
            self._vehicleSettings = []
            for setting in self.currentSetting["ego_settings"]:
                sourcePoint = (setting[0], setting[1])
                destinationPoint = (setting[2], setting[3])

                self._vehicleSettings.append(
                    SourceDestinationPair(
                        source=self._pointToLocation(sourcePoint),
                        destination=self._pointToLocation(destinationPoint, z=0.1)
                    )
                )

        return self._vehicleSettings
    
    def getWalkerSettings(self):
        self._assertCurrentSetting()

        if self._walkerSettings is None:
            self._walkerSettings = []
            for setting in self.currentSetting["walker_settings"]:
                sourcePoint = (setting[0], setting[1])
                destinationPoint = (setting[2], setting[3])

                self._walkerSettings.append(
                    SourceDestinationPair(
                        source=self._pointToLocation(sourcePoint),
                        destination=self._pointToLocation(destinationPoint, z=0.1)
                    )
                )

        return self._walkerSettings
    
    def getWalkerSpawnPoints(self):

        if self._walkerTransforms is None:
            walkerSettings = self.getWalkerSettings()
            self._walkerTransforms = []

            for walkerSetting in walkerSettings:
                sourceTransform = carla.Transform(
                    location = walkerSetting.source
                )
                destination = walkerSetting.destination

                self._walkerTransforms.append((sourceTransform, destination))

        return self._walkerTransforms
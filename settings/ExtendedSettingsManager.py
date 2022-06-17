
from SettingsManager import SettingsManager


class CogModSettingsManager(SettingsManager):
    def __init__(self, client, settingsDict):

        super().__init__(client, settingsDict)





    def getNumberOfVehicleWithSpawnPointAndDestination(self):
        numberOfVehicles = self.currentSetting["number_of_vehicles"]
        spawnPoints = self.currentSetting["spawn_points"]
        destinationPoints = self.currentSetting["destination_points"]

        spawnPoints_transforms = []
        destinationPoints_transforms = []

        for sp in spawnPoints:
            point_to_location = self._pointToLocation(sp)
            location_to_transform = self.locationToVehicleSpawnPoint(point_to_location)
            spawnPoints_transforms.append(location_to_transform)
        for dp in destinationPoints:
            point_to_location = self._pointToLocation(dp)
            location_to_transform = self.locationToVehicleSpawnPoint(point_to_location)
            destinationPoints_transforms.append(location_to_transform)

        return (numberOfVehicles, spawnPoints_transforms, destinationPoints_transforms)

    def getNumberOfCogmodAgentsWithParameters(self):
        cogmod_agent_settings = self.currentSetting["cogmod_agents"]
        numberOfAgents = cogmod_agent_settings["number_of_cogmod_agents"]

        agent_parameter_list = []
        for i in range(1, numberOfAgents+1):
            current_setting = cogmod_agent_settings[str(i)]

            spawn_coordinate = current_setting["spawn_point"]
            destination_coordinate = current_setting["destination_point"]

            spawn_location = self._pointToLocation(spawn_coordinate)
            destination_location = self._pointToLocation(destination_coordinate)

            spawn_transform = self.locationToVehicleSpawnPoint(spawn_location)
            destination_transform = self.locationToVehicleSpawnPoint(destination_location)

            current_setting['spawn_point'] = spawn_transform
            current_setting['destination_point'] = destination_transform

            agent_parameter_list.append(current_setting)

        # print(agent_parameter_list)
        return (numberOfAgents, agent_parameter_list)

    def getNumberOfActorAgentsWithTrajectories(self):
        actor_agent_settings = self.currentSetting["actor_agents"]
        numberOfAgents = actor_agent_settings["number_of_actor_agents"]

        actor_trajectory_list = []
        for i in range (1, numberOfAgents+1):
            current_setting = actor_agent_settings[str(i)]
            trajectory = current_setting["trajectory"]
            trajectory_transforms = []
            for coordinate, time in trajectory:
                # print(coordinate, time)
                point_to_location = self._pointToLocation(coordinate)
                location_to_transform = self.locationToVehicleSpawnPoint(point_to_location)
                trajectory_transforms.append((location_to_transform, time))
            actor_trajectory_list.append(trajectory_transforms)
            pass

        return (numberOfAgents, actor_trajectory_list)



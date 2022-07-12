
from .SettingsManager import SettingsManager


class CogModSettingsManager(SettingsManager):
    def __init__(self, client, settingsDict):

        super().__init__(client, settingsDict)

    def getStraightRoadSimulationSettings(self):

        cogmod_agent_settings = self.getCogmodAgentSetting()
        actor_agent_settings = self.getActorAgentSetting()
        trigger_distance = self.currentSetting["trigger_distance"]
        return (cogmod_agent_settings, actor_agent_settings, trigger_distance)


    def getActorAgentSetting(self):
        # actor agent settings
        actor_agent_settings = self.currentSetting["actor_agent"]

        actor_spawn_coordinate = actor_agent_settings["spawn_point"]
        actor_destination_coordinate = actor_agent_settings["destination_point"]

        actor_spawn_transform = self.convertCoordinateToTransform(actor_spawn_coordinate)
        actor_destination_transform = self.convertCoordinateToTransform(actor_destination_coordinate)

        actor_agent_settings = {
            "spawn_transform": actor_spawn_transform,
            "destination_transform": actor_destination_transform,
            "driver_profile": actor_agent_settings["driver_profile"],
            "target_speed": actor_agent_settings["target_speed"]
        }
        return actor_agent_settings


    def getCogmodAgentSetting(self):
        # cogmod agent settings
        cogmod_agent_settings = self.currentSetting["cogmod_agent"]
    
        cogmod_spawn_coordinate= cogmod_agent_settings["spawn_point"]
        cogmod_destination_coordinate = cogmod_agent_settings["destination_point"] 

        cogmod_spawn_transform = self.convertCoordinateToTransform(cogmod_spawn_coordinate)
        cogmod_destination_transform = self.convertCoordinateToTransform(cogmod_destination_coordinate)

        cogmod_agent_settings = {
            "spawn_transform": cogmod_spawn_transform,
            "destination_transform": cogmod_destination_transform,
            "driver_profile": cogmod_agent_settings["driver_profile"]
        }
        
        return cogmod_agent_settings

    def getVisualModuleSettings(self):
        cogmod_agent_settings = self.getCogmodAgentSetting()
        static_element_settings = self.getStaticElementSettings()
        return cogmod_agent_settings, static_element_settings


    def getStaticElementSettings(self):
        static_element_settings = self.currentSetting["static_element"]
        spawn_points = static_element_settings["spawn_points"]
        types = static_element_settings["types"]
        static_element_settings = []
        for i in range(len(spawn_points)):
            spawn_transform = self.convertCoordinateToTransform(spawn_points[i])
            static_element_settings.append((spawn_transform, types[i]))

        return static_element_settings
        

    




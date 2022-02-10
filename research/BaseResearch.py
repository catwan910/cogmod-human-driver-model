import carla
import os
from lib import ClientUser, LoggerFactory, MapManager, MapNames, SimulationVisualization

class BaseResearch(ClientUser):
    def __init__(self, name, client: carla.Client, mapName, logLevel, outputDir:str = "logs") -> None:
        super().__init__(client)
        logPath = os.path.join(outputDir, f"{name}.log")
        self.logger = LoggerFactory.getBaseLogger(name, defaultLevel=logLevel, file=logPath)

        self.mapManager = MapManager(client)
        self.mapManager.load(mapName)

        self.visualizer = SimulationVisualization(self.client, self.mapManager)

        self.initWorldSettings()
        # self.initVisualizer()

        pass


    def initWorldSettings(self):
        time_delta = 0.007
        settings = self.world.get_settings()
        settings.substepping = False
        settings.fixed_delta_seconds = time_delta
        self.world.apply_settings(settings)
        pass

    
    def initVisualizer(self):
        self.visualizer.drawSpawnPoints()
        self.visualizer.drawSpectatorPoint()
        self.visualizer.drawAllWaypoints(life_time=1.0)
        pass

    
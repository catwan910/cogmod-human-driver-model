import logging
import math
import time
from unittest import result
import carla

from lib.MapManager import MapNames

from .BaseResearch import BaseResearch
# from settings.t_junction_settings import t_junction_settings
from settings.straight_road_settings import straight_road_settings
from settings.ExtendedSettingsManager import CogModSettingsManager
from agents.pedestrians import PedestrianFactory
from agents.vehicles import VehicleFactory
from lib import Simulator, SimulationMode
from lib import Utils

class ResearchCogMod(BaseResearch):

    def __init__(self, 
                 client: carla.Client, 
                 logLevel: logging, 
                 mapName: MapNames, 
                 outputDir:str, 
                 simulationMode: SimulationMode,
                 act_id: str):

        self.name = "Research CogMod"
        super().__init__(name=self.name, 
                         client=client, 
                         mapName=mapName, 
                         logLevel=logLevel, 
                         outputDir=outputDir,
                         simulationMode=simulationMode)


        self.act_id = act_id
        self.simulator = None # populated when run

        self.settingsManager = CogModSettingsManager(self.client, straight_road_settings)
        self.vehicleFactory = VehicleFactory(self.client, visualizer=self.visualizer)

        self.cogmod_agent_setting = {}
        self.actor_agent_setting = {}

        self.cogmod_agent = None
        self.actor_agent = None

        self.global_agent_list = []
        
        self.setup()


    def setup(self):
        self.settingsManager.load(self.act_id)
        self.cogmod_agent_setting, self.actor_agent_setting, self.trigger_distance = self.settingsManager.getStraightRoadSimulationSettings()

        # self.logger.info(f"CogMod agent settings: {self.cogmod_agent_setting}")
        # self.logger.info(f"Actor agent settings: {self.actor_agent_setting}")

        self.logger.info(f"Trigger distance: {self.trigger_distance}")
        # self.visualizer.drawSpawnPoints()


        pass

    def destoryActors(self):
        if self.cogmod_agent is not None:
            self.logger.warn(f'destroying cogmod agent ')
            self.cogmod_agent.get_vehicle().destroy()
            self.cogmod_agent = None
        if self.actor_agent is not None:
            self.logger.warn(f'destroying actor agent ')
            self.actor_agent.get_vehicle().destroy()
            self.actor_agent = None
        pass

    def onEnd(self):
        self.logger.info("destroying all agents")
        self.destoryActors()
        self.global_agent_list = []
        pass
    
    def onTick(self, world_snapshot):
        self.updateVehiclesAsynchoronousMode()
        pass
 

    def updateVehiclesAsynchoronousMode(self):

        if self.cogmod_agent is None or self.actor_agent is None:
            self.logger.error("one or both the agent is None, ending simulation")
            return
        if self.cogmod_agent.is_done() or self.actor_agent.done():
            self.logger.info("one or both the agent is done destory actors")
            return
        
        cogmod_control = self.cogmod_agent.update_agent(self.global_agent_list)
        if cogmod_control is not None:
            self.cogmod_agent.vehicle.apply_control(cogmod_control)


        actor_location = self.actor_agent.get_vehicle().get_location()
        cogmod_location = self.cogmod_agent.get_vehicle().get_location()

        distance = actor_location.distance(cogmod_location)

        actor_control = carla.VehicleControl()
        if distance < self.trigger_distance:
            actor_control = self.actor_agent.add_emergency_stop(actor_control)
        
        actor_control = self.actor_agent.run_step()
        if actor_control is not None:
            self.actor_agent._vehicle.apply_control(actor_control)

        pass


    def createCogmodAgentsAsynchronousMode(self):
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
        self.global_agent_list.append(self.cogmod_agent)
        pass

    def createActorAgentsAsynchronousMode(self):
        spawn_transform = self.actor_agent_setting["spawn_transform"]
        destination_transform = self.actor_agent_setting["destination_transform"]
        driver_profile = self.actor_agent_setting["driver_profile"]
        target_speed = self.actor_agent_setting["target_speed"]

        vehicle = self.vehicleFactory.spawn(spawn_transform)
        if vehicle is None:
            self.logger.error("Could not spawn actor vehicle")
            exit("cannot spawn actor vehicle")
        else:
            self.logger.info(f"successfully spawned actor vehicle {vehicle.id}")
            # self.logger.info(vehicle.get_control())

        # need to create a behavior agent
        self.actor_agent = self.vehicleFactory.createAgent(vehicle=vehicle,
                                                           target_speed=target_speed)
        self.actor_agent.set_destination(destination_transform.location)
        self.global_agent_list.append(self.actor_agent)
        pass


    def run(self, maxTicks=5000):
        self.logger.info(f'start simulation maxTicks {maxTicks}')

        if self.simulationMode == SimulationMode.ASYNCHRONOUS:
            self.createCogmodAgentsAsynchronousMode()
            self.createActorAgentsAsynchronousMode()
            self.world.wait_for_tick()
        if self.simulationMode == SimulationMode.SYNCHRONOUS:
            self.logger.warn("synchronous mode is not implemented yet")
            pass
        
        time.sleep(2.0)

        onTickers = [self.onTick]
        onEnders = [self.onEnd]

        self.simulator = Simulator(self.client, onTickers=onTickers, onEnders=onEnders, simulationMode=self.simulationMode)
        self.simulator.run(maxTicks)
        pass

   
    

# region bin


    # def createActorAgentsSynchronousMode(self):
    #     batch = []
    #     for i in range(self.number_of_actor_agents):
    #         trajectory = self.actor_trajectory_list[i]
    #         spawn_point = trajectory[0][0]
    #         spawn_command = self.vehicleFactory.spawn_command(spawnPoint=spawn_point)
    #         batch.append(spawn_command)
    #         pass

    #     results = self.client.apply_batch_sync(batch, True)

    #     for i in range(len(results)):
    #         result = results[i]
    #         if not result.error:
    #             vehicle_actor = self.world.get_actor(result.actor_id)
    #             actor_agent = self.vehicleFactory.createActorAgent(id=len(self.vehicle_list),
    #                                                                vehicle=vehicle_actor,
    #                                                                trajectory=self.actor_trajectory_list[i])
    #             self.vehicle_list.append(vehicle_actor)
    #             self.actor_agent_list.append(actor_agent)
    #             pass
    #         else:
    #             exit(f"failed to spawn vehicle {i}")
    #         pass
    #     pass

    # # In the synchronous mode, the spawn command are applied in batch
    # def createCogmodAgentSynchronousMode(self):       
    #     batch = []
    #     for i in range(self.number_of_cogmod_agents):
    #         spawn_point = self.cogmod_agent_parameter_list[i]['spawn_point']
            
    #         # creating the vehicle spawning command 
    #         spawn_command = self.vehicleFactory.spawn_command(spawn_point)
    #         batch.append(spawn_command)
    #         pass

    #     # applying all command togather 
    #     results = self.client.apply_batch_sync(batch, True)
    #     # print(f'results : {results}')

    #     for i in range(len(results)):
    #         if not results[i].error:
    #             print(f"successfully spawn vehicle {results[i].actor_id}")
    #             vehicle_actor = self.world.get_actor(results[i].actor_id)
    #             destination_point = self.cogmod_agent_parameter_list[i]['destination_point']
    #             driver_profile = self.cogmod_agent_parameter_list[i]['driver_profile']
    #             vehicleAgent = self.vehicleFactory.createCogModAgent(id=vehicle_actor.id,
    #                                                                  vehicle=vehicle_actor,
    #                                                                  destinationPoint=destination_point,
    #                                                                  driver_profile=driver_profile) 
                
    #             self.vehicle_list.append(vehicle_actor)                      
    #             self.cogmod_agent_list.append(vehicleAgent)
    #         else:
    #             exit(f"failed to spawn vehicle {i}")
    #             return
    #     pass
            
    # def updateVehiclesSynchoronousMode(self, world_snapshot):
    #     batch = []
    #     if len(self.vehicle_list) == 0:
    #         self.logger.warn(f"No vehicle to update")
    #         exit()
    #         return

    #     agent_to_remove = []
    #     for agent in self.cogmod_agent_list:
    #         if agent.is_done():
    #             agent_to_remove.append(agent)
    #         else:
    #             control = agent.update_agent(self.cogmod_agent_list)
    #             if control is not None:
    #                 batch.append(carla.command.ApplyVehicleControl(agent.vehicle.id, control))

    #     split_index = len(batch)

    #     for agent in agent_to_remove:
    #         destroy_command = carla.command.DestroyActor(agent.vehicle.id)
    #         batch.append(destroy_command)
            
    #     results = self.client.apply_batch_sync(batch, True)
    #     for i in range(split_index, len(results)):
    #         print('destroy agent ')
    #         self.destroyAgent(self.cogmod_agent_list[i])
    #         pass
    #     pass


    # def updateVehiclesAsynchoronousMode(self, world_snapshot):
    #     if len(self.vehicle_list) == 0:
    #         self.logger.warn(f"No vehicle to update")
    #         exit()
    #         return

    #     agent_to_remove = []
    #     for agent in self.cogmod_agent_list:
    #         if agent.is_done():
    #             agent_to_remove.append(agent)
    #         else:
    #             control = agent.update_agent(self.cogmod_agent_list)
    #             if control is not None:
    #                 agent.vehicle.apply_control(control)

    #     for agent in agent_to_remove:
    #         self.destroyAgent(agent)
            
  
    #     pass



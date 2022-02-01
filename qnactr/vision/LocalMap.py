

from turtle import distance
from agents.navigation.global_route_planner import GlobalRoutePlanner


class LocalMap():
    def __init__(self, world, vehicle, tracking_radius=100.0):
        
        if world is None:
            raise ValueError('need to have map')
            return

        self._world = world
        self._map = self._world.get_map()
        self._vehicle = vehicle
        self._tracking_radius = tracking_radius

        self._global_plan = None
        self._GP_sampling_resolution = 2.0
        self._global_planner = GlobalRoutePlanner(self._map, 
                                                  self._GP_sampling_resolution)

        self._tracked_vehicles = []
        self._tracked_traffic_signs = []

        print(f'LocalMap is created with map: {world}')
        pass

    def set_global_plan(self, start_transform, end_transform):
        if not start_transform or not end_transform:
            raise ValueError('need to have start and end for global plan')
            return None
        print(f'start transform: {start_transform}, \nend transform: {end_transform}')
        self._global_plan = self._global_planner.trace_route(start_transform.location, end_transform.location)
        pass

    def get_global_plan(self):
        if self._global_plan is None:
            raise ValueError('need to have global plan')
            return None
        return self._global_plan

    def update_local_map(self):
        
        # update tracked vehicles
        all_vehicle_from_world = self._world.get_actors().filter('vehicle.*')
        self._tracked_vehicles = []
        for vehicle in all_vehicle_from_world:
            distance = self._vehicle.get_location().distance(vehicle.get_location())
            if vehicle.id == self._vehicle.id or distance > self._tracking_radius:
                continue
            else:
                self._tracked_vehicles.append(vehicle)
        # update tracked traffic signs
        if len(self._tracked_traffic_signs) == 0:
            all_traffic_signs_from_world = self._world.get_actors().filter("*traffic_light*")
            self._tracked_traffic_signs = all_traffic_signs_from_world

        current_map_dict = {'route': self._global_plan,
                            'tracked_vehicles': self._tracked_vehicles,
                            'tracked_traffic_signs': self._tracked_traffic_signs}

        return current_map_dict
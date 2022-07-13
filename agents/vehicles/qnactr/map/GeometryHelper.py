import carla
import math
from numpy import angle
from shapely.geometry import LineString

class GeometryHelper():

    @staticmethod
    def create_linestring_from_global_plan(global_plan):
        coordinate_2D = []
        for wp, _ in global_plan:
            location = wp.transform.location
            coordinate_2D.append((location.x, location.y))
            pass
        return LineString(coordinate_2D)
        pass

    @staticmethod
    def is_intersecting(global_plan1, global_plan2):
        line_string1 = GeometryHelper.create_linestring_from_global_plan(global_plan1)
        line_string2 = GeometryHelper.create_linestring_from_global_plan(global_plan2)
        return GeometryHelper.find_intersection_between_two_linestrings(line_string1, line_string2)


    @staticmethod
    def find_intersection_between_two_linestrings(line1, line2):
        intersection = line1.intersection(line2)
        return intersection 

    def create_polyline_from_global_plan(global_plan):
        for i in global_plan:
            print(i)
        pass

    @staticmethod
    def find_gaze_triangle(vehicle, gaze_settings, height = 1):
        gaze_direction, view_angle, length, _ = gaze_settings
        view_angle = math.radians(view_angle)   # convert to radians
        # print(gaze_direction, view_angle, length, color)   

        vehicle_transform = vehicle.get_transform()
        vehicle_center = vehicle_transform.location
        vehicle_forward = vehicle_transform.get_forward_vector()

        cos = math.cos(gaze_direction)
        sin = math.sin(gaze_direction)
        newX = vehicle_forward.x * cos - vehicle_forward.y * sin
        newY = vehicle_forward.x * sin + vehicle_forward.y * cos

        direction_vector = carla.Vector3D(newX*length, newY*length, height)

        normalized_direction_vector = direction_vector.make_unit_vector()

        left_point = GeometryHelper.find_corner_point_of_triangle(height, view_angle, length, normalized_direction_vector)
        right_point = GeometryHelper.find_corner_point_of_triangle(height, -view_angle, length, normalized_direction_vector)


        left_point = vehicle_center + left_point
        right_point = vehicle_center + right_point
        end_point = vehicle_center + direction_vector

        return [right_point, left_point, vehicle_center]
        







        pass

    @staticmethod
    def find_corner_point_of_triangle(height, view_angle, length, normalized_direction_vector):
        cos_left = math.cos(view_angle/2)
        sin_left = math.sin(view_angle/2)
        left_point_x =  normalized_direction_vector.x * cos_left - normalized_direction_vector.y * sin_left
        left_point_y =  normalized_direction_vector.x * sin_left + normalized_direction_vector.y * cos_left
        left_point = carla.Vector3D(left_point_x*length, left_point_y*length, height)
        return left_point
    

    
# if __name__ == '__main__':

#     points_a = [(1,1),(1,0), (1,-1)]
#     points_b = [(-3, -3), (0,0), (2,2), (-2,-2)]
#     GeometryHelper.find_intersection_between_two_polyline(points_a, points_b)

    
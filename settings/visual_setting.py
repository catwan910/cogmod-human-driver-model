

from .driver_profile import driver_profile


# In this scenario
# the driver drives in a straight road with 10 m/s speed 
# the driver changes the gaze direction randomly and perceive the 
# environemnt

# | (132, -4)   |            ||           |           || 
# |             | (123,0)    ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           || 
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           || 
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           |           ||
# |             |            ||           | (-5,16)   || 
# |             |            ||           |           ||
# |             |            || (-54, 8)  |           ||
# |             |            ||           |           ||
# |             |            ||           |           ||


visual_settings = {
    "setting1": {
        "cogmod_agent": {
            "spawn_point": (30, 13), #(-55, 8),
            "destination_point": (-60, 12), #(150, 8),
            "driver_profile": driver_profile["driver3"],
            # speed 30
        },
        'static_element': {
            "spawn_points": [(5, 16), (-5, 16), (-19, 16)],
            "types": ('advertisement', 'advertisement', 'advertisement'),
        },
    }
}


import numpy as np
import json
from scipy.spatial import distance_matrix
from  dataclasses import dataclass
from typing import *


@dataclass
class Planet:
    name: str = "planet"
    position : np.ndarray = np.array((0,0))
    velocity : np.ndarray = np.array((1,1))
    mass : float = 50
    size : float = 10
    color : tuple[float] =(1,1,0,0)


#help  dump to JSON Planet class
class PlanetJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if type(o) is Planet:
                result = {"name":o.name, "position": o.position.tolist(),
                          "velocity": o.velocity.tolist(), "mass": float(o.mass),
                          "size":float(o.size), "color": o.color }
                return result
            return super().default(o)


class PlanetSystem:
    planet_list = []

    # -----------------------------------------------------------
    def __init__(self, draw_callback=None):
        self.draw_callback = draw_callback

    # -----------------------------------------------------------
    def add_planet(self, planet):
        self.planet_list.append(planet)

    # -----------------------------------------------------------
    def calc_new_positions(self):
        #calc new position of planets in planet list

        positions = [obj.position for obj in self.planet_list]
        dist_matrix = distance_matrix(positions , positions )

         # for every 2 objects in planet_list
        for i in range(0, len(self.planet_list) - 1):
             for j in range(i + 1, len(self.planet_list)):
                 obj_1 = self.planet_list[i]
                 obj_2 = self.planet_list[j]

                 r = dist_matrix[i, j]
                 r2 = r * r

                 vec = obj_1.position - obj_2.position

                 # vec2 - direction normal vector from obj_2 to obj_1
                 vec2 = vec / r
                 vec1 = -vec2

                 a1 = obj_2.mass / r2
                 a2 = obj_1.mass / r2

                 v1 = a1 * vec1
                 v2 = a2 * vec2

                 obj_1.velocity = obj_1.velocity + v1
                 obj_2.velocity = obj_2.velocity + v2


        for obj in self.planet_list:
            obj.position = obj.position + obj.velocity
    #-----------------------------------------------------------
    def draw(self):
        if self.draw_callback is None:
            return

        for obj in self.planet_list:
            self.draw_callback(obj)

    def save_to_json(self, filename='planets.json'):
        with open(filename, "w") as write_file:
            json.dump(self.planet_list, write_file, cls = PlanetJSONEncoder)


    def load_json(self, filename='planets.json'):
        def dict_to_planet(jsn_dict):
            #obj  = Planet(**jsn_dict)
            jsn_dict['position']=np.array(jsn_dict['position'])
            jsn_dict['velocity'] = np.array(jsn_dict['velocity'])
            return Planet(**jsn_dict)

        with open(filename, "r") as read_file:
            result = json.load(read_file, object_hook=dict_to_planet)
            #print(result)
            self.planet_list = result


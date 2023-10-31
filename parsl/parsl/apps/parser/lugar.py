# -*- coding: utf-8 -*-

import make_serialization

class Lugar:

     #constructor
     def __init__(self, lat, lon, country, state,city,center,position):
        self.lat = lat
        self.lon = lon
        self.country = country
        self.state = state
        self.city = city
        self.center = center
        self.position = position

     def to_json(self):  # New special method.
        return self.__dict__

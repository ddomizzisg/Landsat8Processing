
import urllib.request, json, sys,time,re
from lugar import Lugar
import os
import logging

class File(object):

    def __init__(self,db):
        self.clave = os.environ["GOOGLE_KEY"]
        self.db = db
        self.places = db.places

    #lee las lineas de un archivo
    def openFile(self,path):
        return open(path).readlines()

    #limpia las cadenas dejando solo numeros
    def cleanString(self,strNum):
        return re.sub("[^,.\-WNSE 0-9]", " ", strNum).strip()

    def insertNewPlace(self, latlon, filename, center, position):
        data = self.getPlaces(latlon['lat'],latlon['lon'])
        l = Lugar(latlon['lat'],latlon['lon'],data['country'],data['state'],data['city'],center,position)
        #self.db.insertFilePlaces(d,latlon['lat'],latlon['lon'])
        return l

    #obtiene el lugar que se encuentra en dos coordenadas dadas
    def getPlaces(self,lat,lon):
        #res = self.db.getPlace(lat,lon)
        res = self.places.find_one({'latitude': lat, 'longitude': lon})
        if res is None or (res['state'] is None and res['country'] is None and res['city'] is None):
            #print "From Google"
            url = "https://maps.googleapis.com/maps/api/geocode/json?key="+self.clave+"&latlng="+lat+","+lon+"&sensor=true&language=en"
            print(url)
            try:
                data = json.loads(urllib.request.urlopen(url).read())
            except:
                time.sleep(2)
                data = json.loads(urllib.request.urlopen(url).read())

            country = list(filter(lambda x: "country" in x["types"], data["results"]))
            print(country)
            country = country[0]["address_components"][0]["long_name"] if len(country) > 0 else None
            state = list(filter(lambda x: "administrative_area_level_1" in x["types"], data["results"]))
            state = state[0]["address_components"][0]["long_name"] if len(state) > 0 else None
            city = list(filter(lambda x: "postal_code" in x["types"], data["results"]))
            city = city[0]["address_components"][1]["long_name"] if len(city) > 0 else None

            if city is None:
                city = list(filter(lambda x: "administrative_area_level_2" in x["types"], data["results"]))
                city = city[0]["address_components"][0]["long_name"] if len(city) > 0 else None
            place = {"state":state,"country":country,"city":city, "latitude":lat, "longitude":lon}
            
            if res is not None:
                res = self.places.update_one({'_id':res['_id']}, {"$set": place}, upsert=False)
            else:
                # place
                res = self.places.insert_one(place)
                #print 'One post: {0}'.format(res.inserted_id)
            return place
            
        return res

#!/usr/bin/env python

from osgeo import gdal, osr
import shapely.wkt
import shapely.geometry
from database import DataBase

class ConvertToWRS:

    def __init__(self):
        self.shapefile = '/app/wrs2_desc/wrs2_descending.shp'
        self.shapefile = ogr.Open(self.shapefile)
        self.layer = self.shapefile.GetLayer(0)
        self.polygons = []
        for i in range(self.layer.GetFeatureCount()):
            # Get the feature, and its path and row attributes
            feature = self.layer.GetFeature(i)
            path = feature['PATH']
            row = feature['ROW']

            # Get the geometry into a Shapely-compatible
            # format by converting to Well-known Text (Wkt)
            # and importing that into shapely
            geom = feature.GetGeometryRef()
            shape = shapely.wkt.loads(geom.ExportToWkt())

            # Store the shape and the path/row values
            # in a list so we can search it easily later
            self.polygons.append((shape, path, row))


    def checkPoint(self,feature, point, mode):
        geom = feature.GetGeometryRef() #Get geometry from feature
        shape = shapely.wkt.loads(geom.ExportToWkt()) #Import geometry into shapely to easily work with our point
        return point.within(shape) and feature['MODE']==mode;

    def getNearestSceneCenter(self,lat,lon):
         # Create a point with the given latitude
        # and longitude (NB: the arguments are lon, lat
        # not lat, lon)
        pt = shapely.geometry.Point(lon, lat)
        #res = []
        # Iterate through every polgon
        minDist = 100000
        res = None
        for poly in self.polygons:
            # If the point is within the polygon then
            # append the current path/row to the results
            # list
            if pt.within(poly[0]):
                dist = poly[0].distance(pt)
                if(dist < minDist): 
                    minDist = dist
                    res = {'path': poly[1], 'row': poly[2]}
                #res.append({'path': poly[1], 'row': poly[2]})

        # Return the results list to the user
        return res

#db = DataBase("aem_searcher","aem_seaarcher2", "K$df&bbsd98auja7f8ytycdd59")
#x = db.getPathRows(31.73842025,-83.56585325)
#print x
#con = ConvertToWRS()
#print con.getNearestSceneCenter(31.73842025,-83.56585325)
#print con.getNearestSceneCenter(81.923,5.424)
#print con.getNearestSceneCenter(10.12149025,-73.23126)

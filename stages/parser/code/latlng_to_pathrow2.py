import ogr
import shapely.wkt
import shapely.geometry


class ConvertToWRS:

    def __init__(self):
        self.shapefile = 'wrs2_asc_desc/wrs2_asc_desc.shp'
        self.wrs = ogr.Open(self.shapefile)
        self.layer = self.wrs.GetLayer(0)
        self.mode = 'A'


    def checkPoint(self,feature, point, mode):
        geom = feature.GetGeometryRef() #Get geometry from feature
        shape = shapely.wkt.loads(geom.ExportToWkt()) #Import geometry into shapely to easily work with our point
        return point.within(shape) and feature['MODE']==mode;

    def getNearestSceneCenter(self,lat,lon):
        i=0
        point = shapely.geometry.Point(lon,lat)
        while not self.checkPoint(self.layer.GetFeature(i), point, self.mode):
            i += 1
        feature = self.layer.GetFeature(i)
        path = feature['PATH']
        row = feature['ROW']
        return {'path':path, 'row':row}


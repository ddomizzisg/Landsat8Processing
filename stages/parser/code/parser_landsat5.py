from file import File
from latlng_to_pathrow import ConvertToWRS
import time
import logging

class ParserLansat5(File):

    def __init__(self, content, filename, db, usrToken, catalog):
        self.lines = content.split("\n")
        #self.lines = path
        self.usrToken = usrToken
        self.file_name = filename
        self.catalog = catalog
        super(ParserLansat5, self).__init__(db)

    def calculateCenter(self,lugares):
        sumLat,sumLon = 0,0
        for lug in lugares:
            sumLat += float(lug.lat)
            sumLon += float(lug.lon)

        return {'lat':str(sumLat/4.0),'lon':str(sumLon/4.0)} 

    def parse(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        lat,lon = None,None
        lugares = []
        date = ""
        projection = ""
        ellipsoid = ""

        for l in self.lines:
            #logger.info("xxxxxxxxxxxxxxx%s",l)
            l = l.strip()
            #print l
            if lat is not None and (l.startswith("CORNER_UL_LON_PRODUCT") or l.startswith("CORNER_UR_LON_PRODUCT") or l.startswith("CORNER_LL_LON_PRODUCT") or l.startswith("CORNER_LR_LON_PRODUCT")):
                lon = "%f" % float(l.split("=")[1])
                start_time = time.time()
                l = l.replace("CORNER_", "")
                lugares.append(self.insertNewPlace({'lat':lat,'lon':lon},self.file_name,False,l.split(":")[0][:2]))
                logger.info("Time to get place %s seconds",(time.time() - start_time))
                print(lat, lon)
                lat,lon = None,None
            elif l.startswith("CORNER_UL_LAT") or l.startswith("CORNER_UR_LAT") or l.startswith("CORNER_LL_LAT") or l.startswith("CORNER_LR_LAT"):
                lat = "%f" % float(l.split("=")[1])
                print(lat)
            elif l.startswith("DATE_ACQUIRED"):
                date = l.split("=")[1].strip()
            elif l.startswith("SCENE_CENTER_TIME"):
                date += " " + l.split("=",1)[1].strip()
            elif l.startswith("MAP_PROJECTION"):
                projection = l.split("=")[1].strip()
            elif l.startswith("ELLIPSOID"):
                ellipsoid = l.split("=")[1].strip()

        center = self.calculateCenter(lugares)
        start_time = time.time()
        lugares.append(self.insertNewPlace(center,self.file_name,True,"Center"))
        print("Time to get place --- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        pr = ConvertToWRS().getNearestSceneCenter(float(center['lat']),float(center['lon']))
        print("TIME TO GET PATH AND ROW")
        print("--- %s seconds ---" % (time.time() - start_time))

        #self.db.insertFile(self.file_name,"Landsat",pr['path'],pr['row'],date,projection,ellipsoid)
        #idImg = self.db.insertImage(self.file_name, 3, 4)
        logger.info("xxxxxxxxxxxxxxx%s",lugares)
        
        poligono = '\'('
        poligono += "(" + lugares[0].lon + "," + lugares[0].lat + "),";
        poligono += "(" + lugares[1].lon + "," + lugares[1].lat + "),";
        poligono += "(" + lugares[4].lon + "," + lugares[4].lat + "),";
        poligono += "(" + lugares[3].lon + "," + lugares[3].lat + ")";
        poligono += ')\''
        #idMet = self.db.insertMeta(pr['path'], pr['row'], date, projection, ellipsoid, poligono, idImg)
        
        #for p in lugares:
            #self.db.insertPlace(p.lat, p.lon, p.state, p.country, p.city, p.position, idMet)
        return {"Poligono":poligono,"usr_token":self.usrToken,"File_name":self.file_name,
                "Places":lugares,"Date":date,"Path":pr['path'],"Row":pr['row'],
                "Satelite":"Landsat","Projection":projection,"Ellipsoid":ellipsoid,"catalog":self.catalog}

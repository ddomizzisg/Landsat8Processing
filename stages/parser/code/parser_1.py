
from file import File
from latlng_to_pathrow import ConvertToWRS
import time
import logging
import datetime


class ParserUno(File):

    def __init__(self,content,filename,db, usrToken, catalog):
        #self.path = path
        self.lines = content.split("\n")
        self.usrToken = usrToken
        #self.lines = path
        self.file_name = filename
        self.catalog = catalog
        super(ParserUno, self).__init__(db)

    def getLatLong(self,line):
         #obtiene las posiciones entre las cuales se encuentran las coordenadas
        line = self.cleanString(line).split(",")
        lat = filter(None,line[0].split(" "))
        lon = filter(None,line[1].split(" "))

        #realiza la conversion de grados a decimal
        latD =  (float(lat[0]) + (float(lat[1])/60) + (float(lat[2])/3600))
        lonD = (float(lon[0]) + (float(lon[1])/60) + (float(lon[2])/3600))

        #verifica el signo, es W,S = negativo, N,E = positivo
        latD = -latD if str(lat[3]) is "W" else latD
        lonD = -lonD if str(lon[3]) is "S" else lonD

        return {'lat':str(round(lonD,6)),'lon':str(round(latD,6))}

    def parse(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        #logger.info("%s",self.lines)
        lugares = []
        ellipsoid = ""
        projection = "UTM"
        pr = ""
        logger.info("LINEES 5555 %s",self.lines[-6:])
        for line in self.lines[-6:]:
            if len(line) == 0:
                continue
            logger.info("LINEE %s",line)
            latlon = self.getLatLong(line)
            center = True if "Center" in line else False
            pos = "center"
            if "Upper Left"  in line:
                pos = "UL"
            elif "Upper Right"  in line:
                pos = "UR"
            elif "Lower Left"  in line:
                pos = "LL"
            elif "Lower Right"  in line:
                pos = "LR"

            if pos is "center":
                pr = ConvertToWRS().getNearestSceneCenter(float(latlon['lat']),float(latlon['lon']))
            start_time = time.time()
            lugares.append(self.insertNewPlace(latlon,self.file_name,center,pos))
            logger.info("Time to get place %s seconds",(time.time() - start_time))

        for line in self.lines:
            if "Ellipsoid" in line:
                ellipsoid = line.split(":")[1].strip()

        now = datetime.datetime.now()
        date = self.file_name[5:9]
        month = date[2:4]
        year = "20" + date[0:2]
        date = "01" + "-" + month + "-" + year
        date = str(now)
        #print date
        sat = 'Terra' if self.file_name.startswith("CMA") else 'Aqua'
        #self.db.insertFile(self.file_name,sat,pr['path'],pr['row'],"01/03/2017",projection,ellipsoid)
        #idImg = self.db.insertImage(self.file_name, sat, 4)
        poligono = '\'('
        poligono += "(" + lugares[0].lon + "," + lugares[0].lat + "),"
        poligono += "(" + lugares[1].lon + "," + lugares[1].lat + "),"
        poligono += "(" + lugares[4].lon + "," + lugares[4].lat + "),"
        poligono += "(" + lugares[3].lon + "," + lugares[3].lat + ")"
        poligono += ')\''
        #idMet = self.db.insertMeta(pr['path'], pr['row'], date, projection, ellipsoid, poligono, idImg)
        #for p in lugares:
            #self.db.insertPlace(p.lat, p.lon, p.state, p.country, p.city, p.position, idMet)
        
        return {"Poligono":poligono, "usr_token":self.usrToken,"File_name":self.file_name,"Places":lugares,
                "Satelite":sat,"Projection":projection,"Ellipsoid":ellipsoid,"Path":pr['path'],"Row":pr['row'],
                "Date":date,"catalog":self.catalog}

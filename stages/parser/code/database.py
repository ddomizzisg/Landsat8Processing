import psycopg2
import sys
import os.path
import time

class DataBase:

    def __init__(self,username,database,password, host):
        self.conn = psycopg2.connect("dbname="+database+" user="+username+" password="+password +" \
                    host="+host)

    def insertMeta(self, path, row, date, projection, ellipsoid, poligono, idelemento):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO metadatos (path, row, date, projection, ellipsoid, poligono, idelemento) \
        VALUES (%s,%s,%s,%s, %s,"+poligono+", %s)  RETURNING idmetadato", (path, row, date, projection, ellipsoid, idelemento))
        rows = cur.fetchall()
        cur.close()
        self.conn.commit()
        return rows[0][0]
        cur.close()

    def insertPlace(self,lat,lon,state,country,city,position,idmetadatos):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO points (lat,lon,state,country,city,position,idmetadatos) \
            VALUES (%s,%s,%s, %s,%s,%s,%s)", (lat,lon,state,country,city,position,idmetadatos))
            cur.close()
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Insert place " + str(e))

    def getPlace(self,lat,lon):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT lat,lon,country,state,city from points where country is not null \
                         and lat = %s and lon = %s",(lat,lon))
            rows = cur.fetchall()
            cur.close()
            if(len(rows) > 0):
                return {
                    "lat":rows[0][0],
                    "lon":rows[0][1],
                    "country":rows[0][2],
                    "state":rows[0][3],
                    "city":rows[0][4]
                }
        except Exception as e:
            self.conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e))
            print(exc_type, fname, exc_tb.tb_lineno)
        return None

    def insertImage(self, descriptor, idpadre, typeofelement):
        cur = self.conn.cursor()
        try:
            sql = "INSERT INTO elementos(descriptor, idpadre, typeofelement, hash_name) VALUES \
                   (%s,%s,%s,crypt(%s, gen_salt('xdes'))) RETURNING idelemento"
            values = descriptor, idpadre, typeofelement, descriptor
            #print sql
            cur.execute(sql, values)
            rows = cur.fetchall()
            cur.close()
            self.conn.commit()
            return rows[0][0]
        except Exception as e:
            self.conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e))
            print(exc_type, fname, exc_tb.tb_lineno)

    def insertFilePlaces(self,arch,lat,lon):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO place_archivo (lat,lon,archivo) \
            VALUES (%s,%s,%s)", (str(lat),str(lon),arch))
            cur.close()
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("insert FilePlace " + str(e) + " " +lat + "\t" + lon)

    def getPathRows(self,lat,lon):
        print("\n LOADING PATH/ROW...")
        start_time = time.time()
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * from wrscornerpoints where " + str(lat) + " >= ul_lat and " + str(lon) +"<= ul_lon and "+ str(lat) + " >= ur_lat and " + str(lon) +">= ur_lon and "+ str(lat) + " <= ll_lat and " + str(lon) +"<= ll_lon and "+ str(lat) + " <= lr_lat and " + str(lon) +"> lr_lon ")
            rows = cur.fetchall()
            cur.close()
            res = []
            #print len(rows)
            for x in rows:
                res.append({
                    "path":x[0],
                    "row":x[1],
                    "ctr_lat":x[2],
                    "ctr_lon":x[3],
                    "ul_lat":x[4],
                    "ul_lon":x[5],
                    "ur_lat":x[6],
                    "ur_lon":x[7],
                    "ll_lat":x[8],
                    "ll_lon":x[9],
                    "lr_lat":x[10],
                    "lr_lon":x[11]
                })
            print("\t Task end (time %s seconds)\n\n" % (time.time() - start_time))
            return res
        except Exception as e:
            print(e)
            self.conn.rollback()


    def closeConnection(self):
        self.conn.close()

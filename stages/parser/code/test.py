
from parser_landsat8 import ParserLansat8
from pymongo import MongoClient
import sys

metadata_path = sys.argv[1]
file_metadata = open(metadata_path, "r") 
metadata = file_metadata.read() 

client = MongoClient(sys.argv[3], 27018)
db = client.placesCollection

f = ParserLansat8(metadata,sys.argv[2],db,"xx","xx")
result = f.parse()
print(result)

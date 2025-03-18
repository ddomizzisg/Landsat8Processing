# Import the API
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
import json
import concurrent.futures

def download(scenes):
    for scene in scenes:
        #print(scene['satellite'])
        if scene['satellite'] == 8:
            print(scene['acquisition_date'].strftime('%Y-%m-%d'))
            print(scene['landsat_product_id'])
            try:
                ee.download(scene['landsat_product_id'], output_dir='./data')
            except:
                print("Error")

# Initialize the API with your EarthExplorer credentials
username = 'domizzi'
password = 'auja7f8yauja7f8y'

api = API(username, password)
ee = EarthExplorer(username, password)


# Search for Landsat TM scenes
scenes = api.search(
    dataset='landsat_ot_c2_l1',
    latitude=40.33288,
    longitude=-3.84938,
    start_date='2010-01-01',
    end_date='2024-12-31',
    max_results=10,
    max_cloud_cover=10
)

print(f"{len(scenes)} scenes found.")

sublist_size = len(scenes) // 3
print(sublist_size)
# Divide the list into three sublists
#sublist1 = scenes[:sublist_size]
#sublist2 = scenes[sublist_size: 2 * sublist_size]
#sublist3 = scenes[2 * sublist_size:]

#sublists = [sublist1, sublist2, sublist3]

#with concurrent.futures.ThreadPoolExecutor() as executor:
#    results = list(executor.map(download, sublists))
    #print(scene['acquisition_date'].strftime('%Y-%m-%d'))
    # Write scene footprints to disk
    #fname = f"{scene['landsat_product_id']}.geojson"
    #with open(fname, "w") as f:
    #    json.dump(scene['spatial_coverage'].__geo_interface__, f)
#    print(scene['landsat_product_id'])
#   try:
#        ee.download(scene['landsat_product_id'], output_dir='./data')
#    except:
#        print("Error")


api.logout()

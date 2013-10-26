import urllib
import json
import sys
if len(sys.argv) == 1:
	url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson'
	data = json.load(urllib.urlopen(url))
else:
	data = json.load(open(sys.argv[1]).read())
	
from datetime import datetime
with open(str(datetime.now()) + ".json", "w") as outfile:
    json.dump(data,outfile)

from mpl_toolkits.basemap import Basemap
def plotQuakes(place, data):
    lats = []
    longs = []
    magnitude = []
    depth = []
    for f in data['features']:
        if place in f['properties']['place']:
            longs.append(f['geometry']['coordinates'][0])
            lats.append(f['geometry']['coordinates'][1])
            magnitude.append(f['properties'][0])
            depth.append(f['geometry']['coordinates'][2])
    margin = 30
    maxLong = max(longs)
    maxLat = max(lats)
    minLat = min(lats)
    minLong = min(longs)
    center_Lat = mean(lats)
    center_Long = mean(longs)

    #normalize depth data to convert into colors
    normal_depth = (depth-min(depth))/(max(depth)-min(depth))
    depth_color = 0
    
    m = Basemap(llcrnrlon=minLong-margin,llcrnrlat=minLat-margin,
                urcrnrlon=maxLong+margin,urcrnrlat=maxLat+margin,
                resolution='l',area_thresh=1000.,projection='merc',
                lat_0=center_Lat,lon_0=center_Long)
            
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral',lake_color='blue')
    m.drawmapboundary(fill_color='aqua')
    m.plot(longs, lats, 'k.','MarkerSize',magnitude)
    return m
    
plotQuakes('Alaska', data)
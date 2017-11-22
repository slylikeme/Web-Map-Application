import folium
import pandas

# import the data file
data = pandas.read_csv('Volcanoes.txt')

# create variables from pandas dataframe
lat = list(data['LAT'])
lon = list(data['LON'])
name = list(data['NAME'])
elev = list(data['ELEV'])

# function to sort color of popups by altitude
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <= 3000:
        return 'orange'
    else:
        return 'red'

# create the map using folium
map = folium.Map(location=[40.75, -111.87], zoom_start=6, tiles='Mapbox Bright')

# framework for adding children
fgv = folium.FeatureGroup(name='Volcanoes')
fgp = folium.FeatureGroup(name='Population')

# create the child popup layer by looping through the data
for lt, ln, nme, el in zip(lat, lon, name, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6,
    popup=folium.Popup(nme + ': ' + str(el) + ' meters', parse_html=True),
    fill_color=color_producer(el), color='grey', fill=True, fill_opacity=0.7))

# create a child polygon layer to color countries by population
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 50000000
else 'blue' if 50000000 <= x['properties']['POP2005'] <= 100000000 else 'red'}))

# add the children
map.add_child(fgp)
map.add_child(fgv)

# add the option to turn layers off/on
map.add_child(folium.LayerControl())

# save the map
map.save('Map1.html')

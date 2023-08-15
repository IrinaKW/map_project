# %%
import pandas as pd
import numpy as np
import geopandas as gpd

import matplotlib.pyplot as plt

from geopy.geocoders import Nominatim

#read data and prepare the df
data=pd.read_csv('map_data.csv')
data['lived_there'] = data['lived_there'].apply(lambda x: 0 if x.strip()=='no' else 1)

#create function to get longitude and latitude by country name
geolocator = Nominatim(user_agent="Geolocation")
def geolocate(city):
    try:
        # Geolocate the center of the country
        loc = geolocator.geocode(city)
        # And return latitude and longitude
        return (loc.latitude, loc.longitude)
    except:
        # Return missing value
        return np.nan

#update dataframe with new features
data['geoloc']=data.city.apply(geolocate)
data['long']=data.geoloc.str[0]
data['lat']=data.geoloc.str[1]

# %%

# plot the locations on the worldmap
# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Creating axes and plotting world map
fig, ax = plt.subplots(figsize=(12, 6))
worldmap.plot(color="lightgrey", ax=ax)

# Plotting our Impact Energy data with a color map
x = data['lat']
y = data['long']
z = data['lived_there']
scatter=plt.scatter(x, y, c=z, cmap='autumn')
plt.legend(handles=scatter.legend_elements()[0], labels=['Lived there', 'Travel'], loc='lower center')

# Creating axis limits and title
#plt.xlim([-180, 180])
#plt.ylim([-90, 90])

plt.title("My Travel/Lived World Map")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()


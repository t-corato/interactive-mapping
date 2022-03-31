import folium
import pandas as pd

volcanoes = pd.read_csv("./Volcanoes.txt")

latitude = list(volcanoes["LAT"])
longitude = list(volcanoes["LON"])
elevation = list(volcanoes["ELEV"])
name = list(volcanoes["NAME"])


def color_elevation(elev: int) -> str:
    if elev < 1000:
        return "green"
    elif 1000 <= elev < 3000:
        return "orange"
    else:
        return "red"


html = """<h4>Volcano information:</h4>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map_ = folium.Map(location=[35, -99], tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="USA Volcanoes Map")

for lat, lon, el, nm in zip(latitude, longitude, elevation, name):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lat, lon], popup=folium.Popup(iframe), fill=True,
                                     fill_color=color_elevation(el), color="grey", fill_opacity=0.7))

map_.add_child(fgv)

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(
    data=open("./world.json", "r", encoding="utf-8-sig").read(), style_function=lambda x:
    {"fillColor": "green" if x["properties"]["POP2005"] < 10000000 else "orange"
     if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))

map_.add_child(fgp)

map_.add_child(folium.LayerControl())

map_.save("map_.html")

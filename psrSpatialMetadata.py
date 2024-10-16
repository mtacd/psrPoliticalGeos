# import requests
import requests
import pandas as pd
from datetime import date, datetime

#set up dictionary of URLs

urls = {
    'NYC Council Districts' : 'https://data.cityofnewyork.us/resource/q9fc-2e5x.json',
    'NYC Community Districts' : 'https://data.cityofnewyork.us/resource/jp9i-3b7y.json',
    'NY Congressional Districts' : 'https://services6.arcgis.com/EbVsqZ18sv1kVJ3k/arcgis/rest/services/NYS_Congressional_Districts/FeatureServer/0?f=pjson',
    'NY State Assembly' : 'https://services6.arcgis.com/EbVsqZ18sv1kVJ3k/arcgis/rest/services/NYS_Assembly_Districts/FeatureServer/0?f=pjson',
    'NY State Senate' : 'https://services6.arcgis.com/EbVsqZ18sv1kVJ3k/arcgis/rest/services/NYS_Senate_Districts/FeatureServer/0?f=pjson',
    'NY Counties' : 'https://services6.arcgis.com/EbVsqZ18sv1kVJ3k/arcgis/rest/services/NYS_Civil_Boundaries/FeatureServer/2?f=pjson',
    'NY Cities and Towns' : 'https://services6.arcgis.com/EbVsqZ18sv1kVJ3k/ArcGIS/rest/services/NYS_Civil_Boundaries/FeatureServer/6?f=pjson',
    'CT Counties' : 'https://services1.arcgis.com/FjPcSmEFuDYlIdKC/arcgis/rest/services/Connecticut_County_Index/FeatureServer/0?f=pjson',
    'CT Cities and Towns' : 'https://services1.arcgis.com/FjPcSmEFuDYlIdKC/arcgis/rest/services/Connecticut_and_Vicinity_Town_Boundary_Set/FeatureServer/1?f=pjson'
}

geos = []
dates = []
metaFieldsSocrata = '?$select=:*, *'
df = pd.DataFrame(columns = ['geo', 'last modified date', 'last checked on'])
today = date.today()

for geo in urls: 
    if "data.cityofnewyork" in urls[geo]:
        r = requests.get(urls[geo] + metaFieldsSocrata)
        modified = r.headers['Last-Modified']
        geos.append(geo)
        dates.append(modified)
    elif "arcgis" in urls[geo]:
        r = requests.get(urls[geo])
        modified = r.json()['editingInfo']['dataLastEditDate']
        geos.append(geo)
        dates.append(modified)

df = pd.DataFrame({'geo' : geos, 
                    'last modified date' : dates, 
                    'last checked on' : today
                    })

df
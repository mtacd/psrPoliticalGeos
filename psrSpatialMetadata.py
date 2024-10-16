# import requests
import requests
import pandas as pd
from datetime import datetime

def metadata():
    # create dictionary of URLs where the keys are the geography and the values are the links to that dataset in either the NYC SODA API or the NY/CT State GIS API
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

    # create empty lists that we'll use to store data in the for loop
    geos = []
    dates = []

    # the SODA API has a specific parameter for selecting metadata. For the NYC metadata, this parameter will have to be appended to the URL when it's passed to the GET request
    metaFieldsSocrata = '?$select=:*, *'

    # start for loop
    for geo in urls: 
        # for each entry in the urls dictionary, check which API it's coming from
        if "data.cityofnewyork" in urls[geo]:
            # if the URL is in the NYC API, grab the last modified date from the headers. Append result to lists
            r = requests.get(urls[geo] + metaFieldsSocrata)
            modified = r.headers['Last-Modified']
            geos.append(geo)
            dates.append(modified)
        elif "arcgis" in urls[geo]:
            # if the URL is in the ArcGIS API, get the last modified date from the JSON response, divide it by 1000, an dhtne convert it to a date field. Append results to list.
            r = requests.get(urls[geo])
            modified_raw = r.json()['editingInfo']['dataLastEditDate']
            modified = datetime.fromtimestamp(int(modified_raw / 1000))
            geos.append(geo)
            dates.append(modified)

    # create dataframe and add data from lists to the dataframe
    df = pd.DataFrame({'geo' : geos, 
                        'last modified date' : dates
                        })

    # convert the date field to a datetime
    df['last modified date'] = pd.to_datetime(df['last modified date'])

    # export CSV
    df.to_excel('psrGeoMetadata.xlsx', index=False)
# psrPoliticalGeos

*Code written by Tom Chen and Drew Stanley*
 
 Updates PSR with political geographies like NYC Council, NYS Assembly, etc. and updates the PSR assets' lat/longs with parent lat/longs or station lat/longs. 

There are three modules (Module 1 is the main one while modluesl): 
1. *psrPoliticalGeo.py*
   This is the main script and **it's the only one that actually needs to run**. Modules 2-3 are linked/nested within each other, so running *psrPoliticalGeo.py* will run everything. This script is where all of the political district information is attached to the assets as well as city/town and county (both NY and CT) after the assets lat/longs have been updated.
    2. *psrNearStationUpdate.py*
        After Module 3 runs, this module looks at any PSR assets who don't have a lat/long AND don't have a parent asset with a lat/long. It then looks at those assets to see if they're near a subway station - if they are, it updates the asset with the subway station's lat/long.
        3. *psrParentLatLongUpdate.py*
           This looks up any PSR assets that don't have a lat/long and assigns them a lat/long from the parent asset, if the parent asset has sa lat/long.

ArcGIS files and other dependencies that the code needs to run are not included here - you would need to have those stored locally. This includes any of the spatial files for political districts.

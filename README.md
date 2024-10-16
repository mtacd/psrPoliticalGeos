# psrPoliticalGeos

*Code written by Tom Chen and Drew Stanley*
 
 Updates PSR with political geographies like NYC Council, NYS Assembly, etc. and updates the PSR assets' lat/longs with parent lat/longs or station lat/longs. 

There are three modules. The first module is at the top level, and then the other two submodules are nested below the top level: 
* *psrPoliticalGeo.py*  
   This is the main script and **it's the only one that actually needs to run**. The other two modules below are linked/nested within each other, so running *psrPoliticalGeo.py* will run everything. This script is where all of the political district information is attached to the assets as well as city/town and county (both NY and CT) after the assets lat/longs have been updated.

* *psrSpatialMetadata.py*
   This goes into the APIs of NYC, NYS, and CTS GIS portals and pulls the date of the last time that each of the spatial datasets were updated. After the date is pulled, it's added into a spreadsheet for the PSR team.

    * *psrNearStationUpdate.py*  
        After the module below this one runs, this module looks at any PSR assets who don't have a lat/long AND don't have a parent asset with a lat/long. It then looks at those assets to see if they're near a subway station - if they are, it updates the asset with the subway station's lat/long. Running just this module will also run the module below

        * *psrParentLatLongUpdate.py*  
           This module looks up any PSR assets that don't have a lat/long and assigns them a lat/long from the parent asset, if the parent asset has sa lat/long.

ArcGIS files and other dependencies that the code needs to run are not included here - you would need to have those stored locally. This includes any of the spatial files for political districts.

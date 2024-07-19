# psrPoliticalGeos

*Code written by Tom Chen and Drew Stanley*
 
 Updates PSR with political geographies like NYC Council, NYS Assembly, etc.

*psrLatLongUpdate.py* is the module that updates PSR assets with no lat/long with their parent asset that does have a lat/long. This module is then run with the rest of the political district spatial joins in *psrPoliticalGeos.py*.

ArcGIS files and other dependencies that the code needs to run are not included here - you would need to have those stored locally. This includes any of the spatial files for political districts.

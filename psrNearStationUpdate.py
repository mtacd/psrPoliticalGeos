import arcpy 

import psrParentLatLongUpdate

def nearStation():

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")

    inputFile = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrParentLatLong_updated"

    # select only the assets with no lat/long
    noLatLongInter = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\nearStationNoLatLong_inter"
    arcpy.analysis.Select(
        in_features=inputFile, 
        out_feature_class=noLatLongInter, 
        where_clause="LATITUDE IS NULL And LONGITUDE IS NULL")
    

    arcpy.analysis.Select(
    in_features=noLatLongInter,
    out_feature_class= r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\nearStationNoLatLong",
    where_clause="KEY_ASSET_NEAR_STATION IS NOT NULL"
)

nearStation()
    
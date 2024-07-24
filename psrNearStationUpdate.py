import arcpy 

import psrParentLatLongUpdate

# psrParentLatLongUpdate.updateLatLong()

def nearStation():

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")

    #bring in table with assets that have had their lat/long updated with parent assets, if needed
    inputFile = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrParentLatLong_updated"

    # select only records that have no lat long and have are near a station
    near = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\nearStation"
    arcpy.analysis.Select(in_features=inputFile, 
                          out_feature_class=near, 
                          where_clause="LATITUDE IS NULL And LONGITUDE IS NULL And KEY_ASSET_NEAR_STATION IS NOT NULL")
    
    # update the subset table assets' lat/long columns with station lat/long from original table
    joined_data = arcpy.management.JoinField(in_data=near, in_field="KEY_ASSET_NEAR_STATION", join_table=inputFile, join_field="KEY_ASSET", fm_option="NOT_USE_FM", index_join_fields="NO_INDEXES")[0]

nearStation()

import arcpy 

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

import psrParentLatLongUpdate

# run the first script that matches any child assets that don't have a lat/long to a parent asset that does
psrParentLatLongUpdate.updateLatLong()

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
    joined_data = arcpy.management.JoinField(in_data=near, 
                                             in_field="KEY_ASSET_NEAR_STATION", 
                                             join_table=inputFile, 
                                             join_field="KEY_ASSET",
                                             fields = ['LONGITUDE', 'LATITUDE'],
                                             fm_option="NOT_USE_FM", 
                                             index_join_fields="NO_INDEXES")[0]
    
    # delete old NULL lat/longs from new joined_data, rename new columns to original field names
    delete_old = arcpy.management.DeleteField(joined_data,
                                              ['LATITUDE', 'LONGITUDE'])
    
    updateNames1 = arcpy.management.AlterField(delete_old, 
                                              field = 'LATITUDE_1',
                                              new_field_name = 'LATITUDE',
                                              new_field_alias = 'LATITUDE')
    
    updateNames2 = arcpy.management.AlterField(delete_old, 
                                            field = 'LONGITUDE_1',
                                            new_field_name = 'LONGITUDE',
                                            new_field_alias = 'LONGITUDE')
    
    # join table of updated long/lats to the original table again, then remove the updated assets from the original dataset 
    joined_data = arcpy.management.JoinField(in_data=inputFile, 
                                             in_field="KEY_ASSET", 
                                             join_table=updateNames2, 
                                             join_field="KEY_ASSET",
                                             fields = ['LONGITUDE', 'LATITUDE'],
                                             fm_option="NOT_USE_FM", 
                                             index_join_fields="NO_INDEXES")[0]
    
    removed = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\removed"
    remove_old_rows =  arcpy.analysis.Select(in_features=joined_data,
                                             out_feature_class=removed, 
                                             where_clause="LONGITUDE_1 IS NULL And LATITUDE_1 IS NULL")
    
    # union the two datasets together again with the updated records
    #drop old columns first
    delete_old = arcpy.management.DeleteField(remove_old_rows,
                                            ['LATITUDE_1', 'LONGITUDE_1'])
    
    # then union/merge the two back together again 
    updateNearStations = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\updateNearStations"
    arcpy.management.Merge([delete_old, updateNames2],
                                    output = updateNearStations)
    

    # select only non-null lat/long assets for the next module to take in 
    noNullNearStation = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\noNullNearStation"
    arcpy.analysis.Select(in_features=updateNearStations, out_feature_class=noNullNearStation, where_clause="LATITUDE IS NOT NULL And LONGITUDE IS NOT NULL")

    # # used to check the attribute table without having to open ArcGIS Pro
    # columns = [f.name for f in arcpy.ListFields(merged) if f.type!="Geometry"]
    # #List the fields you want to include. I want all columns except the geometry
    # df = pd.DataFrame(data=arcpy.da.SearchCursor(merged, columns), columns=columns)

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb", workspace=r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb"):
        nearStation()
import arcpy

def updateLatLong():

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")

    tableOutput = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\excel_file"
    arcpy.conversion.ExcelToTable(
    Input_Excel_File = r"C:\Users\1292346\gisProjects\PSR\psrFinal\PSR_Assets.xlsx",
    Output_Table=tableOutput)

    # Process: Convert spreadsheet to X/Y point data (XY Table To Point) (management)
    PSR_point_data = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrLatLong"
    arcpy.management.XYTableToPoint(in_table=tableOutput.__str__().format(**locals(),**globals())if isinstance(tableOutput, str) else tableOutput, out_feature_class=PSR_point_data, x_field="LONGITUDE", y_field="LATITUDE", coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: add Y/N field showing whether record has Latitude or not (Calculate Field) (management)
    PSR_Point_Data_table_2 = arcpy.management.CalculateField(in_table=PSR_point_data, field="hasLat", expression="hasLat(!LATITUDE!)", code_block="""def hasLat(LATITUDE):
    if LATITUDE is None:
        return \"N\"
    else:
        return \"Y\"""")[0]

    # Process: add y/n field showing whether asset is a parent of other assets (Calculate Field) (management)
    PSR_Point_Data_table_3 = arcpy.management.CalculateField(in_table=PSR_Point_Data_table_2, field="isParent", expression="isParent(!KEY_ASSET!, !KEY_ASSET_PARENT!)", code_block="""def isParent(KEY_ASSET, KEY_ASSET_PARENT):
    if KEY_ASSET == KEY_ASSET_PARENT:
        return \"Y\"
    else:
        return \"N\"""")[0]

    # Process: rename latitude (2) (Alter Field) (management)
    lat_renamed_2_ = arcpy.management.AlterField(in_table=PSR_Point_Data_table_3, 
                                                 field="LATITUDE", 
                                                 new_field_name="old_latitude", clear_field_alias="CLEAR_ALIAS")[0]

    # Process: rename longitude(3) (Alter Field) (management)
    long_renamed_3_ = arcpy.management.AlterField(in_table=lat_renamed_2_, 
                                                  field="LONGITUDE", 
                                                  new_field_name="old_longitude", clear_field_alias="CLEAR_ALIAS")[0]

    # Process: Select only rows that are assets with no lat/long (Select) (analysis)
    noLatLong = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrLatLongnoLatLong"
    arcpy.analysis.Select(in_features=long_renamed_3_, out_feature_class=noLatLong, where_clause="hasLat = 'N'")

    # Process: select only rows that are parent assets (Select) (analysis)
    parents = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrLatLongparents"
    arcpy.analysis.Select(in_features=long_renamed_3_, out_feature_class=parents, where_clause="isParent = 'Y'")

    # Process: join assets with no lat/long to parent assets that do (some don't) (Join Field) (management)
    joined_data = arcpy.management.JoinField(in_data=noLatLong, in_field="KEY_ASSET_PARENT", join_table=parents, join_field="KEY_ASSET", fields=["old_longitude", "old_latitude"], fm_option="NOT_USE_FM", index_join_fields="NO_INDEXES")[0]

    # Process: rename latitude (3) (Alter Field) (management)
    lat_renamed_3_ = arcpy.management.AlterField(in_table=joined_data, field="old_latitude_1", new_field_name="new_latitude", new_field_alias="new_latitude", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: rename longitude(3) (2) (Alter Field) (management)
    long_renamed_2_ = arcpy.management.AlterField(in_table=lat_renamed_3_, field="old_longitude_1", new_field_name="new_longitude", new_field_alias="new_longitude", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Select only the assets where the lat/long was updated with the parent lat/long (Select) (analysis)
    noNulls = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrLatLongnoNulls"
    arcpy.analysis.Select(in_features=long_renamed_2_, out_feature_class=noNulls, where_clause="new_longitude IS NOT NULL And new_latitude IS NOT NULL")

    # Process: need to create a copy of the table with updated assets (Copy) (management)
    copy_of_No_nulls = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrLatLongnoNulls_1"
    arcpy.management.Copy(in_data=noNulls, out_data=copy_of_No_nulls)

    # Process: Delete Field (Delete Field) (management)
    new_lat_longs = arcpy.management.DeleteField(in_table=copy_of_No_nulls, drop_field=["old_longitude", "old_latitude", "hasLat", "isParent"])[0]

    # Process: rename latitude (Alter Field) (management)
    lat_renamed = arcpy.management.AlterField(in_table=new_lat_longs, field="new_latitude", new_field_name="LATITUDE", new_field_alias="LATITUDE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: rename longitude (Alter Field) (management)
    long_renamed = arcpy.management.AlterField(in_table=lat_renamed, field="new_longitude", new_field_name="LONGITUDE", new_field_alias="LONGITUDE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join updated assets back onto the original ones (Join Field) (management)
    updated_assets = arcpy.management.JoinField(in_data=long_renamed_3_, in_field="KEY_ASSET", join_table=noNulls, join_field="KEY_ASSET", fields=["new_longitude", "new_latitude"])[0]

    # Process: Remove assets from original dataset that we just updated (Select) (analysis)
    remove_original_assets = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrLatLong_Select"
    arcpy.analysis.Select(in_features=updated_assets, out_feature_class=remove_original_assets, where_clause="new_longitude IS NULL And new_latitude IS NULL")

    # Process: delete extra columns (Delete Field) (management)
    extra_columns_removed = arcpy.management.DeleteField(in_table=remove_original_assets, drop_field=["hasLat", "isParent", "new_longitude", "new_latitude"])[0]

    # Process: rename latitude (4) (Alter Field) (management)
    lat_renamed_4_ = arcpy.management.AlterField(in_table=extra_columns_removed, field="old_latitude", new_field_name="LATITUDE", new_field_alias="LATITUDE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: rename longitude (2) (Alter Field) (management)
    long_renamed_4_ = arcpy.management.AlterField(in_table=lat_renamed_4_, field="old_longitude", new_field_name="LONGITUDE", new_field_alias="LONGITUDE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: union updated assets with the original table that has the updated assets removed. (Merge) (management)
    lat_longs_updated_parents = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrParentLatLong_updated"
    arcpy.management.Merge(inputs=[long_renamed, long_renamed_4_], output=lat_longs_updated_parents)

    # Process: Select only non-null lat/long coordinates (Select) (analysis)
    updatedLatLongNoNulls = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\updatedLatLongNoNulls"
    arcpy.analysis.Select(in_features=lat_longs_updated_parents, out_feature_class=updatedLatLongNoNulls, where_clause="LATITUDE IS NOT NULL And LONGITUDE IS NOT NULL")

    #the two code blocks below would generate an excel file of all assets and another with only lat/long. Since we use the geodatabase feature layer version of the table, the excel files aren't necessary

    # # Process: Table To Excel (Table To Excel) (conversion)
    # latLongUpdatedAll_xlsx = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrLatLonglatLongUpdatedAll.xlsx"
    # arcpy.conversion.TableToExcel(Input_Table=[lat_longs_updated], Output_Excel_File=latLongUpdatedAll_xlsx, Use_field_alias_as_column_header="ALIAS")

    # # Process: Table To Excel (Table To Excel) (conversion)
    # latLongUpdated_noNulls = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrLatLonglatLongUpdatedNoNulls.xlsx"
    # arcpy.conversion.TableToExcel(Input_Table=[updatedLatLongNoNulls], Output_Excel_File=latLongUpdated_noNulls, Use_field_alias_as_column_header="ALIAS")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb", workspace=r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb"):
        updateLatLong()

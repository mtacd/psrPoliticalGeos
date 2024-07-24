# contains ArcGIS tools for spatial analysis.
import arcpy

# to conduct data fransformation procedures
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

#
from sys import argv

# 
import numpy as np

#import the script that updates latitude and longitude
import psrParentLatLongUpdate


# this matches a lat/long to those PSR assets who do not have a lat/long but their parent asset does.
# the resulting feature layer that is all assets with a lat/long is brought back in.

psrParentLatLongUpdate.updateLatLong()

print(f"Latitudes and longitudes have been updated.")

PSRs = r"C:\Users\1292346\gisProjects\PSR\psrFinal\psrFinal.gdb\psrLatLongupdatedLatLongNoNulls"

cityCouncil_dir = r"C:/Users/1292346/gisProjects/PSR/psrFinal/districts/nycCouncil_Project.shp"

communityDist_dir = r"C:/Users/1292346/gisProjects/PSR/psrFinal/districts/nycd.shp"

congressionalDist_dir = r"C:/Users/1292346/gisProjects/PSR/psrFinal/districts/congressionalDistricts.shp"

stateAssembly_dir = r"C:/Users/1292346/gisProjects/PSR/psrFinal/districts/NYS_Assembly_Distric_Project.shp"

stateSenate_dir = r"C:/Users/1292346/gisProjects/PSR/psrFinal/districts/NYS_Senate_Districts_Project.shp"

county_dir = r"C:\Users\1292346\gisProjects\PSR\psrFinal\districts\NYS_and_CT_counties_project.shp"

city_dir = r"C:\Users\1292346\gisProjects\PSR\psrFinal\districts\NY_CT_cities_towns.shp"

output_dir = r"C:/Users/1292346/gisProjects/PSR/psrFinal/psrFinal.gdb"

excel_output_dir = r"C:/Users/1292346/gisProjects/PSR/psrFinal"


def Model(PSR_assets = PSRs,
          cityCouncil = cityCouncil_dir,
          communityDistrict = communityDist_dir,
          congressionalDistrict = congressionalDist_dir,
          stateAssembly = stateAssembly_dir,
          stateSenate = stateSenate_dir,
          counties = county_dir,
          cities_towns = city_dir,
          output = output_dir
         ):  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(r"C:\Program Files\Arcgis\Pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")
    arcpy.ImportToolbox(r"C:\Program Files\Arcgis\Pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")

    # Process: Excel To Table (Excel To Table) (conversion)
    # PSR_Assets = f"{output}/PSR_Assets"
    # arcpy.conversion.ExcelToTable(
    #     Input_Excel_File = Input_Excel_File, 
    #     Output_Table = PSR_Assets, 
    #     Sheet = "updatedLatLongNoNulls", 
    #     field_names_row = 1, 
    #     cell_range = ""
    # )
    print(f"Processing spatial joins...")
    # Process: XY Table To Point (XY Table To Point) (management)
    PSR_Assets_XY = f"{output}/PSR_Assets_XY"
    arcpy.management.XYTableToPoint(
        in_table = PSR_assets, 
        out_feature_class = PSR_Assets_XY, 
        x_field = "LONGITUDE", 
        y_field = "LATITUDE", 
        z_field = "", 
        coordinate_system = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision"
    )
    
    # Intersection between PSR Assets and City Council for Parent City Council Zone
    PSR_Assets_Parent_CC = f"{output}/PSR_Assets_Parent_CC"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_XY,
        join_features = cityCouncil,
        out_feature_class = PSR_Assets_Parent_CC,
        join_operation = "JOIN_ONE_TO_ONE",
        join_type = "KEEP_ALL",
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_XY},KEY_ASSET,-1,-1; DIST_CITY_COUNCIL \" DIST_CITY_COUNCIL \" true true false 50 Text 0 0,First,#,{PSR_Assets_XY}, DIST_CITY_COUNCIL,-1,-1; DIST_COMMUNITY \" DIST_COMMUNITY \" true true false 50 Text 0 0,First,#,{PSR_Assets_XY}, DIST_COMMUNITY,-1,-1; DIST_CONGRESSIONAL \" DIST_CONGRESSIONAL \" true true false 50 Text 0 0,First,#,{PSR_Assets_XY}, DIST_CONGRESSIONAL,-1,-1; DIST_STATE_ASSEMBLY \" DIST_STATE_ASSEMBLY \" true true false 50 Text 0 0,First,#,{PSR_Assets_XY}, DIST_STATE_ASSEMBLY,-1,-1; DIST_STATE_SENATE \" DIST_STATE_SENATE \" true true false 50 Text 0 0,First,#,{PSR_Assets_XY}, DIST_STATE_SENATE,-1,-1; City_Council_Parent_Dist_ID \"City_Council_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{cityCouncil}, CounDist,-1,-1",
        search_radius = "", 
        distance_field_name = ""
    )
    
    # Intersection between PSR Assets and Community District for Parent Community District Zone
    PSR_Assets_Parent_CC_CM = f"{output}/PSR_Assets_Parent_CC_CM"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_Parent_CC,
        join_features = communityDistrict,
        out_feature_class = PSR_Assets_Parent_CC_CM,
        join_operation = "JOIN_ONE_TO_ONE",
        join_type = "KEEP_ALL",
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC},KEY_ASSET,-1,-1; DIST_CITY_COUNCIL \" DIST_CITY_COUNCIL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC}, DIST_CITY_COUNCIL,-1,-1; DIST_COMMUNITY \" DIST_COMMUNITY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC}, DIST_COMMUNITY,-1,-1; DIST_CONGRESSIONAL \" DIST_CONGRESSIONAL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC}, DIST_CONGRESSIONAL,-1,-1; DIST_STATE_ASSEMBLY \" DIST_STATE_ASSEMBLY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC}, DIST_STATE_ASSEMBLY,-1,-1; DIST_STATE_SENATE \" DIST_STATE_SENATE \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC}, DIST_STATE_SENATE,-1,-1;City_Council_Parent_Dist_ID \"City_Council_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{PSR_Assets_Parent_CC}, City_Council_Parent_Dist_ID,-1,-1; Community_District_Parent_Dist_ID \"Community_District_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{communityDistrict}, BoroCD,-1,-1",
        search_radius = "", 
        distance_field_name = ""
    )
    
    
    # Intersection between PSR Assets and Congressional District for Parent Congressional District Zone
    PSR_Assets_Parent_CC_CM_CO = f"{output}/PSR_Assets_Parent_CC_CM_CO"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_Parent_CC_CM,
        join_features = congressionalDistrict,
        out_feature_class = PSR_Assets_Parent_CC_CM_CO,
        join_operation = "JOIN_ONE_TO_ONE",
        join_type = "KEEP_ALL",
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM},KEY_ASSET,-1,-1; DIST_CITY_COUNCIL \" DIST_CITY_COUNCIL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM}, DIST_CITY_COUNCIL,-1,-1; DIST_COMMUNITY \" DIST_COMMUNITY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM}, DIST_COMMUNITY,-1,-1; DIST_CONGRESSIONAL \" DIST_CONGRESSIONAL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM}, DIST_CONGRESSIONAL,-1,-1; DIST_STATE_ASSEMBLY \" DIST_STATE_ASSEMBLY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM}, DIST_STATE_ASSEMBLY,-1,-1; DIST_STATE_SENATE \" DIST_STATE_SENATE \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM}, DIST_STATE_SENATE,-1,-1; City_Council_Parent_Dist_ID \"City_Council_Parent_Dist_ID \" true true false 10 Long 0 0,First,#, {PSR_Assets_Parent_CC_CM}, City_Council_Parent_Dist_ID,-1,-1; Community_District_Parent_Dist_ID \"Community_District_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM}, Community_District_Parent_Dist_ID,-1,-1; Congressional_District_Parent_Dist_ID \"Congressional_District_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{congressionalDistrict}, CongDist,-1,-1",
        search_radius = "", 
        distance_field_name = ""
    )
    
    
    # Intersection between PSR Assets and State Assembly District for Parent State Assembly District Zone
    PSR_Assets_Parent_CC_CM_CO_SA = f"{output}/PSR_Assets_Parent_CC_CM_CO_SA"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_Parent_CC_CM_CO,
        join_features = stateAssembly,
        out_feature_class = PSR_Assets_Parent_CC_CM_CO_SA,
        join_operation = "JOIN_ONE_TO_ONE",
        join_type = "KEEP_ALL",
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO},KEY_ASSET,-1,-1; DIST_CITY_COUNCIL \" DIST_CITY_COUNCIL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO}, DIST_CITY_COUNCIL,-1,-1; DIST_COMMUNITY \" DIST_COMMUNITY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO}, DIST_COMMUNITY,-1,-1; DIST_CONGRESSIONAL \" DIST_CONGRESSIONAL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO}, DIST_CONGRESSIONAL,-1,-1; DIST_STATE_ASSEMBLY \" DIST_STATE_ASSEMBLY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO}, DIST_STATE_ASSEMBLY,-1,-1; DIST_STATE_SENATE \" DIST_STATE_SENATE \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO}, DIST_STATE_SENATE,-1,-1; City_Council_Parent_Dist_ID \"City_Council_Parent_Dist_ID \" true true false 10 Long 0 0,First,#, {PSR_Assets_Parent_CC_CM_CO}, City_Council_Parent_Dist_ID,-1,-1; Community_District_Parent_Dist_ID \"Community_District_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO}, Community_District_Parent_Dist_ID,-1,-1; Congressional_District_Parent_Dist_ID \"Congressional_District_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO}, Congressional_District_Parent_Dist_ID,-1,-1; State_Assembly_Parent_Dist_ID \"State_Assembly_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{stateAssembly}, AssemDist,-1,-1",
        search_radius = "", 
        distance_field_name = ""
    )
    
    
    # Intersection between PSR Assets and State Senate District for Parent State Senate District Zone
    PSR_Assets_Parent_CC_CM_CO_SA_SS = f"{output}/PSR_Assets_Parent_CC_CM_CO_SA_SS"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_Parent_CC_CM_CO_SA,
        join_features = stateSenate,
        out_feature_class = PSR_Assets_Parent_CC_CM_CO_SA_SS,
        join_operation = "JOIN_ONE_TO_ONE",
        join_type = "KEEP_ALL",
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA},KEY_ASSET,-1,-1; DIST_CITY_COUNCIL \" DIST_CITY_COUNCIL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, DIST_CITY_COUNCIL,-1,-1; DIST_COMMUNITY \" DIST_COMMUNITY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, DIST_COMMUNITY,-1,-1; DIST_CONGRESSIONAL \" DIST_CONGRESSIONAL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, DIST_CONGRESSIONAL,-1,-1; DIST_STATE_ASSEMBLY \" DIST_STATE_ASSEMBLY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, DIST_STATE_ASSEMBLY,-1,-1; DIST_STATE_SENATE \" DIST_STATE_SENATE \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, DIST_STATE_SENATE,-1,-1; CityCouncil_Parent_Dist_ID \"CityCouncil_Parent_Dist_ID \" true true false 10 Long 0 0,First,#, {PSR_Assets_Parent_CC_CM_CO_SA}, City_Council_Parent_Dist_ID,-1,-1; CommunityDistrict_Parent_Dist_ID \"CommunityDistrict_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, Community_District_Parent_Dist_ID,-1,-1; CongressionalDistrict_Parent_Dist_ID \"CongressionalDistrict_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, Congressional_District_Parent_Dist_ID,-1,-1; StateAssembly_Parent_Dist_ID \"StateAssembly_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA}, State_Assembly_Parent_Dist_ID,-1,-1; StateSenate_Parent_Dist_ID \"StateSenate_Parent_Dist_ID \" true true false 10 Long 0 0,First,#,{stateSenate}, StSenDist,-1,-1",
        search_radius = "", 
        distance_field_name = ""
    )

    # Intersection between PSR Assets and Counties shapefile
    PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties = f"{output}/PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_Parent_CC_CM_CO_SA_SS,
        join_features = counties,
        out_feature_class = PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,
        join_operation ="JOIN_ONE_TO_ONE",
        join_type ="KEEP_ALL",
        field_mapping = f"KEY_ASSET \" KEY_ASSET \" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},KEY_ASSET,-1,-1; DIST_CITY_COUNCIL \" DIST_CITY_COUNCIL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},DIST_CITY_COUNCIL,0,49;DIST_COMMUNITY \" DIST_COMMUNITY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},DIST_COMMUNITY,0,49;DIST_CONGRESSIONAL \" DIST_CONGRESSIONAL \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},DIST_CONGRESSIONAL,0,49;DIST_STATE_ASSEMBLY \" DIST_STATE_ASSEMBLY \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},DIST_STATE_ASSEMBLY,0,49;DIST_STATE_SENATE \" DIST_STATE_SENATE \" true true false 50 Text 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},DIST_STATE_SENATE,0,49;CityCouncil_Parent_Dist_ID \"CityCouncil_Parent_Dist_ID \" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},CityCouncil_Parent_Dist_ID,-1,-1;CommunityDistrict_Parent_Dist_ID \"CommunityDistrict_Parent_Dist_ID \" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},CommunityDistrict_Parent_Dist_ID,-1,-1;CongressionalDistrict_Parent_Dist_ID \"CongressionalDistrict_Parent_Dist_ID \" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},CongressionalDistrict_Parent_Dist_ID,-1,-1;StateAssembly_Parent_Dist_ID \"StateAssembly_Parent_Dist_ID \" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},StateAssembly_Parent_Dist_ID,-1,-1;StateSenate_Parent_Dist_ID \"StateSenate_Parent_Dist_ID \" true true false 4 Long 0 0,First,#,{PSR_Assets_Parent_CC_CM_CO_SA_SS},StateSenate_Parent_Dist_ID,-1,-1; county_name \"county_name\" true true false 40 Text 0 0,First,#, {counties}, NAMELSAD, -1,-1",
        search_radius = "",
        distance_field_name = ""
    )
    
    # Intersection between PSR Assets and cities and towns shapefile
    PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties_cities = f"{output}/PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties_cities"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,
        join_features = cities_towns,
        out_feature_class = PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties_cities,
        join_operation ="JOIN_ONE_TO_ONE",
        join_type="KEEP_ALL",
        field_mapping='KEY_ASSET " KEY_ASSET " true true false 4 Long 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,KEY_ASSET,-1,-1;DIST_CITY_COUNCIL " DIST_CITY_COUNCIL " true true false 50 Text 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,DIST_CITY_COUNCIL,0,49;DIST_COMMUNITY " DIST_COMMUNITY " true true false 50 Text 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,DIST_COMMUNITY,0,49;DIST_CONGRESSIONAL " DIST_CONGRESSIONAL " true true false 50 Text 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,DIST_CONGRESSIONAL,0,49;DIST_STATE_ASSEMBLY " DIST_STATE_ASSEMBLY " true true false 50 Text 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,DIST_STATE_ASSEMBLY,0,49;DIST_STATE_SENATE " DIST_STATE_SENATE " true true false 50 Text 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,DIST_STATE_SENATE,0,49;CityCouncil_Parent_Dist_ID "CityCouncil_Parent_Dist_ID " true true false 4 Long 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,CityCouncil_Parent_Dist_ID,-1,-1;CommunityDistrict_Parent_Dist_ID "CommunityDistrict_Parent_Dist_ID " true true false 4 Long 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,CommunityDistrict_Parent_Dist_ID,-1,-1;CongressionalDistrict_Parent_Dist_ID "CongressionalDistrict_Parent_Dist_ID " true true false 4 Long 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,CongressionalDistrict_Parent_Dist_ID,-1,-1;StateAssembly_Parent_Dist_ID "StateAssembly_Parent_Dist_ID " true true false 4 Long 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,StateAssembly_Parent_Dist_ID,-1,-1;StateSenate_Parent_Dist_ID "StateSenate_Parent_Dist_ID " true true false 4 Long 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,StateSenate_Parent_Dist_ID,-1,-1;county_name "county_name" true true false 40 Text 0 0,First,#,PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties,county_name,0,39; "city_name" "city_name" true true false 50 Text 0 0,First,#,NY_CT_cities_towns,NAME,0,49',
        match_option="INTERSECT",
        search_radius= "",
        distance_field_name=""
    )
    

    # Process: Pairwise Buffer (Pairwise Buffer) (analysis)
    PSR_Assets_500ftBuffer = f"{output}/PSR_Assets_500ftBuffer"
    arcpy.analysis.PairwiseBuffer(
        in_features = PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties_cities, 
        out_feature_class = PSR_Assets_500ftBuffer, 
        buffer_distance_or_field = "500 Feet", 
        dissolve_option = "NONE", 
        dissolve_field = [], 
        method = "PLANAR", 
        max_deviation = "0 DecimalDegrees"
    )

    # Process: Spatial Join for City Council (Spatial Join) (analysis)
    PSR_Assets_CityCouncil = f"{output}/PSR_Assets_CityCouncil"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_500ftBuffer, 
        join_features = cityCouncil, 
        out_feature_class = PSR_Assets_CityCouncil, 
        join_operation = "JOIN_ONE_TO_MANY", 
        join_type = "KEEP_COMMON", 
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_500ftBuffer},KEY_ASSET,-1,-1; Dist_ID \"Dist_ID \" true true false 10 Long 0 0,First,#,{cityCouncil}, CounDist,-1,-1",
        match_option = "INTERSECT", 
        search_radius = "", 
        distance_field_name = ""
    )

    # Process: Spatial Join for Community District (Spatial Join) (analysis)
    PSR_Assets_CommunityDistrict = f"{output}/PSR_Assets_CommunityDistrict"
    arcpy.analysis.SpatialJoin(
        target_features=PSR_Assets_500ftBuffer, 
        join_features=communityDistrict, 
        out_feature_class=PSR_Assets_CommunityDistrict, 
        join_operation="JOIN_ONE_TO_MANY", 
        join_type="KEEP_COMMON", 
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_500ftBuffer},KEY_ASSET,-1,-1; Dist_ID \"Dist_ID \" true true false 10 Long 0 0,First,#,{communityDistrict}, BoroCD,-1,-1",
        match_option="INTERSECT", 
        search_radius="", 
        distance_field_name=""
    )
    
    # Process: Spatial Join for Congressional District (Spatial Join) (analysis)
    PSR_Assets_CongressionalDistrict = f"{output}/PSR_Assets_CongressionalDistrict"
    arcpy.analysis.SpatialJoin(
        target_features=PSR_Assets_500ftBuffer, 
        join_features=congressionalDistrict, 
        out_feature_class=PSR_Assets_CongressionalDistrict, 
        join_operation="JOIN_ONE_TO_MANY", 
        join_type="KEEP_COMMON", 
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_500ftBuffer},KEY_ASSET,-1,-1; Dist_ID \"Dist_ID \" true true false 10 Long 0 0,First,#,{congressionalDistrict}, CongDist,-1,-1",
        match_option="INTERSECT", 
        search_radius = "", 
        distance_field_name = ""
    )
    
    # Process: Spatial Join for State Assembly (Spatial Join) (analysis)
    PSR_Assets_StateAssembly = f"{output}/PSR_Assets_StateAssembly"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_500ftBuffer, 
        join_features = stateAssembly, 
        out_feature_class=PSR_Assets_StateAssembly, 
        join_operation = "JOIN_ONE_TO_MANY", 
        join_type = "KEEP_COMMON", 
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_500ftBuffer},KEY_ASSET,-1,-1; Dist_ID \"Dist_ID \" true true false 10 Long 0 0,First,#,{stateAssembly}, AssemDist,-1,-1",
        match_option = "INTERSECT", 
        search_radius = "", 
        distance_field_name = ""
    )
    
    # Process: Spatial Join for State Senate (Spatial Join) (analysis)
    PSR_Assets_StateSenate = f"{output}/PSR_Assets_StateSenate"
    arcpy.analysis.SpatialJoin(
        target_features = PSR_Assets_500ftBuffer, 
        join_features = stateSenate, 
        out_feature_class = PSR_Assets_StateSenate, 
        join_operation = "JOIN_ONE_TO_MANY", 
        join_type = "KEEP_COMMON", 
        field_mapping = f"KEY_ASSET \"KEY_ASSET\" true true false 4 Long 0 0,First,#,{PSR_Assets_500ftBuffer},KEY_ASSET,-1,-1; Dist_ID \"Dist_ID \" true true false 10 Long 0 0,First,#,{stateSenate}, StSenDist,-1,-1",
        match_option = "INTERSECT", 
        search_radius = "", 
        distance_field_name = ""
    )

    # # Process: Spatial Join for Counties (Spatial Join) (analysis)
    # PSR_Assets_Counties = f"{output}/PSR_Assets_Counties"
    # arcpy.analysis.SpatialJoin(
    #     target_features=PSR_Assets_500ftBuffer,
    #     join_features=counties,
    #     out_feature_class=PSR_Assets_Counties,
    #     join_operation="JOIN_ONE_TO_MANY",
    #     join_type="KEEP_COMMON",
    #     field_mapping='KEY_ASSET " KEY_ASSET " true true false 4 Long 0 0,First,#,{PSR_Assets_500ftBuffer},KEY_ASSET,-1,-1;county_name "county_name" true true false 100 Text 0 0,First,#,{counties},NAMELSAD,0,99;',
    #     match_option="INTERSECT",
    #     search_radius=None,
    #     distance_field_name="",
    #     match_fields=None
    # )

    # # Process: Spatial Join for cities (Spatial Join) (analysis)
    # PSR_Assets_citiesAndTowns = f"{output}/PSR_Assets_citiesAndTowns"
    # arcpy.analysis.SpatialJoin(
    #     target_features=PSR_Assets_500ftBuffer,
    #     join_features=cities_towns,
    #     out_feature_class=PSR_Assets_citiesAndTowns,
    #     join_operation="JOIN_ONE_TO_MANY",
    #     join_type="KEEP_COMMON",
    #     field_mapping='KEY_ASSET " KEY_ASSET " true true false 4 Long 0 0,First,#,{PSR_Assets_500ftBuffer},KEY_ASSET,-1,-1;city_name "city_name" true true false 100 Text 0 0,First,#,{cities_towns},NAME,0,99;',
    #     match_option="INTERSECT",
    #     search_radius=None,
    #     distance_field_name="",
    #     match_fields=None
    # )
    

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace = fr"{output_dir}", 
                          workspace = fr"{output_dir}"):
        Model(*argv[1:])
    
    print(f"Spatial Join completed, please check the output results and proceed to next step.")

# creating a function to sort the concatenated strings
def sort_dist_str(dist_str):
    
    # assigning comma to a variable
    delim = ','    
    
    # turning the input into a list, and then sorting it, and then converting it back to comma separated text string.
    return delim.join([str(x) for x in sorted([int(x) for x in dist_str.split(delim)])])


# creating a function that lists district IDs that only exist in PSR or analysis result field.
def check_diff(psr, result):
    delim = ','
    psr_np = np.array([psr.split(delim)])
    result_np = np.array([result.split(delim)])
    diff_np = np.setxor1d(psr_np, result_np)
    diff = delim.join(diff_np)
    return(diff)


# defining function to combine individual rows of spatial join intersect results from the previous into a concatenated list of string separated by comma (same as PSR).
# afterwards, convert the string into array and compare for differences.

#note that the beginning of this function only deals with the political districts, which have a specific ID integer to identify them with. City and county data is added on at the end of the function.

def transform_rows(assets_table = f"{output_dir}/PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties_cities",
                   cityCouncil_table = f"{output_dir}/PSR_Assets_CityCouncil",
                   communityDist_table = f"{output_dir}/PSR_Assets_CommunityDistrict",
                   congressional_table = f"{output_dir}/PSR_Assets_CongressionalDistrict",
                   stateAssembly_table = f"{output_dir}/PSR_Assets_StateAssembly",
                   stateSenate_table = f"{output_dir}/PSR_Assets_StateSenate",
                   excel_output = excel_output_dir
                  ):
    
    # read the original assets list in to Pandas Dataframe
    assets_columns = [f.name for f in arcpy.ListFields(assets_table) if f.type != "Geometry"]
    assets = pd.DataFrame(data = arcpy.da.SearchCursor(assets_table, assets_columns), columns = assets_columns)
    
    # drop all other columns and keep only columns of Key Asset and districts
    assets = assets[['KEY_ASSET' 
                     ,'DIST_CITY_COUNCIL', 'CityCouncil_Parent_Dist_ID'
                     , 'DIST_COMMUNITY', 'CommunityDistrict_Parent_Dist_ID'
                     , 'DIST_CONGRESSIONAL', 'CongressionalDistrict_Parent_Dist_ID'
                     , 'DIST_STATE_ASSEMBLY', 'StateAssembly_Parent_Dist_ID'
                     , 'DIST_STATE_SENATE', 'StateSenate_Parent_Dist_ID']]
    
    # change data type of KEY_ASSET column to string.
    assets['KEY_ASSET'] = assets['KEY_ASSET'].astype(str)
    
    # # initiating a column to flag overall changes for an asset
    assets['overall_flag'] = "NO UPDATE"
    
    
    # convert the individual district IDs, in string, into a concatenated list (comma separated) to each asset ID in a for loop which iterates through the 5 spatial join output feature class from previous step.
    for i in [[cityCouncil_table, 'DIST_CITY_COUNCIL'], 
              [communityDist_table, 'DIST_COMMUNITY'], 
              [congressional_table, 'DIST_CONGRESSIONAL'], 
              [stateAssembly_table, 'DIST_STATE_ASSEMBLY'], 
              [stateSenate_table, 'DIST_STATE_SENATE']]:
        
        # get the name of current type of district
        i_name = i[0].split('gdb/PSR_Assets_', 1)[-1]
        
        # place the table from feature class into pandas Dataframe.
        i_columns = [f.name for f in arcpy.ListFields(i[0]) if f.type != "Geometry"]
        i_df = pd.DataFrame(data = arcpy.da.SearchCursor(i[0], i_columns), columns = i_columns)
        
        # change data type of the district ID to INT first to get rid of the decimals and then convert back to string
        i_df['Dist_ID'] = i_df['Dist_ID'].astype(int).astype(str)
        
        # creating a new column which generates a comma separated list of all district IDs associated to the individual record of asset key.
        i_df[f'{i_name}_Dist_ID'] = i_df.groupby('KEY_ASSET')['Dist_ID'].transform(lambda x : ','.join(x))
        
        # removes all other columns except for Key asset and duplicated rows.
        i_df = i_df[['KEY_ASSET', f'{i_name}_Dist_ID']].drop_duplicates()
        
        # convert the key asset column from spatial join result to a string data type
        i_df['KEY_ASSET'] = i_df['KEY_ASSET'].astype(str)
        
        # running through each row and sorting the comma separated list.
        for a in i_df.index:
            i_df[f'{i_name}_Dist_ID'][a] = sort_dist_str(i_df[f'{i_name}_Dist_ID'][a])
        
        # use Merge function to join the asset DF and district DF
        assets = assets.merge(i_df, how = 'outer', left_on = "KEY_ASSET", right_on = "KEY_ASSET" )
        
        # # creating a new flag column for comparison result
        assets[f'{i_name}_flag'] = ""
        
        # # creating a new column to save the difference 
        # assets[f'{i_name}_diff'] = ""
        
        #creating a new column for extended districts
        # assets[f'{i_name}_extended'] = ""

        #creating a new column for when the asset was last updated
        assets[f'{i_name}_lastUpdated'] = ""
        
        # for loop to compare PSR districts, assign flag, label the differences.
        for a in assets.index:
            
            # if PSR districts and result are the same, assign "NO UPDATE" to the district flag.
            if assets[i[1]][a] == assets[f'{i_name}_Dist_ID'][a]:
                assets[f'{i_name}_flag'][a] = "NO UPDATE"
            
            # if both PSR district and result are null, label "NO UPDATE" to the flag.
            elif pd.isnull(assets[i[1]][a]) and pd.isnull(assets[f'{i_name}_Dist_ID'][a]):
                assets[f'{i_name}_flag'][a] = "NO UPDATE"
            
            # if PSR district is null, and result is not, assign "UPDATED (with districts added). Record the differences between both columns. And mark the overall_flag to "UPDATED"
            elif pd.isnull(assets[i[1]][a]) and pd.isnull(assets[f'{i_name}_Dist_ID'][a]) == False:
                assets[f'{i_name}_flag'][a] = "UPDATED (with districts added)"
                # assets[f'{i_name}_diff'][a] = assets[f'{i_name}_Dist_ID'][a]
                assets['overall_flag'][a] = "UPDATED"
                assets[f'{i_name}_lastUpdated'][a]  = pd.Timestamp.today().strftime('%Y-%m-%d')
            
            # if PSR district is not null, and result, assign "REMOVED". Record the differences between both columns. And mark the overall_flag to "UPDATED"
            elif pd.isnull(assets[i[1]][a]) == False and pd.isnull(assets[f'{i_name}_Dist_ID'][a]):
                assets[f'{i_name}_flag'][a] = "REMOVED"
                # assets[f'{i_name}_diff'][a] = check_diff(str(assets[i[1]][a]), str(assets[f'{i_name}_Dist_ID'][a]))
                assets['overall_flag'][a] = "UPDATED"
                assets[f'{i_name}_lastUpdated'][a]  = pd.Timestamp.today().strftime('%Y-%m-%d')
            
            # if the number of districts in PSR is more than the number of districts from analysis results, assign "UPDATED (with districts removed)", record the differences between both columns. And mark the overall_flag to "UPDATED"
            elif str(assets[i[1]][a]).count(',') > str(assets[f'{i_name}_Dist_ID'][a]).count(','):
                assets[f'{i_name}_flag'][a] = "UPDATED (with districts removed)"
                # assets[f'{i_name}_diff'][a] = check_diff(str(assets[i[1]][a]), str(assets[f'{i_name}_Dist_ID'][a]))
                assets['overall_flag'][a] = "UPDATED"
                assets[f'{i_name}_lastUpdated'][a]  = pd.Timestamp.today().strftime('%Y-%m-%d')
            
            # if the number of districts in PSR is less than the number of districts from analysis results, assign "UPDATED (with districts added)", record the differences between both columns. And mark the overall_flag to "UPDATED"
            elif str(assets[f'{i_name}_Dist_ID'][a]).count(',') > str(assets[i[1]][a]).count(','):
                assets[f'{i_name}_flag'][a] = "UPDATED (with districts added)"
                # assets[f'{i_name}_diff'][a] = check_diff(str(assets[i[1]][a]), str(assets[f'{i_name}_Dist_ID'][a]))
                assets['overall_flag'][a] = "UPDATED"
                assets[f'{i_name}_lastUpdated'][a]  = pd.Timestamp.today().strftime('%Y-%m-%d')
            
            #
            else:
                assets[f'{i_name}_flag'][a] = "UPDATED"
                # assets[f'{i_name}_diff'][a] = check_diff(str(assets[i[1]][a]), str(assets[f'{i_name}_Dist_ID'][a]))
                assets['overall_flag'][a] = "UPDATED"
                assets[f'{i_name}_lastUpdated'][a]  = pd.Timestamp.today().strftime('%Y-%m-%d')
    
    # rearrange the assets dataframe columns
    assets = assets[['KEY_ASSET',
                     'DIST_CITY_COUNCIL', 'CityCouncil_Parent_Dist_ID', 'CityCouncil_Dist_ID', 'CityCouncil_lastUpdated',
                     'DIST_COMMUNITY', 'CommunityDistrict_Parent_Dist_ID', 'CommunityDistrict_Dist_ID', 'CommunityDistrict_lastUpdated',
                     'DIST_CONGRESSIONAL', 'CongressionalDistrict_Parent_Dist_ID', 'CongressionalDistrict_Dist_ID', 'CongressionalDistrict_lastUpdated',
                     'DIST_STATE_ASSEMBLY', 'StateAssembly_Parent_Dist_ID', 'StateAssembly_Dist_ID', 'StateAssembly_lastUpdated',
                     'DIST_STATE_SENATE', 'StateSenate_Parent_Dist_ID', 'StateSenate_Dist_ID', 'StateSenate_lastUpdated']]
    

    #bring in counties and cities
    citiesAndCounties = f"{output_dir}/PSR_Assets_Parent_CC_CM_CO_SA_SS_NYcounties_cities"

    #turn counties and cities shapefile into a pandas df
    cols = [f.name for f in arcpy.ListFields(citiesAndCounties) if f.type != "Geometry"]
    cityCountiesFull = pd.DataFrame(data = arcpy.da.SearchCursor(citiesAndCounties, cols), columns = cols)
    city_and_county = cityCountiesFull[['KEY_ASSET', 'county_name', 'city_name']].drop_duplicates()
    city_and_county['KEY_ASSET'] = city_and_county['KEY_ASSET'].apply(lambda x: str(x))

    #join city and county data to the asset data with political districts
    finalDF = assets.merge(city_and_county, how = 'inner', left_on = "KEY_ASSET", right_on = "KEY_ASSET" )

    # export to excel
    finalDF.to_excel(fr"{excel_output}/PSR_Assets_District_Join_Result.xlsx")


if __name__ == '__main__':
    transform_rows()






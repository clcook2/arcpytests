import arcpy
from arcpy import env
from arcpy.sa import ExtractValuesToPoints, ExtractMultiValuesToPoints
import pandas as pd
from pathlib import Path
from arcpy.sa import *
import glob
import os
#import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Check for the ArcGIS license required to use tools in the 'Spatial Analyst' toolbox
    arcpy.CheckOutExtension("Spatial")

    # Set workspace using the arcpy 'workspace' method. This is where input shapefiles (line features) are located.
    arcpy.env.workspace = r"C:\Users\clcook2\Documents\SMAPVEX\LAI_Sentinel2_Python_Processing\shp\MA"

    #rasl = arcpy.ListRasters()

    # Make a list of all shapefiles in the above workspace
    shapefile = r"C:\Users\clcook2\Documents\SMAPVEX\LAI_Sentinel2_Python_Processing\shp\MA\SMAPVEX_LAI_SurveyArea_MA_proj.shp"#arcpy.ListFeatureClasses()

    # Set the folder path containing all input rasters to be analyzed
    rasters = Path(r"C:\Users\clcook2\Documents\SMAPVEX\LAI_Sentinel2_Python_Processing\shp\MA")
    rast_path_str = str(rasters)

    # Set output folder path
    out_folder = r"C:\Users\clcook2\Documents\SMAPVEX\LAI_Sentinel2_Python_Processing\output"
    out_folder_str = str(out_folder)
    #plot_output = Path(r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Analysis\Profiles\output_plots")

    # Output table to store the summary statistics
    #output_table = "summary_stats.dbf"

    # Field in the shapefile that will be used as the zone field
    zone_field = "SiteID"

    # List of statistics to calculate (you can customize this list)
    statistics_type = ["MINIMUM", "MAXIMUM", "MEAN", "STD"]

    try:

        raster_layers = arcpy.ListRasters()

        for raster in raster_layers:
            #raster_name = os.path.basename(raster).rstrip(os.path.splitext(raster)[1])
            # Output table to store the summary statistics
            output_table = out_folder_str + "\\" + raster[:-4] + "_TBL.dbf"

            # Perform zonal statistics
            out_table = ZonalStatisticsAsTable(shapefile, zone_field, raster, output_table, "DATA", "ALL")
            out_table_path = str(out_table)
            #csv_file = os.path.join(out_table_path + ".csv")

            #arcpy.TableToTable_conversion(out_table_path, arcpy.env.workspace, out_table_path + ".csv")

            print(f"Summary statistics for {raster} have been calculated and saved to:", out_table)


    except Exception as e:
        print("An error occurred:", str(e))


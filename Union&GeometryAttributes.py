import arcpy
from arcpy import env
#from arcpy.sa import ExtractValuesToPoints
#import pandas as pd
import os
from pathlib import Path



if __name__ == "__main__":
    # Check for the ArcGIS license required to use tools in the 'Spatial Analyst' toolbox
    arcpy.CheckOutExtension("Spatial")

    # Set workspace using the arcpy 'workspace' method
    env.workspace = r"C:\Users\clcook2\Documents\NASA_CCS\ArcpyScript_Test"

    # Make a list of all shapefiles in the above workspace
    shapefiles = arcpy.ListFeatureClasses()

    # Set output folder path
    out_folder = Path(r"C:\Users\clcook2\Documents\NASA_CCS\ArcpyScript_Test\Output")
    out_folder_str = str(out_folder)

    for shapefile in shapefiles:
        output_file = os.path.join(out_folder, os.path.basename(shapefile) + "_union")
        #arcpy.management.CalculateGeometryAttributes(shapefile,["PERIM_LEN", "PERIMETER_LENGTH"])
        arcpy.analysis.Union(shapefile, output_file)
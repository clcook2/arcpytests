import arcpy
from arcpy import env
from arcpy.sa import *
env.workspace = "F:/lu_crop_rast"
arcpy.env.overwriteoutput = 1

watershedFeat = "F:/watersheds.shp"
outDir = "F:/lu_crop_rast/tables/"

for raster in arcpy.ListRasters():
    outTable = outDir + raster + "_TBL.dbf"
    arcpy.sa.ZonalStatisticsAsTable(watershedFeat,"Name",raster,outTable,"NODATA","MEAN")
import arcpy
from arcpy import env
from arcpy.sa import ExtractValuesToPoints, ExtractMultiValuesToPoints
import pandas as pd
from pathlib import Path
import glob
import os
import matplotlib.pyplot as plt


def plotting_function(names):
    fig, axs = plt.subplots(nrows=len(names), figsize=(12, 6 * len(names)))
    df_list = []
    for file in names:
        df = pd.read_csv(file, index_col=None, header = 0, usecols=['New_Dist','Elevation', 'Moving_Average', 'LBhumped'])
        df_list.append(df)
    for i, df in enumerate(df_list):
        # Plot first subplot
        #axs[i, 0].plot(df['New_Dist'], df['RASTERVALU'])
        #axs[i, 0].set_xlabel('Distance (m)')
        #axs[i, 0].set_ylabel('Elevation (m)')
        #axs[i, 0].set_title(f'Dataframe {i+1}')
        # Plot second subplot
        axs[i].scatter(df['New_Dist'], df['Elevation'], label='Elevation', s=6)
        axs[i].set_xlabel('Distance (m)', fontsize=20)
        axs[i].set_ylabel('Elevation (m)', fontsize=20)
        axs[i].twinx().scatter(df['New_Dist'], df['Moving_Average'], color='black', label='Percent Grade Moving Average', s=6)
        axs[i].fill_between(df['New_Dist'], df['Elevation'], y2=min(df['Elevation']), where=(df['LBhumped']>0),facecolor='red', alpha = 0.2)
        #axs[i].legend(loc="upper center")
        #axs[i, 0].twinx().set_ylabel('Percent Grade Moving Average (%)')
    plt.tight_layout()
    #plt.show()
    plt.savefig((Path.joinpath(plot_output, Path(names[0]).stem + '_figure1.png')))


# def plotting_function(names):
#     num_plots = len(names) + 1
#     fig, ax = plt.subplots(num_plots, 1)#len(names)+1
#     df_list = []
#     for file in names:
#         df = pd.read_csv(file, index_col=None, header = 0, usecols=['New_Dist','RASTERVALU', 'Moving_Average'])
#         df_list.append(df)
#     accum = 0
#     for dframe in df_list:
#         if accum == 0:
#             ax = dframe.plot('New_Dist','RASTERVALU')
#             #ax = dframe.plot()
#             accum = accum + 1
#
#         else:
#             dframe.plot('New_Dist','RASTERVALU', ax=ax)
#             accum = accum + 1
#             if accum == len(names):
#                 plt.savefig((Path.joinpath(plot_output,'figure1.png')))
#     for dframe in df_list:


if __name__ == "__main__":
    # Check for the ArcGIS license required to use tools in the 'Spatial Analyst' toolbox
    arcpy.CheckOutExtension("Spatial")

    # Set workspace using the arcpy 'workspace' method. This is where input shapefiles (line features) are located.
    env.workspace = r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Analysis\Profiles\input_shapefiles"

    # Make a list of all shapefiles in the above workspace
    shapefiles = arcpy.ListFeatureClasses()

    # Set the folder path containing all input DEMs to be analyzed
    dems = Path(r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Agisoft\20210407_LSRCsites_Milford_to_BayCity\Outputs")

    # Set the folder path containing all input humped crossing results ("BAD MASK") to be analyzed
    humped = Path(r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Analysis\Profiles\input_badmasks")

    # Set output folder path
    out_folder = Path(r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Analysis\Profiles\output")
    out_folder_str = str(out_folder)
    plot_output = Path(r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Analysis\Profiles\output_plots")

    # Set the distance interval at which to generate points along lines in the shapefiles
    dist = '0.1016 meters'
    dist_float = dist.split(" ")
    dist_float = float(dist_float[0])

    # Clear the output folder prior to generating output (in case data remains from a previous run of this script)
    for file_path in out_folder.iterdir():
        if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
            file_path.unlink()

    # Set folder path that will later contain temporary shapefiles 'genpoints.shp'
    temp_folder = Path(r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Analysis\Profiles\temp")

    # Delete any existing files in the temporary folder path prior to initializing the empty point shapefiles (in case data remains from a previous run of this script)
    for file_path in temp_folder.glob("*"):
        if file_path.is_file():
            file_path.unlink()


    # Iterating over the shapefiles, generate points along the shapefile,
    # extract elevation data to those points, and then output these values in a csv for each shapefile.
    for shapefile in shapefiles:

        # determine the proper raster name based on the input shapefile name
        rastname = shapefile[:-4] + ".tif"
        rastpath = Path.joinpath(dems, rastname)
        rastpath_str = str(rastpath)

        # determine the proper humped crossing result raster name based on the input shapefile name
        humpname = shapefile[:-7] + "HEIGHT_BAD_MASK_LOWBOY_RESAMPLE.TIF"
        humppath = Path.joinpath(humped, humpname)
        humppath_str = str(humppath)


        # Provide paths for the temporary shapefiles that will contain the outputs from processing using the next several tools
        temp_out_genpoints = r"Y:\gis_lab\project\MTRI_Inc\USDOT_DroneBasedGradeCrossings\Analysis\Profiles\temp\genpoints.shp"
        #temp_out_extractpoints = r"J:\project\MTRAC_Crossingi\Analysis\20230426_Ohio_Crossings\Profiles\temp\extractpoints.shp"
        #temp_out_extractpoints2 = r"J:\project\MTRAC_Crossingi\Analysis\20230426_Ohio_Crossings\Profiles\temp\extractpoints2.shp"

        # create points every four inches along the lines of the input shapefile and make a temporary point shapefile
        arcpy.management.GeneratePointsAlongLines(shapefile, temp_out_genpoints, 'DISTANCE', Distance=dist)

        # create a new field and calculate the cumulative distance for each point
        arcpy.AddField_management(temp_out_genpoints, "Distance", "FLOAT")
        expression = "!FID! * {}".format(dist_float)
        arcpy.CalculateField_management(temp_out_genpoints, "Distance", expression, "PYTHON")
        #arcpy.AddField_management(temp_out_genpoints, "Sorter1", "LONG")
        #arcpy.CalculateField_management(temp_out_genpoints, "Sorter1", "!FID!")

        # use the point shapefile to extract elevation data from the specified DEM, then change the field name from the default to 'Elevation'
        if os.path.exists(humppath):
            ExtractMultiValuesToPoints(temp_out_genpoints, [[humppath_str, "LBhumped"], [rastpath_str, "Elevation"]])
        else:
            ExtractMultiValuesToPoints(temp_out_genpoints, [[rastpath_str, "Elevation"]])
            arcpy.AddField_management(temp_out_genpoints, "LBhumped", "FLOAT")
            arcpy.CalculateField_management(temp_out_genpoints, "LBhumped", "-9999")

        # save the attribute data of the shapefile to xlsx, and then create a csv using pandas
        out_csv = Path.joinpath(out_folder, shapefile[:-4] + ".xlsx")
        out_csv_str = str(out_csv)
        arcpy.conversion.TableToExcel(temp_out_genpoints, out_csv_str)
        read_file = pd.read_excel(out_csv)
        read_file.to_csv(out_csv_str[:-5] + ".csv")

        # delete the temporary shapefiles that are no longer needed
        for file_path in temp_folder.glob("*"):
            if file_path.is_file():
                file_path.unlink()

        # delete the temporary .xlsx files that are no longer needed
        for file_path in out_folder.iterdir():
            if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
                file_path.unlink()

    # Use glob to get a list of all CSV files in the output directory
    csv_files = glob.glob(out_folder_str + "\\" + "*.csv")

    # Iterate over each CSV file, sort the csv, and create a new csv for each line present in the original csv
    for file in csv_files:
        # Read the CSV file into a pandas dataframe
        df = pd.read_csv(file)

        # Sort the csv by the ORIG_FID field and then the distance field
        df = df.sort_values('ORIG_FID')
        df = df.sort_values('Distance')

        # Find the number of unique lines within the csv using the ORIG_FID field
        unique_lines = df["ORIG_FID"].unique()

        # For each unique line, create a new csv
        for line_num in unique_lines:
            filtered_df = df[df['ORIG_FID'] == line_num]
            filtered_df.to_csv(file[:-4] + '_sorted_' + str(line_num) + '.csv')

        # Delete our no longer needed, unsorted, csv file
        Path(file).unlink()

    # Again use glob to get a list of all CSV files in the output directory
    csv_files = glob.glob(out_folder_str + "\\" + "*.csv")

    # Iterate over each csv file, create the field 'New_Dist', and calculate the distance in this new field
    for file in csv_files:
        df = pd.read_csv(file)
        df['New_Dist'] = df['Distance'] - df['Distance'].min()
        df['Delta_Elevation'] = df['Elevation'].diff(periods=-(round((1/dist_float)))).shift(round(0.5/dist_float))
        df['Delta_Distance'] = df['New_Dist'].diff(periods=-(round((1/dist_float)))).shift(round(0.5/dist_float))
        df['Percent_Grade'] = (df['Delta_Elevation'] / df['Delta_Distance']) * 100
        df['Moving_Average'] = df['Percent_Grade'].rolling(window=(round((1/dist_float))+(1-(round(1/dist_float))%2)), center=True).mean()
        df.to_csv(file[:-4] + '_final.csv')

        # Delete our no longer needed previous csv file
        Path(file).unlink()

    # Again use glob to get a list of all CSV files in the output directory
    csv_files = glob.glob(out_folder_str + "\\" + "*.csv")

    first = True
    listoflists = []
    names = []
    count = 0
    count2 = 0
    for csv in csv_files:
        count += 1
    for csv in csv_files:
        count2 += 1
        file = Path(csv)
        filename = file.name
        if first == True:
            past_csv = filename[0:16]
            names.append(csv)
            first = False
        else:
            if filename[0:16] == past_csv:
                names.append(csv)
                if count2 == count:
                    listoflists.append(names)
                    plotting_function(names)
            else:
                listoflists.append(names)
                plotting_function(names)
                names.clear()
                names.append(csv)
            past_csv = filename[0:16]



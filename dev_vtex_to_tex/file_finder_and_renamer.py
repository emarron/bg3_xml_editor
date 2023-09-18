# given vtexbank info:
# read csv format [gtex, id, name, count]
# find gtex + count, from "C:\Users\emar\AppData\Local\Larian Studios\BG3_modding_tools\bg3-modders-multitool\UnpackedData\VirtualTextures\Generated\Public\VirtualTextures"
# rename to name + count(associated dict name) and output to ".Generated/kartoffels_clubhouse/Textures/"

import os
import csv
import shutil

# Define the dictionary of texture suffixes
texture_suffix_list = ["_BM", "_NM", "_PM"]

# Path to the CSV file
csv_file_path = "g_tex_filenames.csv"

# Directory where the texture files are located
source_directory = "C:\\Users\\emar\\AppData\\Local\\Larian Studios\\BG3_modding_tools\\bg3-modders-multitool\\UnpackedData\\VirtualTextures\\Generated\\Public\\VirtualTextures\\source\\"

# Output directory for renamed texture files
output_directory = './Generated/Public/Shared/Assets/kartoffels_clubhouse/Textures/'

# Read and process the CSV file
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header

    for row in csv_reader:
        gtex_filename = row[0]
        name = row[2]
        count = int(row[3])
        for i in range(count):
        # Construct the new filename using the provided dictionary
            new_filename = f"{name}{texture_suffix_list[i]}.dds"

            # Source and destination paths for the texture file
            try:
                source_path = os.path.join(source_directory, gtex_filename + "_" + str(i) +
                                           ".dds")
                destination_path = os.path.join(output_directory, new_filename)

                # Rename and copy the texture file to the output directory
                shutil.copy(source_path, destination_path)
                print(f"Renamed and copied {source_path} to {destination_path}")
            except FileNotFoundError:
                print(f">>>FAILED TO COPY {source_path} to {destination_path}")


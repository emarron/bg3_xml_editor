import os
import shutil
import xml.etree.ElementTree as ET

# Define the XML file path
xml_file = 'texture.xml'
# Define the destination folder
destination_folder = 'foo'

# Parse the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Iterate through each 'node' element
for node in root.findall('.//node'):
    # Find the 'attribute' element with id="SourceFile"
    source_file_elem = node.find(".//attribute[@id='SourceFile']")
    
    if source_file_elem is not None:
        source_file_value = source_file_elem.get('value')
        source_file_path = os.path.join(os.path.dirname(xml_file), source_file_value)
        
        # Check if the source file exists
        if os.path.exists(source_file_path):
            # Create the destination directory if it doesn't exist
            os.makedirs(destination_folder, exist_ok=True)
            
            # Copy the source file to the destination folder
            shutil.copy(source_file_path, os.path.join(destination_folder, os.path.basename(source_file_value)))
            # print(f"Copied: {source_file_path} to {destination_folder}")
        else:
            print(f"Source file does not exist: {source_file_path}")

print("Finished copying files.")

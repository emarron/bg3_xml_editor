import csv
import xml.etree.ElementTree as ET

# ID: used by the material resource to uniquely identify the virtual texture node
# GTex: used by the virtual texture resource to uniquely identify the virtual texture file
# Name: probably for internal sorting, matches the Name in the material resource.

#output: csv_filename, usually "g_tex_filenames.csv" used by "file_finder_and_readnamer.py"

# Load and parse the XML file
tree = ET.parse('SharedDev/Content/Assets/Characters/_merged.lsx')
root = tree.getroot()

# Find the region with id="VirtualTextureBank"
virtual_texture_bank_region = root.find(".//region[@id='VirtualTextureBank']")

if virtual_texture_bank_region is not None:
    resource_nodes = virtual_texture_bank_region.findall(".//node[@id='Resource']")

    print("List of Resource Attributes:")
    csv_filename = 'g_tex_filenames.csv'
      # Write header

    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['GTexFileName', 'ID', 'Name', 'VirtualTextureLayerConfig'])
        for resource_node in resource_nodes:
            g_tex_file_name = resource_node.find(".//attribute[@id='GTexFileName']").get("value")
            resource_id = resource_node.find(".//attribute[@id='ID']").get("value")
            name = resource_node.find(".//attribute[@id='Name']").get("value")
            v_tex_layer_config = resource_node.find(".//attribute[@id='VirtualTextureLayerConfig']").get("value")
            csv_writer.writerow([g_tex_file_name, resource_id, name, v_tex_layer_config])
            print("GTexFileName:", g_tex_file_name)
            print("ID:", resource_id)
            print("Name:", name)
            print("VirtualTextureLayerConfig:", v_tex_layer_config)
            print()


else:
    print("VirtualTextureBank region not found in the XML.")

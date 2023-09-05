import xml.etree.ElementTree as ET

# ID: used by the material resource to uniquely identify the virtual texture node
# GTex: used by the virtual texture resource to uniquely identify the virtual texture file
# Name: probably for internal sorting, matches the Name in the material resource.

# Load and parse the XML file
tree = ET.parse('Characters/Humans/[PAK]_Female_Armor/_merged.lsx')
root = tree.getroot()

# Find the region with id="VirtualTextureBank"
virtual_texture_bank_region = root.find(".//region[@id='VirtualTextureBank']")

if virtual_texture_bank_region is not None:
    resource_nodes = virtual_texture_bank_region.findall(".//node[@id='Resource']")

    print("List of Resource Attributes:")
    for resource_node in resource_nodes:
        g_tex_file_name = resource_node.find(".//attribute[@id='GTexFileName']").get("value")
        resource_id = resource_node.find(".//attribute[@id='ID']").get("value")
        name = resource_node.find(".//attribute[@id='Name']").get("value")

        print("GTexFileName:", g_tex_file_name)
        print("ID:", resource_id)
        print("Name:", name)
        print()
else:
    print("VirtualTextureBank region not found in the XML.")

import xml.etree.ElementTree as ET


# Function to extract VirtualTextureParameters IDs and Resource Name from a given XML element
def extract_virtual_texture_info(resource_node):
    virtual_texture_info = []

    resource_name = resource_node.find(".//attribute[@id='Name']").get("value")
    virtual_texture_ids = []

    for virtual_texture_node in resource_node.findall(".//node[@id='VirtualTextureParameters']"):
        attribute_id = virtual_texture_node.find(".//attribute[@id='ID']")
        if attribute_id is not None:
            virtual_texture_ids.append(attribute_id.get("value"))

    if virtual_texture_ids:
        virtual_texture_info.append((resource_name, virtual_texture_ids))

    return virtual_texture_info


# Load and parse the XML file
tree = ET.parse('_merged.lsx')
root = tree.getroot()

# Find the region with id="MaterialBank"
material_bank_region = root.find(".//region[@id='MaterialBank']")

if material_bank_region is not None:
    virtual_texture_info_list = []

    # Find nodes with id="Resource" within the MaterialBank region
    resource_nodes = material_bank_region.findall(".//node[@id='Resource']")

    # Iterate through each Resource node
    for resource_node in resource_nodes:
        # Check if the Resource node contains VirtualTextureParameters
        virtual_texture_info_list.extend(extract_virtual_texture_info(resource_node))

    print("List of VirtualTextureParameters IDs and corresponding Resource Names:")
    for resource_name, virtual_texture_ids in virtual_texture_info_list:
        print("Resource Name:", resource_name)
        print("VirtualTextureParameters IDs:", virtual_texture_ids)
        print()
else:
    print("MaterialBank region not found in the XML.")

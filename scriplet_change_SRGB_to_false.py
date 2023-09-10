import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('texture.xml')
root = tree.getroot()

# Find all nodes with id="Resource"
resource_nodes = root.findall('.//node[@id="Resource"]')

# Iterate through each "Resource" node
for resource_node in resource_nodes:
    # Find the "Name" attribute
    name_attr = resource_node.find('.//attribute[@id="Name"]')
    
    # Find the "SRGB" attribute
    srgb_attr = resource_node.find('.//attribute[@id="SRGB"]')
    
    # Check if the "Name" attribute's value contains "_PM"
    if name_attr is not None and "_PM" in name_attr.get('value'):
        # Set the "SRGB" attribute's value to "False"
        if srgb_attr is not None:
            srgb_attr.set('value', 'False')

# Save the modified XML back to a file
tree.write('modified_merged.lsx')

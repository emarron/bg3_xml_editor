import xml.etree.ElementTree as ET

# Parse the first XML file
tree1 = ET.parse('[PAK]_vtex_to_tex/male/_merged.lsx')
root1 = tree1.getroot()

# Merge MaterialBank section
materialbank_children_tag1 = root1.find(".//node[@id='MaterialBank']/children")
tree2 = ET.parse('[PAK]_vtex_to_tex/female/_merged.lsx')
root2 = tree2.getroot()
materialbank_children_tag2 = root2.find(".//node[@id='MaterialBank']/children")
for resource_node in materialbank_children_tag2.findall(".//node[@id='Resource']"):
    materialbank_children_tag1.append(resource_node)

# Parse the second XML file again for TextureBank

# Merge TextureBank section
texturebank_tag1 = root1.find(".//node[@id='TextureBank']")
texturebank_tag2 = root2.find(".//node[@id='TextureBank']")
for resource_node in texturebank_tag2.findall(".//node[@id='Resource']"):
    texturebank_tag1.append(resource_node)

# Save the merged XML content to a new file
tree1.write('merged.xml', encoding="utf-8", xml_declaration=True)

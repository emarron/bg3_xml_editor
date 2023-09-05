import xml.etree.ElementTree as ET

# Load and parse the XML file
tree = ET.parse('Characters/Humans/[PAK]_Female_Armor/_merged.lsx')

root = tree.getroot()

# Create a new XML structure for modified resources
new_root = ET.Element("root")

# Find the region with id="MaterialBank"
material_bank_region = root.find(".//region[@id='MaterialBank']")

if material_bank_region is not None:
    # Iterate through each <node id="Resource"> element
    for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
        # Create a copy of the resource node
        modified_resource_node = ET.Element("node", id="Resource")

        # Iterate through child nodes of the original resource node
        for child_node in resource_node:
            # Skip <node id="VirtualTextureParameters"> elements
            if child_node.get("id") == "VirtualTextureParameters":
                continue

            # Create a copy of the child node and add it to the modified resource node
            modified_child_node = ET.Element(child_node.tag, attrib=child_node.attrib)
            for sub_child_node in child_node:
                modified_sub_child_node = ET.Element(sub_child_node.tag, attrib=sub_child_node.attrib)
                modified_child_node.append(modified_sub_child_node)
            modified_resource_node.append(modified_child_node)

        # Append modified <node id="Resource"> to the new XML structure
        new_root.append(modified_resource_node)

    # Create a new XML tree from the modified root
    new_tree = ET.ElementTree(new_root)

    # Write modified XML structure to new.xml
    new_tree.write("new.xml", encoding="utf-8", xml_declaration=True)

    print("Modified XML written to 'new.xml'.")
else:
    print("MaterialBank region not found in the XML.")

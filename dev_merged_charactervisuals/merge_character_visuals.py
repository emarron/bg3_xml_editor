# program to merge character visual files
import xml.etree.ElementTree as ET
from pathlib import Path


def merge_xml_trees(tree1,tree2,output):
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    # Find the 'CharacterVisualBank' node in both XML documents
    character_visual_bank1 = root1.find(".//node[@id='CharacterVisualBank']")
    character_visual_bank1 = root1.find(".//node[@id='CharacterVisualBank']")
    character_visual_bank2 = root2.find(".//node[@id='CharacterVisualBank']")

    # Find all 'Resource' nodes under 'CharacterVisualBank' in both XML documents
    resource_nodes1 = character_visual_bank1.findall(".//node[@id='Resource']")
    resource_nodes2 = character_visual_bank2.findall(".//node[@id='Resource']")

    # Create a dictionary to store the 'Resource' nodes from the second XML document
    resource_nodes2_dict = {node.find(".//attribute[@id='ID']").get('value'): node for node in resource_nodes2}

    # Iterate over 'Resource' nodes in the first XML document
    for resource_node1 in resource_nodes1:
        # Get the 'ID' attribute value of the current 'Resource' node
        id_value = resource_node1.find(".//attribute[@id='ID']").get('value')
        
        # Check if the 'ID' value exists in the second XML document
        if id_value in resource_nodes2_dict:
            # Find the 'RealMaterialOverrides' node in the first and second 'Resource' nodes
            real_material_overrides1 = resource_node1.find(".//node[@id='RealMaterialOverrides']")
            real_material_overrides2 = resource_nodes2_dict[id_value].find(".//node[@id='RealMaterialOverrides']")
            
            # Find the <children> element under real_material_overrides1
            children1 = real_material_overrides1.find(".//children")
            
            # If <children> doesn't exist, create it
            if children1 is None:
                children1 = ET.Element("children")
                real_material_overrides1.append(children1)
            
            # Iterate over 'Object' nodes in real_material_overrides2 and append them to children1
            for obj_node2 in real_material_overrides2.findall(".//node[@id='Object']"):
                # Clone the 'Object' node from the second XML document
                obj_node1 = obj_node2
                children1.append(obj_node1)
                
    # Serialize the merged XML document
    merged_xml_content = ET.tostring(root1, encoding='utf-8').decode()

    merged_xml_content = ET.tostring(root1, encoding='utf-8').decode()

    # Save the merged XML content to the output file
    with open(output, "w") as merged_file:
        merged_file.write(merged_xml_content)


def merge_xml_files_in_dirs(dir1,dir2, output_dir):
        # Convert string paths to Path objects
    dir1 = Path(dir1)
    dir2 = Path(dir2)
    output_dir = Path(output_dir)
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterate over all XML files in dir1
    for file_path1 in dir1.glob("*.lsx"):
        # Check if the same file exists in dir2
        file_path2 = dir2 / file_path1.name

        if file_path2.exists():
            # Load the XML trees
            tree1 = ET.parse(file_path1)
            tree2 = ET.parse(file_path2)

            # Merge and write to the output directory
            output_file = output_dir / file_path1.name
            merge_xml_trees(tree1, tree2, output_file)

dir1 = "headed"
dir2 = "eyes"
output_dir = "headed_eyes"
merge_xml_files_in_dirs(dir1, dir2, output_dir)
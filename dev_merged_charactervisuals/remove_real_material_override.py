#removes realmaterialoverrides from given directory's xml/lsx
import xml.etree.ElementTree as ET
from pathlib import Path

def remove_real_material_overrides_children(tree):
    root = tree.getroot()
    # Find all 'Resource' nodes
    resource_nodes = root.findall(".//node[@id='Resource']")

    for resource_node in resource_nodes:
        # Find the 'RealMaterialOverrides' node
        real_material_overrides = resource_node.find(".//node[@id='RealMaterialOverrides']")
        # Find the <children> element under real_material_overrides
        children = real_material_overrides.find(".//children")
        
        # If <children> exists, clear its content
        if children is not None:
            object_nodes = children.findall(".//node[@id='Object']")
            for object_node in object_nodes:
                mapkey_node = object_node.find(".//attribute[@id='MapKey']")
                if mapkey_node is not None and "Head" in mapkey_node.get('value'):
                    children.remove(object_node)

def process_xml_files_in_dirs(dir_path, output_dir):
    dir_path = Path(dir_path)
    output_dir = Path(output_dir)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterate over all XML files in dir_path
    for file_path in dir_path.glob("*.lsx"):
        tree = ET.parse(file_path)
        remove_real_material_overrides_children(tree)

        output_file = output_dir / file_path.name
        tree.write(output_file, encoding='utf-8')

dir_path = "current"
output_dir = "headless"
process_xml_files_in_dirs(dir_path, output_dir)

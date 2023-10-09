#merges visual banks and material banks of given directories' xml/lsx/whatever
from pathlib import Path
import xml.etree.ElementTree as ET

def merge_xmls(filenames, base_xml):
    base_tree = ET.parse(base_xml)
    base_root = base_tree.getroot()
    material_base_children_node = base_root.find(".//node[@id='MaterialBank']/children")
    visual_base_children_node = base_root.find(".//node[@id='VisualBank']/children")
    # for each filename, parse the xml, and get all resource nodes
    for filename in filenames:
        tree = ET.parse(filename)
        root = tree.getroot()
        resource_nodes = root.findall(".//node[@id='MaterialBank']/children/*")
        # add each resource node to the base xml
        for resource_node in resource_nodes:
            material_base_children_node.append(resource_node)
        resource_nodes = root.findall(".//node[@id='VisualBank']/children/*")
        for resource_node in resource_nodes:
            visual_base_children_node.append(resource_node)
    # save the merged xml to a new file
    merged_tree = ET.ElementTree(base_root)
    merged_tree.write("merged.xml")

source_path = Path('vanilla_heads/TEST/')
base_xml_path = Path('blanks/blank.lsx')
files = []
for path in source_path.rglob('*'):
    if path.suffix == ('.lsx'):
        files.append(path)
merge_xmls(files,base_xml_path)

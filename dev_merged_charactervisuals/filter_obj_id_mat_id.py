#filters "obj_id_mat_id" by %given% substring
import xml.etree.ElementTree as ET
from pathlib import Path
# Sample XML content
import xml.etree.ElementTree as ET
from pathlib import Path

def filter_obj_id_mat_id(given_xml, substring, section):
    xml_tree = ET.parse(given_xml)
    xml_root = xml_tree.getroot()

    # Create a new root for output XML
    output_root = ET.Element("root")

    # Iterate through all "Object" nodes
    for obj_node in xml_root.findall(".//node[@id='Object']"):
        mapkey_node = obj_node.find(".//attribute[@id='MapKey']")
        if mapkey_node is not None:
            if substring in mapkey_node.attrib['value']:
                print(f"Found: {mapkey_node.attrib['value']} for {substring}")
                output_root.append(obj_node)
    output_tree = ET.ElementTree(output_root)
    output_tree.write(f'{given_xml.stem}_{section}_{substring}.lsx')


def create_substrings_and_filter(given_xml):
    sections = {
        'NORMIES': (['ELF','HEL','HUM'], ['F_','FS_','M_','MS_']),
        'TIEFLINGS': (['TIF', 'CAMBION'], ['F_','FS_','M_','MS_']),
        'HALFORC': (['HRC'], ['F_','M_']),
        'DWARVES': (['DWR'], ['F_','M_']),
        'GITHYANKI': (['GTY'], ['F_','M_']),
        'GNOMES': (['GNO'], ['F_','M_']),
        'HALFLINGS': (['HFL'], ['F_','M_'])
    }

    for section, (prefixes, suffixes) in sections.items():
        for prefix in prefixes:
            for suffix in suffixes:
                substring = prefix + "_" + suffix
                filter_obj_id_mat_id(given_xml, substring, section)

source_xml = Path("vanilla_heads/patch_3/all_redirects/merged_obj_id_mat_id.xml")
create_substrings_and_filter(source_xml)
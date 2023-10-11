# TODO: Create List of every Larian material UUID where using SourceFile "CHAR_Skin_Head_v3*.lsf".
# TODO: for each modder-created material UUID where SourceFile "CHAR_SkinHead_v3*.lsf", check if its in my list
# TODO: if it is print badnoodle detected.

import csv
import xml.etree.ElementTree as ET
from pathlib import Path

# Load and parse the XML file


def parse_xml_for_larian_resources(xml):
    larian_resources_dict = {}
    mat_tree = ET.parse(xml)
    mat_root = mat_tree.getroot()
    material_bank_region = mat_root.find(".//region[@id='MaterialBank']")
    if material_bank_region is not None:
        # Iterate through each <node id="Resource"> element
        for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
            resource_name = resource_node.find(
                ".//attribute[@id='Name']").get("value")
            resource_id = resource_node.find(
                f".//attribute[@id='ID']").get("value")
            resource_SourceFile = resource_node.find(
                ".//attribute[@id='SourceFile']")
            lod_files = ["CHAR_Skin_Head_v3.lsf", "CHAR_Skin_Head_v3_LOD1.lsf",
                         "CHAR_Skin_Head_v3_LOD2.lsf", "CHAR_Skin_Head_v3_LOD3.lsf", "CHAR_Skin_Head_v3_LOD4.lsf"]
            if any(lod in resource_SourceFile.get("value") for lod in lod_files):
                larian_resources_dict[resource_id] = resource_name
        return larian_resources_dict
    else:
        print("MaterialBank region not found in the XML.")
        return None


def parse_xml_for_bad_noodles(xml, larian_resources_dict):
    bad_noodle_dict = {}

    mat_tree = ET.parse(xml)
    mat_root = mat_tree.getroot()
    material_bank_region = mat_root.find(".//region[@id='MaterialBank']")

    if material_bank_region is not None:
        # Iterate through each <node id="Resource"> element
        for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
            resource_name = resource_node.find(
                ".//attribute[@id='Name']").get("value")
            resource_id = resource_node.find(
                f".//attribute[@id='ID']").get("value")

            if resource_id in larian_resources_dict:
                bad_noodle_dict[resource_id] = resource_name

        return bad_noodle_dict
    else:
        print("MaterialBank region not found in the XML.")
        return None


def write_dict(output_path, data_dict, field_names=None):
    # clearly from chatgpt
    with open(output_path, 'w', newline='') as file:
        # If field_names is not provided, default to ["ID", "Name"]
        if not field_names:
            field_names = ["ID", "Name"]

        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

        # If the dictionary is double-level (contains sub-dicts), e.g., {'path': {'ID': 'Name'}}
        if isinstance(next(iter(data_dict.values())), dict):
            for path, resource_data in data_dict.items():
                for resource_id, resource_name in resource_data.items():
                    writer.writerow(
                        {'Path': path, 'ID': resource_id, 'Name': resource_name})
        # If the dictionary is single-level, e.g., {'ID': 'Name'}
        else:
            for resource_id, resource_name in data_dict.items():
                writer.writerow({'ID': resource_id, 'Name': resource_name})


def read_csv_to_dict(filename):
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        return {rows[0]: rows[1] for rows in reader}


def write_larian_resources_csv(source_path, output_path):
    larian_resources_dict = parse_xml_for_larian_resources(source_path)
    field_names = ["ID", "Name"]
    write_dict(output_path, larian_resources_dict, field_names)


def find_bad_noodles(source_directory, dict):
    larian_resources_dict = read_csv_to_dict(dict)
    master_bad_noodle_dict = {}
    source_path = Path(source_directory)

    for path in source_path.rglob('*'):
        if path.suffix == '.lsx' and "CharacterCreation" not in str(path):
            result = parse_xml_for_bad_noodles(path, larian_resources_dict)
            if result:
                relative_path_str = str(path.relative_to(source_path))
                master_bad_noodle_dict[relative_path_str] = result
    return master_bad_noodle_dict


# part 1
larian_resources_path = Path('./vanilla_heads/patch_3/all/merged.lsx')
larian_resources_dict = Path('./larian_resources_dict.csv')
write_larian_resources_csv(larian_resources_path, larian_resources_dict)

# part 2
bad_noodle_dict_path = Path('./bad_noodle_dict.csv')
master_bad_noodle_dict = find_bad_noodles(
    './modded_heads/source/', larian_resources_dict)
write_dict(bad_noodle_dict_path, master_bad_noodle_dict,["Path", "ID", "Name"])

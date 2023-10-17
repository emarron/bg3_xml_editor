# future home of xml parsing
import re
import uuid
# import xml.etree.ElementTree as ET
# we will be using lxml,
from lxml import etree


def create_variants(given_name):
    variant_dict = {'name': given_name, 'skeleton': given_name + "_BASE",
                    'texture_clea': given_name + "_CLEA", 'texture_hmvy': given_name + "_HMVY",
                    'texture_msk': given_name + "_MSK", 'texture_nm': given_name + "_NM"}
    # could map to dictionary
    return variant_dict


def create_resource_in_bank(resource_node, region_bank):
    children_tag = region_bank.find('./node/children')
    # Create a new node with id="resource"
    # Append the new node to 'children'
    children_tag.append(resource_node)


def replace_id(node, xml):
    id_value = node.find(".//attribute[@id='ID']").get('value')
    uuid4 = str(uuid.uuid4())
    return xml.replace(id_value, uuid4), uuid4


def replace_source_file_path(node, output_source_file_path, xml):
    # make sure windows paths become unix paths
    source_file_path_value = node.find(
        ".//attribute[@id='SourceFile']").get('value')
    return xml.replace(source_file_path_value, str(output_source_file_path.as_posix()))


def replace_template_file_path(node, output_source_file_path, xml):
    # make sure windows paths become unix paths
    template_file_path_value = node.find(
        ".//attribute[@id='Template']").get('value')
    return xml.replace(template_file_path_value, str(output_source_file_path.with_suffix('.Dummy_Root.0').as_posix()))


def replace_name(reference_name, output_name, xml):
    # Pattern for SourceFile
    pattern_sourcefile = re.compile(r'(?<=SourceFile")\s*\b' + re.escape(reference_name) + r'\b', re.IGNORECASE)
    
    # Pattern for Template
    pattern_template = re.compile(r'(?<=Template")\s*\b' + re.escape(reference_name) + r'\b', re.IGNORECASE)
    
    # Overall pattern excluding the lookbehinds
    pattern_general = re.compile(r'\b' + re.escape(reference_name) + r'\b', re.IGNORECASE)
    
    # First, let's find all matches that are not preceded by "SourceFile" or "Template"
    all_matches = pattern_general.findall(xml)
    sourcefile_matches = pattern_sourcefile.findall(xml)
    template_matches = pattern_template.findall(xml)
    
    # Number of replacements to make
    num_replacements = len(all_matches) - len(sourcefile_matches) - len(template_matches)
    
    # Now, let's replace only those matches which are not inside the "SourceFile" or "Template" attributes
    result_xml, num_subs_done = pattern_general.subn(output_name, xml, count=num_replacements)
    
    return result_xml


def extract_reference_nodes(xml_root, references_dict):
    material_bank = xml_root.find(".//region[@id='MaterialBank']")
    texture_bank = xml_root.find(".//region[@id='TextureBank']")
    visual_bank = xml_root.find(".//region[@id='VisualBank']")

    reference_nodes = {}
    # Extract material node
    for node in material_bank.findall(".//node[@id='Resource']"):
        name = node.find(".//attribute[@id='Name']").get("value")
        if references_dict['name'].lower() == name.lower():
            reference_nodes['material'] = node

    # Extract texture nodes
    for node in texture_bank.findall(".//node[@id='Resource']"):
        name = node.find(".//attribute[@id='Name']").get("value")
        for key in ['texture_clea', 'texture_hmvy', 'texture_msk', 'texture_nm']:
            if references_dict[key].lower() == name.lower():
                reference_nodes[key] = node

    # Extract visual node
    for node in visual_bank.findall(".//node[@id='Resource']"):
        name = node.find(".//attribute[@id='Name']").get("value")
        if references_dict['name'].lower() == name.lower():
            reference_nodes['visual'] = node

    return reference_nodes


def create_resources_in_banks(reference_nodes, base_banks):
    for key, node in reference_nodes.items():
        if 'texture' in key:
            bank_key = 'texture'
        else:
            bank_key = key

        # Ensure the base bank exists for this type of node
        if bank_key in base_banks:
            create_resource_in_bank(node, base_banks[bank_key])
        else:
            print(f"Warning: No base bank found for key: {bank_key}")


def replace_ids_and_paths_in_xml(str_base_xml, reference_nodes, output_paths_dict, reference_name, output_name):
    uuids = {}
    # crappy fix for replace_name

    # Replace UUIDs
    for key, node in reference_nodes.items():
        str_base_xml, extracted_uuid = replace_id(node, str_base_xml)
        uuids[key] = extracted_uuid

    # Replace source file paths
    for key, node in reference_nodes.items():
        output_key = None
        if key in output_paths_dict:
            output_key = key
        elif key == 'visual':
            output_key = 'body'

        if output_key:
            str_base_xml = replace_source_file_path(
                node, output_paths_dict[output_key], str_base_xml)

    # Replace template file paths (add more logic here if needed)
    str_base_xml = replace_template_file_path(
        reference_nodes['visual'], output_paths_dict['body'], str_base_xml)

    str_base_xml = replace_name(reference_name, output_name, str_base_xml)

    return str_base_xml, uuids.get('visual', None)


def merge_xml_nodes(target_node, source_node):
    """
    Merge children of source_node into target_node
    """
    for child in source_node:
        target_node.append(child)


def merge_xml(existing_xml_str, new_xml_str):
    existing_xml_str = existing_xml_str.replace(
        '<?xml version="1.0" encoding="utf-8"?>', '').strip()
    new_xml_str = new_xml_str.replace(
        '<?xml version="1.0" encoding="utf-8"?>', '').strip()

    existing_root = etree.fromstring(existing_xml_str)
    new_root = etree.fromstring(new_xml_str)

    # List of region IDs to target for merging
    region_ids = ["MaterialBank", "VisualBank", "TextureBank"]

    for region_id in region_ids:
        # Locate the target and source nodes for each region ID
        target_node = existing_root.find(
            f".//region[@id='{region_id}']/node[@id='{region_id}']/children")
        source_node = new_root.find(
            f".//region[@id='{region_id}']/node[@id='{region_id}']/children")

        # If both nodes exist, merge them
        if target_node is not None and source_node is not None:
            merge_xml_nodes(target_node, source_node)

    return etree.tostring(existing_root, encoding='utf-8').decode('utf-8')

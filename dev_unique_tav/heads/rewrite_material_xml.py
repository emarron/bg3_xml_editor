# given directory, and xml(s) meeting some naming criteria, xml(s) contents meeting some criteria, changes the contents' parameters and outputs to new file.

import xml.etree.ElementTree as ET
from pathlib import Path

# Load and parse the XML file
def parse_xml(xml):
    mat_tree = ET.parse(xml)
    mat_root = mat_tree.getroot()
    # Find the region with id="MaterialBank"
    material_bank_region = mat_root.find(".//region[@id='MaterialBank']")
    output_mat_root = ET.Element("root")
    if material_bank_region is not None:
        # Iterate through each <node id="Resource"> element
        for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
            # Find the <children> element
            children_element = resource_node.find("./children")
            # resource_name = resource_node.find(".//attribute[@id='Name']")
            resource_SourceFile = resource_node.find(
                ".//attribute[@id='SourceFile']")
            lod_files = ["CHAR_Skin_Head_v3.lsf","CHAR_Skin_Head_v3_LOD1.lsf", "CHAR_Skin_Head_v3_LOD2.lsf", "CHAR_Skin_Head_v3_LOD3.lsf", "CHAR_Skin_Head_v3_LOD4.lsf"]
            if any(lod in resource_SourceFile.get("value") for lod in lod_files):
                # I can't verify that HEAD is going to be in modded heads so I left it out.
                # if "_NKD_Head" in resource_name.get("value"):
                if children_element is not None:
                    bool_makeup, bool_tattoo = False, False
                    texture_2D_parameters_nodes = resource_node.findall(
                        ".//node[@id='Texture2DParameters']")
                    for texture_2D_parameters_node in texture_2D_parameters_nodes:
                        param_name = texture_2D_parameters_node.find(
                            ".//attribute[@id='ParameterName']")
                        if param_name.get("value") == "TattooAtlas":
                            param_ID = texture_2D_parameters_node.find(
                                ".//attribute[@id='ID']")
                            # this is the ID for the default tattoo set.
                            # if param_ID.get("value") == "505e82ee-ed64-05cc-aa31-6b7057a5b75f":
                            param_ID.set(
                                "value", "505e82ee-ed64-05cc-aa31-ieatpaste666")
                            param_ID = texture_2D_parameters_node.find(
                                ".//attribute[@id='Enabled']")
                            param_ID.set("value", "True")
                            bool_tattoo = True
                        if param_name.get("value") == "MakeUpAtlas":
                            param_ID = texture_2D_parameters_node.find(
                                ".//attribute[@id='ID']")
                            # this is the ID for the default makeup set.
                            # if param_ID.get("value") == "2f72fffe-7602-05c4-b005-14bd527391f1":
                            param_ID.set(
                                "value", "2f72fffe-7602-05c4-b005-ieatpaste666")
                            param_ID = texture_2D_parameters_node.find(
                                ".//attribute[@id='Enabled']")
                            param_ID.set("value", "True")
                            bool_makeup = True
                    if bool_makeup or bool_tattoo:
                        output_mat_root.append(resource_node)
                    children_element = None
        return output_mat_root
    else:
        print("MaterialBank region not found in the XML.")
        return None


def write_xmls(material_root):
    material_tree = ET.ElementTree(material_root)
    material_output = "merged_material.xml"
    material_tree.write(str(material_output),
                        encoding="utf-8", xml_declaration=True)
    print(f"Modified XML written to '{str(material_output)}'.")

source_path = Path('./modded_heads/source/')
merged_material_root = ET.Element("root")

for path in source_path.rglob('*'):
    if path.suffix == ('.lsx') and "CharacterCreation" not in str(path):
        result = parse_xml(path)
        if result != None:
            merged_material_root.extend(result)
write_xmls(merged_material_root)

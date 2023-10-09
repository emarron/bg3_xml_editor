# given directory, and xml(s) meeting some naming criteria, xml(s) contents meeting some criteria, changes the contents' UUID, then parameters and finally creates a map of the ObjectID --> new MaterialUUID for RealMaterialOverrides.


import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

# Load and parse the XML file


def parse_xml(xml):
    mat_tree = ET.parse(xml)
    mat_root = mat_tree.getroot()
    # Find the region with id="MaterialBank"
    material_bank_region = mat_root.find(".//region[@id='MaterialBank']")
    output_mat_root = ET.Element("root")

    visual_bank_region = mat_root.find(".//region[@id='VisualBank']")
    list_obj_id_mat_id = []
    if material_bank_region is not None:
        # Iterate through each <node id="Resource"> element
        for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
            # Find the <children> element
            children_element = resource_node.find("./children")
            resource_name = resource_node.find(".//attribute[@id='Name']")
            resource_SourceFile = resource_node.find(
                ".//attribute[@id='SourceFile']")
            base_materials = ["CHAR_Skin_Head_v3.lsf", "CHAR_Skin_Head_v3_LOD1.lsf",
                              "CHAR_Skin_Head_v3_LOD2.lsf"]
            resource_names = ["ELF", "DWR", "GNO", "GTH",
                              "HEL", "HLF", "HUM", "TIF", "CAMBION"]
            resource_names_excluded = ["CHD_", "MC_", "Severed", "SKEL_",
                                       "ZOM_", "NeckCut", "GOB_", "HARPY_", "HOB_", "PIXIE_", "BUGBEAR_"]
            # because surely no one will use these
            if any(base_material in resource_SourceFile.get("value") for base_material in base_materials) and not any(excluded_name in resource_name.get("value") for excluded_name in resource_names_excluded):
                # if "_F_" in resource_name.get("value"):
                # and for some godforsaken reason some the heads use the same obj ID. unique-key must be both obj and mat id
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
                            # probably gonna replace it with "505e82ee-ed64-05cc-aa31-ieatpaste666" because its funny
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
                        if bool_makeup and bool_tattoo:
                            uuid4 = str(uuid.uuid4())
                            resource_node_id = resource_node.find(
                                ".//attribute[@id='ID']")
                            vb_resource_nodes = visual_bank_region.findall(
                                ".//node[@id='Resource']")
                            for vb_resource_node in vb_resource_nodes:
                                # this needs to be rewritten for when we have multiple references to the same material from different objects
                                obj_nodes = vb_resource_node.findall(
                                    f".//node[@id='Objects']")
                                for obj_node in obj_nodes:
                                    mat_id = obj_node.find(
                                        f".//attribute[@id='MaterialID']").get("value")
                                    if mat_id == resource_node_id.get("value"):
                                        obj_node_name = obj_node.find(
                                            ".//attribute[@id='ObjectID']")
                                        print(obj_node_name.get("value"))
                                        list_obj_id_mat_id.append(
                                            [obj_node_name.get("value"), uuid4])
                            resource_node_id.set("value", uuid4)
                            output_mat_root.append(resource_node)
                            bool_makeup, bool_tattoo = False, False
                    children_element = None
        obj_id_mat_id_root = ET.Element("root")
        for pair in list_obj_id_mat_id:
            node = ET.SubElement(obj_id_mat_id_root, "node", id="Object")
            ET.SubElement(node, "attribute", id="MapKey",
                          type="FixedString", value=pair[0])
            ET.SubElement(node, "attribute", id="MapValue",
                          type="FixedString", value=pair[1])
        return [output_mat_root, obj_id_mat_id_root]
    else:
        print("MaterialBank region not found in the XML.")
        return None


def write_xmls(material_root, obj_id_mat_id_root):
    material_tree = ET.ElementTree(material_root)
    material_output = "merged_material.xml"
    material_tree.write(str(material_output),
                        encoding="utf-8", xml_declaration=True)
    print(f"Modified XML written to '{str(material_output)}'.")

    obj_id_mat_id_tree = ET.ElementTree(obj_id_mat_id_root)
    obj_id_mat_id_output = "merged_obj_id_mat_id.xml"

    obj_id_mat_id_tree.write(str(obj_id_mat_id_output),
                             encoding='utf-8', xml_declaration=True)
    print(f"Modified XML written to '{str(obj_id_mat_id_output)}'.")


source_path = Path('vanilla_heads/patch_3/all/')
merged_material_root = ET.Element("root")
merged_obj_id_mat_id_root = ET.Element("root")

for path in source_path.rglob('*'):
    if path.suffix == ('.lsx'):
        result = parse_xml(path)
        if result != None:
            merged_material_root.extend(result[0])
            merged_obj_id_mat_id_root.extend(result[1])
write_xmls(merged_material_root, merged_obj_id_mat_id_root)

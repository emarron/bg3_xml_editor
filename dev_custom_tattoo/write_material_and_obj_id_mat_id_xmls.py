import csv
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

# todo: use virtual texture name instead of material bank name
# todo: write PM as SRGB: FALSE, or just do it after :shrug:
# todo: rewrite this to NOT be a piece of trash.


# Load and parse the XML file
def parse_xml(xml):

    mat_tree = ET.parse(xml)
    mat_root = mat_tree.getroot()
    # Find the region with id="MaterialBank"
    material_bank_region = mat_root.find(".//region[@id='MaterialBank']")
    output_mat_root = ET.Element("root")

    visual_bank_region = mat_root.find(".//region[@id='VisualBank']")
    dict_obj_id_mat_id = {}
    list_obj_id_mat_id = []
    if material_bank_region is not None:
        # Iterate through each <node id="Resource"> element
        for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
            # Find the <children> element
            children_element = resource_node.find("./children")
            resource_name = resource_node.find(".//attribute[@id='Name']")
            resource_SourceFile = resource_node.find(".//attribute[@id='SourceFile']")
            if "CHAR_Skin_Head_v3.lsf" in resource_SourceFile.get("value"):
                # I can't verify that HEAD is going to be in modded heads so I left it out.
                # if "_NKD_Head" in resource_name.get("value"):
                # and for some godforsaken reason some the heads use the same obj ID. unique-key must be both obj and mat id
                if children_element is not None:
                    texture_2D_parameters_nodes = resource_node.findall(".//node[@id='Texture2DParameters']")
                    for texture_2D_parameters_node in texture_2D_parameters_nodes:
                        param_name = texture_2D_parameters_node.find(".//attribute[@id='ParameterName']")
                        if param_name.get("value") == "TattooAtlas":
                            param_ID = texture_2D_parameters_node.find(".//attribute[@id='ID']")
                            # this is the ID for the default tattoo set.
                            if param_ID.get("value") == "505e82ee-ed64-05cc-aa31-6b7057a5b75f":
                                # probably gonna replace it with "505e82ee-ed64-05cc-aa31-ieatpaste666" because its funny
                                uuid4 = str(uuid.uuid4())
                                resource_node_id = resource_node.find(".//attribute[@id='ID']")
                                vb_resource_nodes = visual_bank_region.findall(".//node[@id='Resource']")
                                for vb_resource_node in vb_resource_nodes:
                                        obj_nodes = vb_resource_node.findall(f".//node[@id='Objects']")
                                        for obj_node in obj_nodes:
                                            if obj_node is not None and obj_node.find(f".//attribute[@id='MaterialID']").get("value")==resource_node_id.get("value"):
                                                obj_node_name = obj_node.find(".//attribute[@id='ObjectID']")
                                                print(obj_node_name.get("value"))
                                                # replace this with list.
                                                list_obj_id_mat_id.append([obj_node_name.get("value"),uuid4])
                                resource_node_id.set("value", uuid4)
                                output_mat_root.append(resource_node)
                    children_element = None
        obj_id_mat_id_root = ET.Element("root")
        for pair in list_obj_id_mat_id:
            node = ET.SubElement(obj_id_mat_id_root, "node", id="Object")
            ET.SubElement(node, "attribute", id="MapKey", type="FixedString", value=pair[0])
            ET.SubElement(node, "attribute", id="MapValue", type="FixedString", value=pair[1])
        return [output_mat_root, obj_id_mat_id_root]
    else:
        print("MaterialBank region not found in the XML.")
        return None

def write_xmls(material_root, obj_id_mat_id_root ):
        material_tree = ET.ElementTree(material_root)
        material_output = "merged_material.xml"
        material_tree.write(str(material_output), encoding="utf-8", xml_declaration=True)
        print(f"Modified XML written to '{str(material_output)}'.")


        obj_id_mat_id_tree = ET.ElementTree(obj_id_mat_id_root)
        obj_id_mat_id_output = "merged_obj_id_mat_id.xml"

        obj_id_mat_id_tree.write(str(obj_id_mat_id_output), encoding='utf-8', xml_declaration=True)
        print(f"Modified XML written to '{str(obj_id_mat_id_output)}'.")

# todo: make it so repeats of the same material are addressed. i.e: HEAD D and HEAD D eyes gouged are the same.
# todo: get ears and other parts, also why aren't we getting strong types.
# todo: for file in paths:
source_path = Path('./source/male_gith_part_2/')
merged_material_root = ET.Element("root")
merged_obj_id_mat_id_root = ET.Element("root")

for path in source_path.rglob('*'):
    if path.suffix == ('.lsx') and path.stem == ("_merged"):
        result = parse_xml(path)
        if result != None:
            merged_material_root.extend(result[0])
            merged_obj_id_mat_id_root.extend(result[1])
write_xmls(merged_material_root, merged_obj_id_mat_id_root)

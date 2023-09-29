import uuid
import xml.etree.ElementTree as ET


# todo: write PM as SRGB: FALSE, or just do it after :shrug:
# todo: rewrite this to NOT be a piece of trash.

def create_texture_node(id_value, name_value, type):
    texture_node = ET.Element("node", id="Resource")
    attributes = [
        ("Depth", "int32", "1"),
        ("Height", "int32", "2048"),
        ("ID", "FixedString", id_value),
        ("Localized", "bool", "False"),
        ("Name", "LSString", name_value + type),
        ("SRGB", "bool", "True"),
        ("SourceFile", "LSString",
         'Generated/Public/Shared/Assets/kartoffels_clubhouse/Textures/' + name_value + type + '.dds'),
        ("Streaming", "bool", "True"),
        ("Template", "FixedString", name_value),
        ("Type", "int32", "1"),
        ("Width", "int32", "2048"),
        ("_OriginalFileVersion_", "int64", "144115198813274412")
    ]
    for attr_id, attr_type, attr_value in attributes:
        attribute = ET.Element("attribute", id=attr_id, type=attr_type, value=attr_value)
        texture_node.append(attribute)
    return texture_node


texture_suffix_dict = {
    "basecolor": "_BM",
    "normalmap": "_NM",
    "physicalmap": "_PM"
}

# Load and parse the XML file
tex_tree = ET.parse('Shared/Content/Assets/Characters/_merged.lsx')
mat_tree = ET.parse('Shared/Content/Assets/Characters/Humans/[PAK]_Female_Armor/_merged.lsx')
tex_root = tex_tree.getroot()
mat_root = mat_tree.getroot()
# Find the region with id="MaterialBank"
material_bank_region = mat_root.find(".//region[@id='MaterialBank']")
virtual_texture_bank_region = tex_root.find(".//region[@id='VirtualTextureBank']")
# for the separate texture bank data:
output_tex_root = ET.Element("root")
output_mat_root = ET.Element("root")
virtual_texture_dictionary = {}
if virtual_texture_bank_region is not None:
    # iterate and grab names
    for resource_node in virtual_texture_bank_region.findall(".//node[@id='Resource']"):
        vtex_id = resource_node.find(".//attribute[@id='ID']").get("value")
        vtex_name = resource_node.find(".//attribute[@id='Name']").get("value")
        virtual_texture_dictionary[vtex_id] = vtex_name
if material_bank_region is not None:
    # Iterate through each <node id="Resource"> element
    for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
        # Find the <children> element
        children_element = resource_node.find("./children")
        resource_name = resource_node.find(".//attribute[@id='Name']")
        resource_SourceFile = resource_node.find(".//attribute[@id='SourceFile']")
        if "_VT" in resource_SourceFile.get("value"):
            if "_ARM_" in resource_name.get("value"):
                if children_element is not None:
                    virtual_texture_parameters_node = resource_node.find(".//node[@id='VirtualTextureParameters']")
                    if virtual_texture_parameters_node is not None:
                        # Create and append three <node id="Texture2DParameters"> elements
                        children_element.remove(virtual_texture_parameters_node)
                        for texture_param_name in ["basecolor", "normalmap", "physicalmap"]:
                            uuid4 = str(uuid.uuid4())
                            texture2d_parameters_node = ET.Element("node", id="Texture2DParameters")
                            attribute_enabled = ET.Element("attribute", id="Enabled", type="bool", value="True")
                            attribute_export_as_preset = ET.Element("attribute", id="ExportAsPreset", type="bool",
                                                                    value="False")
                            attribute_group_name = ET.Element("attribute", id="GroupName", type="FixedString", value="")
                            attribute_id = ET.Element("attribute", id="ID", type="FixedString", value=uuid4)
                            attribute_ignore_texel_density = ET.Element("attribute", id="IgnoreTexelDensity",
                                                                        type="bool",
                                                                        value="True")
                            attribute_parameter_name = ET.Element("attribute", id="ParameterName", type="FixedString",
                                                                  value=texture_param_name)

                            texture2d_parameters_node.extend([
                                attribute_enabled,
                                attribute_export_as_preset,
                                attribute_group_name,
                                attribute_id,
                                attribute_ignore_texel_density,
                                attribute_parameter_name
                            ])

                            children_element.append(texture2d_parameters_node)
                            # to make this work cross-reference vtex-id with vtex-name, when loading the initial XML, get a list of all vtexs[id]=name in vtex bank as dict.
                            mat_name = resource_node.find("./attribute[@id='Name']").get(
                                "value")
                            vtex_id = virtual_texture_parameters_node.find("./attribute[@id='ID']").get(
                                "value")  # Get Name attribute value from resource_node
                            vtex_name = virtual_texture_dictionary.get(vtex_id)
                            try:
                                texture_resource_node = create_texture_node(uuid4, vtex_name,
                                                                            texture_suffix_dict.get(texture_param_name))

                            except TypeError:
                                # this will trigger when referencing a texture node outside given _merged.lsx, if this is the case, I'm just going to create it based on the material node as its correct 90% of the time.
                                print(f'vtex_id: {vtex_id}, vtex_name: {vtex_name}, mat_name: {mat_name}')
                                texture_resource_node = create_texture_node(uuid4, mat_name,
                                                                            texture_suffix_dict.get(texture_param_name))
                            output_tex_root.append(texture_resource_node)
                        output_mat_root.append(resource_node)
                        # sets this to none after we are done as a failsafe.
                        virtual_texture_parameters_node = None
                    # sets this to none after we are done as a failsafe.
                    children_element = None

    # Write modified XML structure to new.xml
    material_tree = ET.ElementTree(output_mat_root)
    material_tree.write("material.xml", encoding="utf-8", xml_declaration=True)

    print("Modified XML written to 'material.xml'.")
    texture_tree = ET.ElementTree(output_tex_root)
    texture_tree.write("texture.xml", encoding="utf-8", xml_declaration=True)
    print("Texture XML written to 'texture.xml'.")

else:
    print("MaterialBank region not found in the XML.")

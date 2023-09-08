import uuid
import xml.etree.ElementTree as ET


def create_texture_node(id_value, name_value, type):
    texture_node = ET.Element("node", id="Resource")
    attributes = [
        ("Depth", "int32", "1"),
        ("Height", "int32", "2048"),
        ("ID", "FixedString", id_value),
        ("Localized", "bool", "False"),
        ("Name", "LSString", name_value + type),
        ("SRGB", "bool", "True"),
        ("SourceFile", "LSString", 'Generated/Public/Shared/Assets/kartoffels_clubhouse/Textures/'+ name_value + type + '.dds'),
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
tree = ET.parse('Shared/Content/Assets/Characters/Humans/[PAK]_Female_Armor/_merged.lsx')
root = tree.getroot()
# Find the region with id="MaterialBank"
material_bank_region = root.find(".//region[@id='MaterialBank']")

# for the separate texture bank data:
texture_root = ET.Element("root")

if material_bank_region is not None:
    # Iterate through each <node id="Resource"> element
    for resource_node in material_bank_region.findall(".//node[@id='Resource']"):
        # Find the <children> element
        children_element = resource_node.find("./children")

        if children_element is not None:
            virtual_texture_parameters_node = resource_node.find(".//node[@id='VirtualTextureParameters']")
            if virtual_texture_parameters_node is not None:
                # Create and append three <node id="Texture2DParameters"> elements
                children_element.remove(virtual_texture_parameters_node)
                for texture_param_name in ["basecolor", "normalmap", "physicalmap"]:
                    uuid4 = str(uuid.uuid4())
                    texture2d_parameters_node = ET.Element("node", id="Texture2DParameters")
                    attribute_enabled = ET.Element("attribute", id="Enabled", type="bool", value="True")
                    attribute_export_as_preset = ET.Element("attribute", id="ExportAsPreset", type="bool", value="False")
                    attribute_group_name = ET.Element("attribute", id="GroupName", type="FixedString", value="")
                    attribute_id = ET.Element("attribute", id="ID", type="FixedString", value=uuid4)
                    attribute_ignore_texel_density = ET.Element("attribute", id="IgnoreTexelDensity", type="bool",
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
                    somevalue = "some_value"  # Replace with actual value
                    somevalue2 = "some_value2"  # Replace with actual value
                    name = resource_node.find("./attribute[@id='Name']").get(
                        "value")  # Get Name attribute value from resource_node
                    texture_resource_node = create_texture_node(uuid4, name,
                                                                texture_suffix_dict.get(texture_param_name))
                    texture_root.append(texture_resource_node)

    # Write modified XML structure to new.xml
    tree.write("new.xml", encoding="utf-8", xml_declaration=True)

    print("Modified XML written to 'new.xml'.")
    texture_tree = ET.ElementTree(texture_root)
    texture_tree.write("texture.xml", encoding="utf-8", xml_declaration=True)
    print("Texture XML written to 'texture.xml'.")

else:
    print("MaterialBank region not found in the XML.")

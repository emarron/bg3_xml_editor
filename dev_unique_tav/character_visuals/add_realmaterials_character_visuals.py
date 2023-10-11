# program to append resources to character visual files
import xml.etree.ElementTree as ET
from pathlib import Path


def merge_xml_trees(tree1, tree2, substring, output):
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    # Find the 'CharacterVisualBank' node in both XML documents
    character_visual_bank1 = root1.find(".//node[@id='CharacterVisualBank']")

    # Find all 'Resource' nodes under 'CharacterVisualBank' in both XML documents
    resource_nodes1 = character_visual_bank1.findall(".//node[@id='Resource']")
    resource_nodes2 = root2.findall(".//node[@id='Object']")

    # Create a dictionary to store the 'Resource' nodes from the second XML document
    # Iterate over 'Resource' nodes in the first XML document
    for resource_node1 in resource_nodes1:
        body_set_visual_value = resource_node1.find(
            ".//attribute[@id='BodySetVisual']").get('value')
        if body_set_visual_value == substring:
            real_material_overrides1 = resource_node1.find(
                ".//node[@id='RealMaterialOverrides']")
            children1 = real_material_overrides1.find(".//children")
            if children1 is None:
                children1 = ET.Element("children")
                real_material_overrides1.append(children1)
            for resource_node in resource_nodes2:
                children1.append(resource_node)

    # Serialize the merged XML document
    merged_xml_content = ET.tostring(root1, encoding='utf-8').decode()

    merged_xml_content = ET.tostring(root1, encoding='utf-8').decode()

    # Save the merged XML content to the output file
    with open(output, "w") as merged_file:
        merged_file.write(merged_xml_content)


def merge_xml_files_in_dirs(dir1, dir2_folder, substring, output_dir):
    dir1 = Path(dir1)
    dir2 = Path("patch_3") / dir2_folder
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    for file_path1 in dir1.glob("*.lsx"):
        for file_path2 in dir2.glob("*.lsx"):
            if file_path2.exists():
                tree1 = ET.parse(file_path1)
                tree2 = ET.parse(file_path2)
                output_file = output_dir / file_path1.name
                merge_xml_trees(tree1, tree2, substring, output_file)

folder_to_substring = {
    "dwr_f_": "774a9359-3d67-4021-b32f-6c229d709741",
    "dwr_m_": "a2883048-858d-2937-720d-795a83666532",
    "gno_f_": "15c6cbdb-a29e-f1d6-79f4-0f9b69384789",
    "gno_m_": "c59f89aa-584f-615d-84d9-1d89e98c3d30",
    "gty_f_": "b7bfa2d3-4dad-d8a3-8639-9e3dddb97a00",
    "gty_m_": "e933d49d-9207-e9fc-819f-45db5b403a11",
    "hfl_f_": "c50cc8ac-4e4c-9178-a19e-4969e6ccc55b",
    "hfl_m_": "3ddf6079-6af3-8391-6aa3-0d8582f4a396",
    "hrc_f_": "ecf0a1f3-1874-8f5c-dde4-40d57af42fe6",
    "hrc_m_": "0146aeba-f96d-9273-bb1c-0121453d9a8d",
    "normies_f_": "53715306-dab4-4921-82e8-0c1a84171f79",
    "normies_fs_": "b86e1014-a3c2-4a1e-8972-6b9b48faab22",
    "normies_m_": "001232d5-2155-44b9-a238-ad4e01f9e87d",
    "normies_ms_": "12ae5f3b-d96f-4cb0-8025-39b16052259f",
    "tif_f_": "04883d8a-bbfa-46ff-8984-b257c871bec3",
    "tif_fs_": "7c13b43c-0bbb-4c66-b9ad-a76dbc1bf4e8",
    "tif_m_": "6790f60d-6124-4e26-885e-e3b44dcd467e",
    "tif_ms_": "fb3af81e-0311-4366-9fa4-26361e585be8"
}

dir1 = "headed"
output_dir = "headed"
for folder, substring in folder_to_substring.items():
    merge_xml_files_in_dirs(dir1, folder, substring, output_dir)
"""
folder: substring
dwr_f_: "774a9359-3d67-4021-b32f-6c229d709741"
dwr_m_: "a2883048-858d-2937-720d-795a83666532"
gno_f_: "15c6cbdb-a29e-f1d6-79f4-0f9b69384789"
gno_m_: "c59f89aa-584f-615d-84d9-1d89e98c3d30"
gty_f_: "b7bfa2d3-4dad-d8a3-8639-9e3dddb97a00"
gty_m_: "e933d49d-9207-e9fc-819f-45db5b403a11"
hfl_f_: "c50cc8ac-4e4c-9178-a19e-4969e6ccc55b"
hfl_m_: "3ddf6079-6af3-8391-6aa3-0d8582f4a396"
hrc_f_: "ecf0a1f3-1874-8f5c-dde4-40d57af42fe6"
hrc_m_: "0146aeba-f96d-9273-bb1c-0121453d9a8d"
normies_f_: "53715306-dab4-4921-82e8-0c1a84171f79"
normies_fs_: "b86e1014-a3c2-4a1e-8972-6b9b48faab22
normies_m_: "001232d5-2155-44b9-a238-ad4e01f9e87d"
normies_ms_: "12ae5f3b-d96f-4cb0-8025-39b16052259f"
tif_f_: "04883d8a-bbfa-46ff-8984-b257c871bec3"
tif_fs_: "7c13b43c-0bbb-4c66-b9ad-a76dbc1bf4e8"
tif_m_: "6790f60d-6124-4e26-885e-e3b44dcd467e"
tif_ms_: "fb3af81e-0311-4366-9fa4-26361e585be8"

"""
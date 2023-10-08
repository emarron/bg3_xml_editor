# todo
# create boilerplate XML (skeletonbank, materialbank, texturebank, visualbank)
# copy given %reference_name% from given %larian_merged_character_resources% _merged.lsx, 
#i.e. "ELF_F_NKD_HEAD_A" --> retrieve skeleton resource "ELF_F_NKD_HEAD_A_BASE", material resource "ELF_F_NKD_HEAD_A", texture resources "ELF_F_NKD_HEAD_A_CLEA","ELF_F_NKD_HEAD_A_NM", "ELF_F_NKD_HEAD_A_HMVY", visual resource "ELF_F_NKD_HEAD_A"
# rewrite UUID of each retrieved NODE, making sure to edit across entire XML. i.e: the material resource will reference the texture resources.
# Enter in the PATHS from given directory. given directory must be named %item_name%, where inside is %item_name%.GR2, %item_name%_BASE.GR2, %item_name%_CLEA.DDS, %item_name%_NM.DDS, %item_name%_HMVY.DDS.
# rename all "Name" values from %reference_name% to %item_name%

# finally, create a variation if skeleton doesn't exist
# finally, create command line interface

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
import uuid
import re
import sys
import tkinter as tk
from tkinter import filedialog

def create_variants(given_name):
    variant_dict = {}
    variant_dict['name'] = given_name # used by material and visual resource
    variant_dict['skeleton_name'] = given_name + "_BASE"
    variant_dict['texture_clea_name'] = given_name + "_CLEA"
    variant_dict['texture_hmvy_name'] = given_name + "_HMVY"
    variant_dict['texture_nm_name'] = given_name + "_NM"
    # could map to dictionary
    return variant_dict

# run a check to make sure all entities exist physically, shit code
def create_variant_paths(path, dictionary):
    if path.exists():
        paths_dict = {}
        paths_dict['texture_clea_path'] = (path / dictionary['texture_clea_name']).with_suffix(".DDS")
        paths_dict['texture_hmvy_path'] = (path / dictionary['texture_hmvy_name']).with_suffix(".DDS")
        paths_dict['texture_nm_path'] = (path / dictionary['texture_nm_name']).with_suffix(".DDS")
        paths_dict['skeleton_path'] = (path / dictionary['skeleton_name']).with_suffix(".GR2")
        paths_dict['head_path'] = (path / dictionary['name']).with_suffix(".GR2")
        return paths_dict
    else:
        return None # set up a break here or something


def create_resource_in_bank(resource_node,region_bank):
    children_tag = region_bank.find('./node/children')
    # Create a new node with id="resource"
    # Append the new node to 'children'
    children_tag.append(resource_node)

def replace_id(node, xml):
    id_value = node.find(".//attribute[@id='ID']").get('value')
    uuid4 = str(uuid.uuid4())
    return xml.replace(id_value, uuid4)

def replace_source_file_path(node, output_source_file_path,xml):
    # make sure windows paths become unix paths
    source_file_path_value = node.find(".//attribute[@id='SourceFile']").get('value') 
    return xml.replace(source_file_path_value,str(output_source_file_path.as_posix()))

def replace_template_file_path(node, output_source_file_path,xml):
        # make sure windows paths become unix paths
    template_file_path_value = node.find(".//attribute[@id='Template']").get('value')
    return xml.replace(template_file_path_value,str(output_source_file_path.with_suffix('.Dummy_Root.0').as_posix()))

def replace_name(original_name, output_name, xml):
    pattern = re.compile(re.escape(original_name), re.IGNORECASE)
    return pattern.sub(output_name,xml)

def check_file_existence(file_path):
    file_path = Path(file_path)

    if file_path.exists():
        print(f"The file '{file_path}' exists.")
    else:
        print(f"The file '{file_path}' does not exist. Exiting program.")
        sys.exit(1)

def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    
def browse_directory(entry):
    dir_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)

def generate_xml():
    base_xml_path = Path(base_xml_entry.get())
    reference_xml_path = Path(reference_xml_entry.get())
    reference_name = reference_name_entry.get()
    output_dir_path = Path(output_dir_entry.get())

# base_xml_path = Path("./source/base.xml")
# reference_xml_path = Path("./source/_merged.lsx") # elf heads
# reference_name = "ELF_F_NKD_HEAD_D"
# output_dir_path = Path("./Generated/Hazel_Head")




# Now you can use these variables as needed in your code
print(f"Base XML path: {base_xml_path}")
print(f"Reference XML path: {reference_xml_path}")
print(f"Reference name: {reference_name}")
print(f"Output directory path: {output_dir_path}")

# does reference_xml_path exist?
# does output_dir_path exist?
# can also check if reference name exists in path (maybe)



check_file_existence(base_xml_path)
check_file_existence(reference_xml_path)
check_file_existence(output_dir_path)


# some checks
output_name = output_dir_path.name
references_dict = create_variants(reference_name)
outputs_dict = create_variants(output_name)
output_paths_dict = create_variant_paths(output_dir_path, outputs_dict)
for key,value in output_paths_dict.items():
    check_file_existence(value)
    
print("All files exist, beginning program, please make sure your Reference Head Name is properly typed as I can't check for that.")
print(f"Reference Head Name: {reference_name}")
print(f"Output Head Name: {output_name}")


# if output_paths_dict != None:
#     for key,value in output_paths_dict.items():
#         exists = value.exists()
#         print(f'key: {key}, value: {value}, exists: {exists}')
#     else: 
#         print(f'you have typed in your output directory incorrectly')

# print(f'reference path: {reference_xml_path}, reference exists: {reference_xml_path.exists()}')

# create a stop here if our required files don't exist, and tell user to fix their paths. Skeleton file is not a hard requirement


# load and parse XML file

reference_xml = ET.parse(str(reference_xml_path))
reference_skel_bank = reference_xml.getroot().find((".//region[@id='SkeletonBank']"))
reference_mat_bank = reference_xml.getroot().find((".//region[@id='MaterialBank']"))
reference_tex_bank = reference_xml.getroot().find((".//region[@id='TextureBank']"))
reference_vis_bank = reference_xml.getroot().find((".//region[@id='VisualBank']"))

for resource_node in reference_skel_bank.findall(".//node[@id='Resource']"):
    name = resource_node.find(".//attribute[@id='Name']").get("value")
    if references_dict['skeleton_name'].lower() == name.lower(): 
        reference_skeleton_node = resource_node
for resource_node in reference_mat_bank.findall(".//node[@id='Resource']"):
    name = resource_node.find(".//attribute[@id='Name']").get("value")
    if references_dict['name'].lower() == name.lower(): 
        reference_material_node = resource_node
for resource_node in reference_tex_bank.findall(".//node[@id='Resource']"):
    name = resource_node.find(".//attribute[@id='Name']").get("value")
    if references_dict['texture_clea_name'].lower() == name.lower(): 
        reference_texture_clea_node = resource_node
    if references_dict['texture_hmvy_name'].lower() == name.lower(): 
        reference_texture_hmvy_node = resource_node
    if references_dict['texture_nm_name'].lower() == name.lower(): 
        reference_texture_nm_node = resource_node
for resource_node in reference_vis_bank.findall(".//node[@id='Resource']"):
    name = resource_node.find(".//attribute[@id='Name']").get("value")
    if references_dict['name'].lower() == name.lower(): 
        reference_visual_node = resource_node




base_xml = ET.parse(str(base_xml_path))
# this is for our generated node
base_skel_bank = base_xml.getroot().find((".//region[@id='SkeletonBank']"))
base_mat_bank = base_xml.getroot().find((".//region[@id='MaterialBank']"))
base_tex_bank = base_xml.getroot().find((".//region[@id='TextureBank']"))
base_vis_bank = base_xml.getroot().find((".//region[@id='VisualBank']"))
    
create_resource_in_bank(reference_skeleton_node, base_skel_bank)
create_resource_in_bank(reference_material_node, base_mat_bank)
create_resource_in_bank(reference_texture_clea_node, base_tex_bank)
create_resource_in_bank(reference_texture_hmvy_node, base_tex_bank)
create_resource_in_bank(reference_texture_nm_node, base_tex_bank)
create_resource_in_bank(reference_visual_node, base_vis_bank)

# now there are many ways one could go about updating entries but...... lets do it the shitty way
# replace UUIDs:
str_base_xml = ET.tostring(base_xml.getroot(), encoding='utf-8').decode('utf-8')
str_base_xml = replace_id(reference_skeleton_node, str_base_xml)
str_base_xml = replace_id(reference_material_node, str_base_xml)
str_base_xml = replace_id(reference_texture_clea_node, str_base_xml)
str_base_xml = replace_id(reference_texture_hmvy_node, str_base_xml)
str_base_xml = replace_id(reference_texture_nm_node, str_base_xml)
str_base_xml = replace_id(reference_visual_node, str_base_xml)

# replace source file paths:
str_base_xml = replace_source_file_path(reference_skeleton_node,output_paths_dict['skeleton_path'],str_base_xml)
str_base_xml = replace_source_file_path(reference_texture_clea_node,output_paths_dict['texture_clea_path'],str_base_xml)
str_base_xml = replace_source_file_path(reference_texture_hmvy_node,output_paths_dict['texture_hmvy_path'],str_base_xml)
str_base_xml = replace_source_file_path(reference_texture_nm_node,output_paths_dict['texture_nm_path'],str_base_xml)
str_base_xml = replace_source_file_path(reference_visual_node,output_paths_dict['head_path'],str_base_xml)

# replace template file paths:
str_base_xml = replace_template_file_path(reference_skeleton_node,output_paths_dict['skeleton_path'],str_base_xml)
str_base_xml = replace_template_file_path(reference_visual_node,output_paths_dict['head_path'],str_base_xml)

# replace names:

str_base_xml = replace_name(reference_name, output_name, str_base_xml)

# write XML
with open("output_xml.xml", 'w', encoding='utf-8') as file:
    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    file.write(str_base_xml)

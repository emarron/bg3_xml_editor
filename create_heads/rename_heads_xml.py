import re
import tkinter as tk
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter import filedialog

# create variant that accepts "_REMAPPED"

def check_file_existence(file_path):
    # make sure its a path
    file_path = Path(file_path)
    # for some reason this isn't case sensitive so here's a work around.
    path_as_str = str(file_path)
    if path_as_str not in str(file_path.resolve()):
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)  # Clear existing text
        output_text.insert(tk.END, f"The file '{file_path}' does not exist. Exiting program.\n")
        output_text.config(state=tk.DISABLED)
        print(f"The file '{file_path}' does not exist. Exiting program.")
        autoresize_text_widget(output_text)
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")


# Define other necessary functions and variables here

def create_variants(given_name):
    variant_dict = {'name': given_name, 'skeleton_name': given_name + "_BASE",
                    'texture_clea_name': given_name + "_CLEA", 'texture_hmvy_name': given_name + "_HMVY",
                    'texture_nm_name': given_name + "_NM"}
    # could map to dictionary
    return variant_dict


# run a check to make sure all entities exist physically, shit code
def create_variant_paths(path, dictionary):
    if path.exists():
        paths_dict = {'texture_clea_path': (path / dictionary['texture_clea_name']).with_suffix(".DDS"),
                      'texture_hmvy_path': (path / dictionary['texture_hmvy_name']).with_suffix(".DDS"),
                      'texture_nm_path': (path / dictionary['texture_nm_name']).with_suffix(".DDS"),
                      'skeleton_path': (path / dictionary['skeleton_name']).with_suffix(".GR2"),
                      'head_path': (path / dictionary['name']).with_suffix(".GR2")}
        return paths_dict
    else:
        return None  # set up a break here or something


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
    source_file_path_value = node.find(".//attribute[@id='SourceFile']").get('value')
    return xml.replace(source_file_path_value, str(output_source_file_path.as_posix()))


def replace_template_file_path(node, output_source_file_path, xml):
    # make sure windows paths become unix paths
    template_file_path_value = node.find(".//attribute[@id='Template']").get('value')
    return xml.replace(template_file_path_value, str(output_source_file_path.with_suffix('.Dummy_Root.0').as_posix()))


def replace_name(original_name, output_name, xml):
    pattern = re.compile(re.escape(original_name), re.IGNORECASE)
    return pattern.sub(output_name, xml)


def is_subdirectory(child, parent):
    try:
        child = Path(child).resolve()
        parent = Path(parent).resolve()
        return child.parts[:len(parent.parts)] == parent.parts
    except FileNotFoundError:
        return False


def generate_xml():
    try:
        base_directory = Path.cwd()  # Get the current working directory
        base_xml_path = Path(base_xml_entry.get())
        reference_xml_path = Path(reference_xml_entry.get())
        reference_name = reference_name_entry.get()
        output_dir_path = Path(output_dir_entry.get()).resolve()

        if not is_subdirectory(output_dir_path, base_directory):
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)  # Clear existing text
            output_text.insert(tk.END,
                               f"The output directory '{output_dir_path}' is not inside the base directory '{base_directory}'. Stopping generate_xml.\n")
            output_text.config(state=tk.DISABLED)
            print(
                f"The output directory '{output_dir_path}' is not inside the base directory '{base_directory}'. "
                f"Stopping generate_xml.")
            autoresize_text_widget(output_text)
            return

        output_dir_path = Path(output_dir_entry.get()).relative_to(base_directory)

        # Check file existence
        check_file_existence(base_xml_path)
        check_file_existence(reference_xml_path)
        check_file_existence(output_dir_path)

        # Perform other checks and actions as needed
        output_name = output_dir_path.name
        references_dict = create_variants(reference_name)
        outputs_dict = create_variants(output_name)
        output_paths_dict = create_variant_paths(output_dir_path, outputs_dict)
        for key, value in output_paths_dict.items():
            check_file_existence(value)
        print(
            "All files exist, beginning program, please make sure your Reference Head Name is properly typed as I can't "
            "check for that.")
        print(f"Reference Head Name: {reference_name}")
        print(f"Output Head Name: {output_name}")

        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)  # Clear existing text
        output_text.insert(tk.END,
                           "All files exist, beginning program, please make sure your Reference Head Name is properly "
                           "typed as I can't check for that.\n")
        output_text.insert(tk.END, f"Reference Head Name: {reference_name}\n")
        output_text.insert(tk.END, f"Output Head Name: {output_name}\n")
        autoresize_text_widget(output_text)

        reference_xml = ET.parse(str(reference_xml_path))
        reference_skel_bank = reference_xml.getroot().find(".//region[@id='SkeletonBank']")
        reference_mat_bank = reference_xml.getroot().find(".//region[@id='MaterialBank']")
        reference_tex_bank = reference_xml.getroot().find(".//region[@id='TextureBank']")
        reference_vis_bank = reference_xml.getroot().find(".//region[@id='VisualBank']")

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
        base_skel_bank = base_xml.getroot().find(".//region[@id='SkeletonBank']")
        base_mat_bank = base_xml.getroot().find(".//region[@id='MaterialBank']")
        base_tex_bank = base_xml.getroot().find(".//region[@id='TextureBank']")
        base_vis_bank = base_xml.getroot().find(".//region[@id='VisualBank']")

        create_resource_in_bank(reference_skeleton_node, base_skel_bank)
        create_resource_in_bank(reference_material_node, base_mat_bank)
        create_resource_in_bank(reference_texture_clea_node, base_tex_bank)
        create_resource_in_bank(reference_texture_hmvy_node, base_tex_bank)
        create_resource_in_bank(reference_texture_nm_node, base_tex_bank)
        create_resource_in_bank(reference_visual_node, base_vis_bank)

        # now there are many ways one could go about updating entries but...... lets do it the shitty way
        # replace UUIDs:
        str_base_xml = ET.tostring(base_xml.getroot(), encoding='utf-8').decode('utf-8')
        str_base_xml, skeleton_uuid = replace_id(reference_skeleton_node, str_base_xml)
        str_base_xml, material_uuid = replace_id(reference_material_node, str_base_xml)
        str_base_xml, texture_clea_uuid = replace_id(reference_texture_clea_node, str_base_xml)
        str_base_xml, texture_hmvy_uuid = replace_id(reference_texture_hmvy_node, str_base_xml)
        str_base_xml, texture_nm_uuid = replace_id(reference_texture_nm_node, str_base_xml)
        str_base_xml, visual_uuid = replace_id(reference_visual_node, str_base_xml)

        # replace source file paths:
        str_base_xml = replace_source_file_path(reference_skeleton_node, output_paths_dict['skeleton_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(reference_texture_clea_node, output_paths_dict['texture_clea_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(reference_texture_hmvy_node, output_paths_dict['texture_hmvy_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(reference_texture_nm_node, output_paths_dict['texture_nm_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(reference_visual_node, output_paths_dict['head_path'], str_base_xml)

        # replace template file paths:
        str_base_xml = replace_template_file_path(reference_skeleton_node, output_paths_dict['skeleton_path'],
                                                  str_base_xml)
        str_base_xml = replace_template_file_path(reference_visual_node, output_paths_dict['head_path'], str_base_xml)

        # replace names:
        str_base_xml = replace_name(reference_name, output_name, str_base_xml)

        # write XML
        with open("_merged.lsx", 'w', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            file.write(str_base_xml)
        print(f"Wrote file to _merged.lsx, make sure to copy the Visual Reference ID to your "
                                   f"CharacterCreationAppearanceVisuals.lsx")
        print(f"Visual Reference UUID: {visual_uuid}")
        output_text.insert(tk.END, f"Wrote file to _merged.lsx, make sure to copy the Visual Reference ID to your "
                                   f"CharacterCreationAppearanceVisuals.lsx\n")
        output_text.insert(tk.END, f"Visual Reference UUID: {visual_uuid}\n")
        output_text.config(state=tk.DISABLED)
        autoresize_text_widget(output_text)

    except FileNotFoundError as e:
        pass  # You can add your error handling code here


def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def browse_directory(entry):
    dir_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)


def autoresize_text_widget(widget):
    lines = widget.get(1.0, tk.END).count('\n') + 1
    widget.config(height=lines)

    # Calculate the maximum line length to set the width accordingly
    max_line_length = max(len(line) for line in widget.get(1.0, tk.END).splitlines())
    widget.config(width=max_line_length + 2)  # Add some extra space for visibility


root = tk.Tk()
root.title("XML Processing")
# Create and pack labels and entry fields
tk.Label(root, text="Base XML Path:").pack()
base_xml_entry = tk.Entry(root)
base_xml_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(base_xml_entry)).pack()

tk.Label(root, text="Reference XML Path:").pack()
reference_xml_entry = tk.Entry(root)
reference_xml_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(reference_xml_entry)).pack()

tk.Label(root, text="Reference Name:").pack()
reference_name_entry = tk.Entry(root)
reference_name_entry.pack()

tk.Label(root, text="Output Directory Path:").pack()
output_dir_entry = tk.Entry(root)
output_dir_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_directory(output_dir_entry)).pack()

# Create and pack the "Generate XML" button
generate_button = tk.Button(root, text="Generate XML", command=generate_xml)
generate_button.pack()

output_text = tk.Text(root, height=5, width=75, state=tk.DISABLED)
output_text.pack()

# Run the GUI
root.mainloop()

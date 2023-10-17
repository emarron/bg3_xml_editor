# def generate_xml():
    try:
        base_directory = Path.cwd()  # Get the current working directory
        base_xml_path = Path(base_xml_entry.get())
        reference_xml_path = Path(reference_xml_entry.get())
        reference_name = reference_name_entry.get()
        output_dir_path = Path(output_dir_entry.get()).resolve()
        output_name = output_name_entry.get()

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

        output_dir_path = Path(output_dir_entry.get()
                               ).relative_to(base_directory)

        # Check file existence
        check_file_existence(base_xml_path)
        check_file_existence(reference_xml_path)
        check_file_existence(output_dir_path)

        # Perform other checks and actions as needed
        references_dict = create_variants(reference_name)
        outputs_dict = create_variants(output_name)
        output_paths_dict = create_variant_paths(output_dir_path, outputs_dict)
        # check existence of file names
        for key, value in output_paths_dict.items():
            check_file_existence(value)
        print(
            "All files exist, beginning program, please make sure your Reference Body Name is properly typed as I can't "
            "check for that.")
        print(f"Reference Body Name: {reference_name}")
        print(f"Output Body Name: {output_name}")

        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)  # Clear existing text
        output_text.insert(tk.END,
                           "All files exist, beginning program, please make sure your Reference Body Name is properly "
                           "typed as I can't check for that.\n")
        output_text.insert(tk.END, f"Reference Body Name: {reference_name}\n")
        output_text.insert(tk.END, f"Output Body Name: {output_name}\n")
        autoresize_text_widget(output_text)

        reference_xml = ET.parse(str(reference_xml_path))
        # reference_skel_bank = reference_xml.getroot().find(".//region[@id='SkeletonBank']")
        reference_mat_bank = reference_xml.getroot().find(
            ".//region[@id='MaterialBank']")
        reference_tex_bank = reference_xml.getroot().find(
            ".//region[@id='TextureBank']")
        reference_vis_bank = reference_xml.getroot().find(
            ".//region[@id='VisualBank']")

        # for resource_node in reference_skel_bank.findall(".//node[@id='Resource']"):
        #     name = resource_node.find(".//attribute[@id='Name']").get("value")
        #     if references_dict['skeleton_name'].lower() == name.lower():
        #         reference_skeleton_node = resource_node
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
            if references_dict['texture_msk_name'].lower() == name.lower():
                reference_texture_msk_node = resource_node
            if references_dict['texture_nm_name'].lower() == name.lower():
                reference_texture_nm_node = resource_node
        for resource_node in reference_vis_bank.findall(".//node[@id='Resource']"):
            name = resource_node.find(".//attribute[@id='Name']").get("value")
            if references_dict['name'].lower() == name.lower():
                reference_visual_node = resource_node

        base_xml = ET.parse(str(base_xml_path))
        # this is for our generated node
        # base_skel_bank = base_xml.getroot().find(".//region[@id='SkeletonBank']")
        base_mat_bank = base_xml.getroot().find(
            ".//region[@id='MaterialBank']")
        base_tex_bank = base_xml.getroot().find(".//region[@id='TextureBank']")
        base_vis_bank = base_xml.getroot().find(".//region[@id='VisualBank']")

        # create_resource_in_bank(reference_skeleton_node, base_skel_bank)
        create_resource_in_bank(reference_material_node, base_mat_bank)
        create_resource_in_bank(reference_texture_clea_node, base_tex_bank)
        create_resource_in_bank(reference_texture_hmvy_node, base_tex_bank)
        create_resource_in_bank(reference_texture_msk_node, base_tex_bank)
        create_resource_in_bank(reference_texture_nm_node, base_tex_bank)
        create_resource_in_bank(reference_visual_node, base_vis_bank)

        # now there are many ways one could go about updating entries but...... lets do it the shitty way
        # replace UUIDs:
        str_base_xml = ET.tostring(
            base_xml.getroot(), encoding='utf-8').decode('utf-8')
        # str_base_xml, skeleton_uuid = replace_id(reference_skeleton_node, str_base_xml)
        str_base_xml, material_uuid = replace_id(
            reference_material_node, str_base_xml)
        str_base_xml, texture_clea_uuid = replace_id(
            reference_texture_clea_node, str_base_xml)
        str_base_xml, texture_msk_uuid = replace_id(
            reference_texture_msk_node, str_base_xml)
        str_base_xml, texture_hmvy_uuid = replace_id(
            reference_texture_hmvy_node, str_base_xml)
        str_base_xml, texture_nm_uuid = replace_id(
            reference_texture_nm_node, str_base_xml)
        str_base_xml, visual_uuid = replace_id(
            reference_visual_node, str_base_xml)

        # replace source file paths:
        # str_base_xml = replace_source_file_path(reference_skeleton_node, output_paths_dict['skeleton_path'],
        #                                         str_base_xml)
        str_base_xml = replace_source_file_path(reference_texture_clea_node, output_paths_dict['texture_clea_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(reference_texture_hmvy_node, output_paths_dict['texture_hmvy_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(reference_texture_msk_node, output_paths_dict['texture_msk_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(reference_texture_nm_node, output_paths_dict['texture_nm_path'],
                                                str_base_xml)
        str_base_xml = replace_source_file_path(
            reference_visual_node, output_paths_dict['body_path'], str_base_xml)

        # replace template file paths:
        # str_base_xml = replace_template_file_path(reference_skeleton_node, output_paths_dict['skeleton_path'],
        #                                           str_base_xml)
        str_base_xml = replace_template_file_path(
            reference_visual_node, output_paths_dict['body_path'], str_base_xml)

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


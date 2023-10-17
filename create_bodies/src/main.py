from pathlib import Path
from . import gui
from . import io
from . import parse
import xml.etree.ElementTree as ET
from lxml import etree


def generate_xml():
    try:
        # get our data
        base_directory = Path.cwd()
        base_xml_path = Path(gui.base_xml_entry.get())
        reference_xml_path = Path(gui.reference_xml_entry.get())
        reference_name = gui.reference_name_entry.get()
        output_dir_path = Path(gui.output_dir_entry.get()).resolve()
        output_name = gui.output_name_entry.get()

        # we must validate that our output dir is in our base dir
        if not io.validate_output_directory(output_dir_path, base_directory):
            return

        # further we need to validate the files we have exist
        io.validate_files_existence(
            [base_xml_path, reference_xml_path, output_dir_path])

        # create variants based on references, outputs, paths.
        output_dir_path = output_dir_path.relative_to(base_directory)
        references_dict = parse.create_variants(reference_name)
        outputs_dict = parse.create_variants(output_name)
        output_paths_dict = io.create_variant_paths(
            output_dir_path, outputs_dict)

        # validate output paths
        io.validate_files_existence(output_paths_dict.values())

        message = (
            f"All files exist, beginning program, please make sure your Reference Body Name is properly typed as I can't check for that.")
        print(message)

        # get reference
        reference_xml = etree.parse(str(reference_xml_path))

        # get reference's nodes
        reference_nodes = parse.extract_reference_nodes(
            reference_xml.getroot(), references_dict)

        # get base
        base_xml = etree.parse(str(base_xml_path))
        # Extract banks from base_xml
        base_banks = {
            'material': base_xml.getroot().find(".//region[@id='MaterialBank']"),
            'texture': base_xml.getroot().find(".//region[@id='TextureBank']"),
            'visual': base_xml.getroot().find(".//region[@id='VisualBank']")
        }

        # copy reference nodes into base banks
        parse.create_resources_in_banks(reference_nodes, base_banks)

        # replace with our data
        str_base_xml, visual_uuid = parse.replace_ids_and_paths_in_xml(
            etree.tostring(base_xml.getroot(), encoding='utf-8').decode('utf-8'),
            reference_nodes,
            output_paths_dict,
            reference_name,
            output_name

        )

        # output file
        io.write_xml_to_file(Path("_merged.lsx"), str_base_xml)

        # print success message and visual uuid
        message = (f"Reference Body Name: {reference_name}",
                   f"Output Body Name: {output_name}",
                   f"Wrote file to _merged.lsx, make sure to copy the Visual Reference ID to your CharacterCreationAppearanceVisuals.lsx",
                   f"Visual Reference UUID: {visual_uuid}")
        print(message)
    except FileNotFoundError as e:
        # Handle the exception (lol)
        pass

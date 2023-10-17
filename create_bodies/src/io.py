# future home of io
from pathlib import Path
from . import parse

def check_file_existence(file_path):
    # # make sure its a path
    # file_path = Path(file_path)
    # # for some reason this isn't case sensitive so here's a work around.
    # path_as_str = str(file_path)
    # if path_as_str not in str(file_path.resolve()):
    #     message = (f"The file '{file_path}' does not exist. Exiting program.")
    #     print(message)
    #     raise FileNotFoundError(message)
        file_path = Path(file_path)
        if not file_path.exists():
            message = (f"The file '{file_path}' does not exist. Exiting program.")
            print(message)
            raise FileNotFoundError(message)


def is_subdirectory(child, parent):
    try:
        child = Path(child).resolve()
        parent = Path(parent).resolve()
        return child.parts[:len(parent.parts)] == parent.parts
    except FileNotFoundError:
        return False


def validate_files_existence(paths):
    for path in paths:
        check_file_existence(path)


def validate_output_directory(output_dir_path, base_directory):
    if not is_subdirectory(output_dir_path, base_directory):
        message = (f"The output directory '{output_dir_path}' is not inside the base directory '{base_directory}'. "
                   f"Stopping generate_xml.")
        print(message)
        return False
    return True

# run a check to make sure all entities exist physically, shit code


def create_variant_paths(path, dictionary):
    if path.exists():
        paths_dict = {'texture_clea': (path / dictionary['texture_clea']).with_suffix(".DDS"),
                      'texture_hmvy': (path / dictionary['texture_hmvy']).with_suffix(".DDS"),
                      'texture_msk': (path / dictionary['texture_msk']).with_suffix(".DDS"),
                      'texture_nm': (path / dictionary['texture_nm']).with_suffix(".DDS"),
                      'body': (path / dictionary['name']).with_suffix(".GR2")}
        return paths_dict
    else:
        return None  # set up a break here or something

def write_xml_to_file(output_path, str_base_xml):
    if output_path.exists():
        with open(output_path, 'r', encoding='utf-8') as file:
            existing_data = file.read()
        merged_xml = parse.merge_xml(existing_data, str_base_xml)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            file.write(merged_xml)
    else:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            file.write(str_base_xml)


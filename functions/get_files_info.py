import os
from functools import reduce

def get_files_info(working_directory, directory="."):

    dir_path = os.path.abspath(
        os.path.join(working_directory, directory)
    )
    parent_path = os.path.abspath(working_directory)
    dir_name = 'current' if directory == "." else f"'{directory.rstrip("/")}'"

    intro_msg = f"Result for {dir_name} directory:\n"
    
    # user-input validation
    if not dir_path.startswith(parent_path):
        return intro_msg + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(dir_path):   return intro_msg + f'    Error: "{directory}" is not a directory'

    children = os.listdir(dir_path)
    try:
        get_file_info = with_abspath(dir_path)
        dir_contents = reduce(
            lambda acc,child: acc + get_file_info(child), children, ""
        ).rstrip("\n")
        return intro_msg + dir_contents
    except Exception as e:
        return f"Error listing files: {e}"

def with_abspath(abspath):
    def get_file_info(file):
        file_path = os.path.join(abspath, file)
        size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        file_name = os.path.basename(file_path)

        return f" - {file_name}: file_size={size} bytes, is_dir={is_dir}\n"
    return get_file_info
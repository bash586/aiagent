import os
from config import MAX_CHAR_LIMIT

def get_file_content(working_directory, file_path):
    file_abspath = os.path.abspath(
        os.path.join(working_directory, file_path)
    )
    parent_path = os.path.abspath(working_directory)

    # user-input validation
    if not file_abspath.startswith(parent_path):
        return  f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_abspath):   return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(file_abspath, "r") as f:
        contents = f.read(MAX_CHAR_LIMIT)
        if len(contents) >= MAX_CHAR_LIMIT:  contents += f'[...File "{file_path}" truncated at {MAX_CHAR_LIMIT} characters]'
        return contents
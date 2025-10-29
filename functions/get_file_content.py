import os
from config import MAX_CHAR_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    file_abspath = os.path.abspath(
        os.path.join(working_directory, file_path)
    )
    parent_path = os.path.abspath(working_directory)

    # user-input validation
    if not file_abspath.startswith(parent_path):
        return  f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_abspath):   return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file_abspath, "r") as f:
            contents = f.read(MAX_CHAR_LIMIT)
            if len(contents) >= MAX_CHAR_LIMIT:  contents += f'[...File "{file_path}" truncated at {MAX_CHAR_LIMIT} characters]'
            return contents
    except OSError as e:
        return f'Error: Failed to read "{file_path}": {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="returns python file in text format with maximum number of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The target file path that we want to return its content, relative to the working directory.",
            ),
        },
    ),
)
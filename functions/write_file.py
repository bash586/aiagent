import os
from google.genai import types

def write_file(working_directory, file_path, content):
    file_abspath = os.path.abspath(
        os.path.join(working_directory, file_path)
    )
    parent_path = os.path.abspath(working_directory)

    # user-input validation
    if not file_abspath.startswith(parent_path):
        return  f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_abspath):
        try:
            os.makedirs(os.path.dirname(file_abspath), exist_ok=True)
        except Exception as e:
            return f"Error: Failed to create {file_path}: {e}"
    if os.path.exists(file_abspath) and os.path.isdir(file_abspath):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(file_abspath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        return f'Error: failed to write to "{file_path}": {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Creates or overwrites a file inside the permitted working directory. "
        "If the file does not exist, it will be created automatically. "
        "Existing files are truncated before writing new content."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the target file (relative to working_directory). "
                    "The file will be created if it does not exist."
                ),
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="The new text content to write into the target file.",    
            ),
        },
    ),
)
    
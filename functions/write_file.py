import os

def write_file(working_directory, file_path, content):
    file_abspath = os.path.abspath(
        os.path.join(working_directory, file_path)
    )
    parent_path = os.path.abspath(working_directory)

    # user-input validation
    if not file_abspath.startswith(parent_path):
        return  f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_abspath):
        # write new file
        pass
    with open(file_abspath, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
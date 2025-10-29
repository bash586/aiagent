import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    
    file_abspath = os.path.abspath(
        os.path.join(working_directory, file_path)
    )
    parent_path = os.path.abspath(working_directory)

    # user-input validation
    if not file_abspath.startswith(parent_path):
        return  f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_abspath):
        return f'Error: File "{file_path}" not found.'
    if not file_abspath.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(args=["uv", "run", file_abspath, *args], timeout=30, text=True, cwd=parent_path)
    except subprocess.SubprocessError as e:
        return f"Error: executing Python file: {e}"
    exit_code = completed_process.returncode
    return f"""
STDOUT:{completed_process.stdout}
STDERR:{completed_process.stderr}
{
    ("Process exited with code " + str(exit_code)) if exit_code != 0 else "" 
}
""" if completed_process.stdout else "No output produced."

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file from a specified working directory using subprocess.run(), ensuring safety and returning the output, errors, and exit code in a single string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the target file path that needs to be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command line arguments needed to run python file",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument to pass to the executed Python file.",
                ),
                default=[],
            ),
        },
        required=['file_path'],
    ),
)
from functions import (
    get_file_content,
    get_files_info,
    run_python_file,
    write_file,
)
from google.genai import types
from config import *

all_functions = {
    "get_file_content": get_file_content.get_file_content,
    "get_files_info": get_files_info.get_files_info,
    "run_python_file": run_python_file.run_python_file,
    "write_file": write_file.write_file,
}

def call_function(function_call_part: types.FunctionCall, verbose=False)->types.Content:
    """Function used as a "Mediator" between tool functions (passed to AI model as tools) and the model itself

    Returns:
        types.Content:  post-execution feedback(function result OR error msg) sent to model
    """
    function_name = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    func = all_functions[function_name]
    if function_name not in all_functions: 
        return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name = function_name,
                    response = {'error': f"Unknown function: {function_name}"}
                ),
            ],
        )
    args["working_directory"] = WORKING_DIR
    
    function_result = func(**args)
    return types.Content(
        role="tool",
        parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
        ],
    )
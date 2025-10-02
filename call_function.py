from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

from config import HARDCODED_WD

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

function_dictionary = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}



def call_function(function_call_part, verbose=False):

    # function_call_part es un types.FunctionCall con .name y .args

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    try:
        if not function_call_part.name in function_dictionary:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

        
        function_call_part.args['working_directory'] = HARDCODED_WD
        result = function_dictionary[function_call_part.name](**function_call_part.args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )

    except Exception as e:
        print(f"Error: cannot call function {function_call_part.name} with arguments {function_call_part.args}")

    
    

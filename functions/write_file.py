import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:

        parent_dir = os.path.dirname(abs_file_path)
        
        os.makedirs(parent_dir, exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error writing in the file \"{file_path}\": {e}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites the previous content in the specified file with the content, constrained to the working directory. If the file doesn't exist then it creates the file and write in it. If the file_path isn't a file, it raises an error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to write the content in, relative to the working directory. If not provided, it returns an error message.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to overwrite the file given with.",
            ),
        },
    ),
)

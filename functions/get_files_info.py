import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # crea el path absoluto del join
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    # si no empieza con la direccion de working_directory 
    # -> directory accede fuera del working_directory
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    elif not os.path.isdir(full_path):
        return f'   Error: "{directory}" is not a directory'
    
    
    try:
        lines = []
        for c in sorted(os.listdir(full_path)):
            content_full_path = os.path.join(full_path, c)
            name = c
            is_dir = os.path.isdir(content_full_path)
            file_size = os.path.getsize(content_full_path)
            lines.append(
                f" - {name}: file_size={file_size} bytes, is_dir={is_dir}"
                )

        return '\n'.join(lines)
    except Exception as e:
        return f"Error listing files: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

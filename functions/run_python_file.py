import os
from subprocess import run
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    elif not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    elif not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # create list of commands for run
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)
        
        result = run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        return "\n".join(output) if output else "No output produced"

    except Exception as e:
        return f"Error: executing Python file: {e}"

    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file specified by file_path with the args passed, constrained to the working directory. If the file doesn't exist or isn't a .py file then it raises an error.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path of the python file to run, relative to the working directory. If not provided, it returns an error message.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments needed to be passed to the python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

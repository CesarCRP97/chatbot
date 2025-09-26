import os

def get_files_info(working_directory, directory="."):
    try:
        # crea el path absoluto del join
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        # si no empieza con la direccion de working_directory 
        # -> directory accede fuera del working_directory
        if not full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        elif not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        

        lines = ["Result for current directory:"]

        for c in sorted(os.listdir(full_path)):
            content_full_path = os.path.join(full_path, c)
            
            name = c
            is_dir = os.path.isdir(content_full_path)
            file_size = os.path.getsize(content_full_path)

            new_line = f" - {name}: file_size={file_size} bytes, is_dir={is_dir}"
            lines.append(new_line)

        return '\n'.join(lines)
    except Exception as e:
        return f"Error: {e}"
    
from functions.get_files_info import get_files_info


def run_tests():
    # Define tus tests como pares (working_directory, directory)
    tests = [
        ("calculator", "."),                         # directorio actual
        ("calculator", "pkg"),                        # subir un nivel
        ("calculator", "/bin"),                 # carpeta que no existe
        ("calculator", "../"),
    ]

    for i, (wd, d) in enumerate(tests):

        
        directory_name = d        
        if directory_name == ".":
            directory_name = "current"
        else:
            directory_name = f"'{directory_name}'"
        print(f"Result for {directory_name} directory:")
        result = get_files_info(wd, d)
        print(result)

if __name__ == "__main__":
    run_tests()
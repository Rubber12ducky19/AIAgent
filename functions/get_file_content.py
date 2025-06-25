import os
def get_file_content(working_directory, file_path):
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory,file_path))

    if abs_file_path.startswith(abs_working_directory) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(abs_file_path) != True:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    def read_file_content(abs_file_path):
        MAX_CHARS = 10000
        with open(abs_file_path, "r") as f:
            file_object = f.read(MAX_CHARS)
            if len(file_object) == MAX_CHARS:
                return file_object + (f'\n[...File "{file_path}" truncated at 10000 characters]')
            return file_object
    return read_file_content(abs_file_path)
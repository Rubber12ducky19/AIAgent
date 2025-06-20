import os

def get_files_info(working_directory, directory=None):  
    
    abs_working_directory = os.path.abspath(working_directory)
    #print (f"DEBUG: abs_working_directory = {abs_working_directory}")
    abs_directory = os.path.abspath(os.path.join(abs_working_directory,directory))
    #print (f"DEBUG: abs_directory = {abs_directory}")
    

    if abs_directory.startswith(abs_working_directory) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(abs_directory) != True:
        return f'Error: "{directory}" is not a directory'
    
    def get_files_in_directory(dir):
        result = []
        for file in os.listdir(dir):
            result.append(f"- {file}: file_size={os.path.getsize(os.path.join(abs_directory,file))}, is_dir={os.path.isdir(os.path.join(abs_directory,file))}")
        result_output = "\n".join(result)
        return result_output
    return get_files_in_directory(abs_directory)
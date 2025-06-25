import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory,file_path))
    if abs_file_path.startswith(abs_working_directory) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python3",file_path],
            cwd = working_directory,
            capture_output=True,
            text=True,
            timeout=30)
    
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process time out after 30 seconds"
    except FileNotFoundError:
        return "Error: executing Python file: Python interpreter not found"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if result.returncode != 0:
        return f"Process exited with code {result.returncode}"
    if result.stdout == "": 
        if result.stderr == "":
            return f"No output produced."

    return f"STDOUT: {result.stdout}\nSTDERR:{result.stderr}"

    
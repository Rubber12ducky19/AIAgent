import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
user_prompt = sys.argv
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt[1])]),]


system_prompt ="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
model_name = "gemini-2.0-flash-001"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files and directories",
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
schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory.",
            )
        }
    )
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory.",
            )
        }
    )
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory.",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="The content to be written or overwritten.",
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_contents,schema_run_python_file,schema_write_file,
    ]
)


if len(user_prompt) > 1:
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt))
    
    
    if response.function_calls:
        #If the list is NOT empty
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
    else:
        #If the list IS empty
        print(response.text)
    if "--verbose" in user_prompt:
        print(f"User prompt: {user_prompt[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
else:
    print(f"Error: No prompt provided.")
    sys.exit(1)
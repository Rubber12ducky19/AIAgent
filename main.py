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
#print (f"User prompt: {user_prompt[1]}")
if len(user_prompt) > 1:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,)

    print(response.text)
    if "--verbose" in user_prompt:
        print(f"User prompt: {user_prompt[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
else:
    print(f"Error: No prompt provided.")
    sys.exit(1)
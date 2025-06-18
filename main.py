import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
#When the program starts, load the environment variables from .env using dotenv and read the API key

from google import genai
#print(f"API Key: {api_key}") #Test to see if api-key exists.
client = genai.Client(api_key=api_key)
#Use the API to create a new instance of the Gemini Client
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
      contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
#generate_content() returns a GenerateContentResponse object.
print(response.text)

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

generated_content = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=messages
)
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}")

print(generated_content.text)
from google import genai

from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

for model in client.models.list():
    if "generateContent" in model.supported_actions and "preview" not in model.name and "tts" not in model.name and "image" not in model.name and "gemma" not in model.name:
        print(model.name)
import os, argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from function_calls import available_functions, call_function

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
for _ in range(20):

    generated_content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}")


    if generated_content.candidates:
        for candidate in generated_content.candidates:
            messages.append(candidate.content)

    if generated_content.function_calls:
        for function_call in generated_content.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)
            if not function_call_result.parts:
                raise Exception(f"Function Call Result is empty")
            if not isinstance(function_call_result.parts[0].function_response, types.FunctionResponse):
                raise Exception("Function Response type mismatch")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Function Response Empty")
            function_results = [function_call_result.parts[0]]
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
    else:
        print(generated_content.text)
        break

if generated_content.function_calls:
    print("End without final response")
    sys.exit(1)
import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import *
from call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(MAX_RETRY_ATTEMPTS):
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final Response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error: {str(e)}")

def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool)->types.GenerateContentResponse:

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file,
        ]
    )

    response = client.models.generate_content(
        model = MODEL_NAME,
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    for candidate in response.candidates:
        messages.append(candidate.content)

    function_calls = response.function_calls
    functions_responses = []
    for function_call_part in function_calls:

        function_call_result: types.Content = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        function_response_part = function_call_result.parts[0]
        functions_responses.append(function_response_part)
        print(f"-> {function_response_part.function_response.response}")
        
    messages.append(types.Content(
        role='user',
        parts=functions_responses
    ))

if __name__ == "__main__":
    main()
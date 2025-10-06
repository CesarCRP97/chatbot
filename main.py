import os
import sys


from call_function import available_functions, call_function
from prompts import system_prompt

from config import LIMIT_CYCLES


from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key= api_key)

    verbose = "--verbose" in sys.argv
    args = []

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    # Join all args to form the complete prompt
    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n")
    

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    for _ in range(LIMIT_CYCLES):
        try:
            response = generate_content(client, messages, verbose)
            is_text = False
            # Normalizado de response.function_calls
            calls = response.function_calls or []
            if len(calls) == 0 and response.text:
                print(response.text)
                is_text = True
                break
            else:
                for candidate in response.candidates:
                    # append the full candidate content to messages
                    if candidate.content:
                        messages.append(candidate.content)


        except Exception as e:
            print(f"Error during content generation: {e}")
            break




def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    calls = response.function_calls or []
    for function_call_part in calls:
        # call each function and append the result to messages
        result = call_function(function_call_part, verbose)

        tool_msg = types.Content(
                    role="user", 
                    parts=[
                        types.Part(
                            function_response= types.FunctionResponse(
                                name=function_call_part.name,
                                response={"result": result})
                        ),
                    ],
        )

        messages.append(tool_msg)

        if result.parts[0].function_response.response  is None:
            raise Exception("Not response produced when calling function")

        elif verbose:
            print(f"-> {result.parts[0].function_response.response}")

    return response


# For debugging: print the last n messages with their roles and number of parts
def debug_tail(messages, n=6):
    print("TAIL:", [(m.role, len(getattr(m, "parts", []) or [])) for m in messages[-n:]])


if __name__ == "__main__":
    main()

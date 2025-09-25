import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types



def verbose_output(user_prompt, response):
    print(f"\nUser prompt: {user_prompt}\n")
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main():
    # Si no ha introducido un comando, imprime error y termina.
    if len(sys.argv) < 2:
        print("This script needs a prompt to be used")
        sys.exit(1)

    prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key= api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages
        )

    
    if '--verbose' in sys.argv[2:]:
        verbose_output(prompt, response)
    else:
        print(response.text)
        

    


if __name__ == "__main__":
    main()

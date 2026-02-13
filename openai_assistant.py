"""

- This is a program created by Noah Sizemore

- The goal of this program is to create/use OpenAI API to correct users English.
The program should take input and output both text and speech to allow for multi-modal functionality.
The model instructions were provided by HayGen.


Credit to these websites:
- https://github.com/openai/openai-python
- https://docs.heygen.com/docs/integrate-with-opeanai-assistant

"""


import os
import sys
import openai
import pyttsx3
from openai import OpenAI

def main():
    # Standard implementation of gathering API key
    api_key = os.environ.get("OPENAI_API_KEY")

    # if API was not found
    if not api_key:
        print("Please provide an OpenAI API key in environment variable.")
        sys.exit(1)

    # initializing the client with API key and the TTS
    try:
        client = OpenAI(
            api_key=api_key
        )
        engine = pyttsx3.init()
    except Exception as e:
        print(f"There was an error initializing {e}")

    print("--- Tutor is active (Type \"exit\" to quit) ---")

    # Messaging client indefinitely until "exit"
    while True:
        message_client = str(input("\nYou: ")).strip()

        if message_client.lower() in ["exit", "quit"]:
            print("Thank you! Goodbye!")
            break

        if not message_client:
            continue

        # creating response with guidelines
        try:
            response = client.responses.create(
                model="gpt-5.2",
                # for this API, creating tutor to advise correct pronunciation of English
                instructions="""
                    You are an English tutor. Help students improve their language skills by:
                    - Correcting mistakes in grammar and vocabulary
                    - Explaining concepts with examples
                    - Engaging in conversation practice
                    - Providing learning suggestions
                    Be friendly, adapt to student's level, and always give concise answers.
                        """,
                input=message_client,
            )

            # print response in text to support multi-modal functionality
            print(f"Tutor: {response.output_text}")
            # creating text-to-speech output for correct pronunciation
            engine.say(response.output_text)
            engine.runAndWait()

        # error handling
        except openai.AuthenticationError:
            print("Invalid API key")
            break
        except openai.RateLimitError:
            print("Rate limit exceeded. Please wait")
        except Exception as e:
            print(f"There was an error processing {e}")
# run program
if __name__ == "__main__":
    main()
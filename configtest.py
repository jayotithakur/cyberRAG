import os

# Check if the OpenAI API key is set
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print("OpenAI API Key is set.")
else:
    print("OpenAI API Key is not set.")

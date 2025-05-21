import os
from dotenv import load_dotenv

# Load .env file contents into environment variables
load_dotenv()

def get_groq_api_key():
    """
    Returns the Groq API key stored in environment variables.
    Raises an error if the key is not found.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not set in environment variables.")
    return api_key

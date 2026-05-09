import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_BASE_URL = os.getenv("GITHUB_BASE_URL", "https://api.github.com")

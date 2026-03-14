
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Read variables
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
API_KEY = os.getenv("GROQ_API_KEY")


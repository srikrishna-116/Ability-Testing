from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from a local `.env` file (not committed to git).
# Copy `.env.example` to `.env` and fill in your real secrets.
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://gsrikrishna2004_db_user:KRISHNA@mycluster.hwwmkgu.mongodb.net/",
)
DB_NAME = os.getenv("DB_NAME", "adaptive_test")
API_key = os.getenv(
    "GROQ_API_KEY",
    "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",
)

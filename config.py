import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API Credentials
API_ID = int(os.getenv("API_ID", "28597362"))
API_HASH = os.getenv("API_HASH", "594f16e2cf9a6173bdf7a1cca942d94c")
SESSION_NAME = os.getenv("SESSION_NAME", "my_session")

# MySQL Configuration
DB_HOST = os.getenv("DB_HOST", "sql204.infinityfree.com")
DB_USER = os.getenv("DB_USER", "if0_37813242")
DB_PASSWORD = os.getenv("DB_PASSWORD", "5I1DrdS3tWi")
DB_NAME = os.getenv("DB_NAME", "if0_37813242_telegram")

# GitHub CSV URL (Optional)
GITHUB_CSV_URL = os.getenv("GITHUB_CSV_URL", "")

# Message Template
MESSAGE_TEMPLATE = os.getenv("MESSAGE_TEMPLATE", "Hello {name}, welcome!")

# Upload Folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

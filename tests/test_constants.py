import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("NUKI_API_TOKEN")
SMARTLOCK_ID = int(os.getenv("NUKI_SMARTLOCK_ID"))
TEST_EMAIL_PREFIX = os.getenv("TEST_EMAIL_PREFIX")
ORIGINAL_EMAIL_PREFIX = os.getenv("ORIGINAL_EMAIL_PREFIX")
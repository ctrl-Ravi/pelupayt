# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print("APIS:", os.getenv("APIS"))

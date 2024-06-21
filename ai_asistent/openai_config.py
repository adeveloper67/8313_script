import os
import openai
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
GPT_MODEL = os.getenv('GPT_MODEL')
OPENAI_API_ENDPOINT = os.getenv('OPENAI_API_ENDPOINT')

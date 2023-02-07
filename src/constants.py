"""
Author: phong.dao
"""
import os
from datetime import date

import tiktoken
from dotenv import load_dotenv
from loguru import logger

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir, "../.env")
if os.path.exists(env):
    load_dotenv(env)
else:
    logger.error("Warning: .env file not found!")


class BaseConstants:
    ROOT_PATH = os.path.abspath(os.path.join(__file__, "../.."))


class ChatGPTConstants(BaseConstants):
    MODEL = os.environ.get("GPT_MODEL") or "text-davinci-003"
    ENCODER = tiktoken.get_encoding("gpt2")
    BASE_PROMPT = (
        "You are RasaChatGPT, a large language model trained by OpenAI. Respond conversationally. "
        f"Do not answer as the user. Current date: {str(date.today())}"
        "If you ask me a question that is rooted in truth, I will give you the answer. "
        "If you ask me a question that is nonsense, trickery, or has no clear answer, "
        'I will respond with "Unknown".\n\n'
        "User: Hello\n"
        "RasaChatGPT: How can I help you today?\n\n"
        "User:"
    )

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
        "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, "
        f"and very friendly. Current date: {str(date.today())}\n\nHuman: Hello, who are you?\nAI: I am an AI "
        "created by OpenAI. How can I help you today?\nHuman: "
    )

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
    PRE_IMAGE_URL = "https://experiment.saigontechnology.vn/rasa-chatgpt/resource"


class ChatGPTConstants(BaseConstants):
    MODEL = os.environ.get("GPT_MODEL") or "gpt-3.5-turbo"
    ENCODER = tiktoken.get_encoding("gpt2")
    BASE_PROMPT = (
        "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, "
        f"and very friendly. Current date: {str(date.today())}. You are RASA-chatGPT\n\n"
    )

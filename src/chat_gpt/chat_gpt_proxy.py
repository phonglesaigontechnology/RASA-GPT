"""
Author: acheong08
Base on: https://github.com/acheong08/ChatGPT
"""
import os
from typing import Text

from revChatGPT.V2 import Chatbot

from src.chat_gpt.chat_gpt import ChatGPT


class ChatGPTProxy(ChatGPT):
    def __init__(self):
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        super().__init__()
        self.chatbot = Chatbot(email=os.getenv("CHATGPT_USER"), password=os.getenv("CHATGPT_PASSWORD"))

    async def ask(
        self,
        question: Text,
        temperature: float = 0.5,
    ):
        """
        Args:
            question:
            temperature:

        Returns: A response from ChatGPT
        Examples:
            >>>import asyncio
            >>>chat_gpt_ = ChatGPTProxy()
            >>>result = asyncio.run(chat_gpt_.ask("Hello"))
            >>>print(result)
        """
        response = ""
        async for line in self.chatbot.ask(question):
            response += line["choices"][0]["text"].replace("<|im_end|>", "")
        return str(response)

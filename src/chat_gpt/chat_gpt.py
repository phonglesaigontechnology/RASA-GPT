"""
Author: phong.dao
Base on https://platform.openai.com/examples/default-qa
"""
import os
from typing import Text

import openai
from loguru import logger

from src.constants import ChatGPTConstants

openai.api_key = os.getenv("OPENAI_APIKEY")


class ChatGPT:
    """
    A wrapper class contains useful methods for easier using chatGPT
    """

    def __init__(self, engine=None):
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        self.model = engine or ChatGPTConstants.MODEL

    @staticmethod
    def remove_suffix(input_string, suffix):
        """
        Remove suffix from string (Support for Python 3.8)
        """
        if suffix and input_string.endswith(suffix):
            return input_string[: -len(suffix)]
        return input_string

    @staticmethod
    def remove_prefix(input_string, prefixes):
        """
        Remove prefix from string (Support for Python 3.8)
        """
        for prefix in prefixes:
            if prefix and input_string.startswith(prefix):
                input_string = input_string[len(prefix) :]
        return input_string

    def _get_completion(
        self,
        prompt: str,
        temperature: float = 0.5,
        stream: bool = False,
    ):
        """
        Get the completion function
        """
        response = None
        for i in range(5):

            try:
                response = openai.Completion.create(
                    model=self.model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=500,
                    stop=["\n\n\n"],
                    stream=stream,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
            except Exception as e:
                logger.error("Server error!")
            if response is not None:
                return response
        raise Exception("ChatGPT API returned no choices")

    def _process_completion(
        self,
        completion: dict,
    ) -> Text:
        if completion.get("choices") is None:
            raise Exception("ChatGPT API returned no choices")
        if len(completion["choices"]) == 0:
            raise Exception("ChatGPT API returned no choices")
        if completion["choices"][0].get("text") is None:
            raise Exception("ChatGPT API returned no text")
        # return the first choice of response
        chatgpt_response = completion["choices"][0]["text"]
        chatgpt_response = self.remove_suffix(
            chatgpt_response,
            "<|im_end|>",
        )
        chatgpt_response = self.remove_prefix(
            chatgpt_response,
            [" AI:", "AI:"],
        )

        return chatgpt_response

    def ask(
        self,
        question: Text,
        temperature: float = 0.5,
    ) -> Text:
        """
        Send a request to ChatGPT and return the response
        """
        if question and not question.endswith("\n"):
            question += "\n"
        completion = self._get_completion(
            ChatGPTConstants.BASE_PROMPT + question,
            temperature,
        )
        return self._process_completion(
            completion,
        )

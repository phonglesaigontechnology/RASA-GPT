"""
Author: phong.dao
Base on https://platform.openai.com/examples/default-qa
"""
import os
import time
from typing import Text, List, Dict

import openai
import tiktoken
from loguru import logger
from openai.error import RateLimitError, APIError

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

    def create_chat_message(self, role, content):
        """
        Create a chat message with the given role and content.

        Args:
        role (str): The role of the message sender, e.g., "system", "user", or "assistant".
        content (str): The content of the message.

        Returns:
        dict: A dictionary containing the role and content of the message.
        """
        return {"role": role, "content": content}

    def generate_context(self, prompt, full_message_history, model):
        current_context = [
            self.create_chat_message("system", prompt),
            self.create_chat_message("system", f"The current time and date is {time.strftime('%c')}"),
        ]

        # Add messages from the full message history until we reach the token limit
        next_message_to_add_index = len(full_message_history) - 1
        insertion_index = len(current_context)
        # Count the currently used tokens
        current_tokens_used = count_message_tokens(current_context, model)
        return (
            next_message_to_add_index,
            current_tokens_used,
            insertion_index,
            current_context,
        )

    def chat_with_ai(self, prompt, user_input, full_message_history, token_limit):
        """Interact with the OpenAI API, sending the prompt, user input, message history,
        and permanent memory."""
        while True:
            try:
                """
                Interact with the OpenAI API, sending the prompt, user input,
                    message history, and permanent memory.

                Args:
                    prompt (str): The prompt explaining the rules to the AI.
                    user_input (str): The input from the user.
                    full_message_history (list): The list of all messages sent between the
                        user and the AI.
                    permanent_memory (Obj): The memory object containing the permanent
                      memory.
                    token_limit (int): The maximum number of tokens allowed in the API call.

                Returns:
                str: The AI's response.
                """
                # Reserve 1000 tokens for the response

                logger.debug(f"Token limit: {token_limit}")
                send_token_limit = token_limit - 1000

                (
                    next_message_to_add_index,
                    current_tokens_used,
                    insertion_index,
                    current_context,
                ) = self.generate_context(prompt, full_message_history, self.model)

                while current_tokens_used > 2500:
                    # remove memories until we are under 2500 tokens
                    (
                        next_message_to_add_index,
                        current_tokens_used,
                        insertion_index,
                        current_context,
                    ) = self.generate_context(prompt, full_message_history, self.model)

                current_tokens_used += count_message_tokens(
                    [self.create_chat_message("user", user_input)], self.model
                )  # Account for user input (appended later)

                while next_message_to_add_index >= 0:
                    # print (f"CURRENT TOKENS USED: {current_tokens_used}")
                    message_to_add = full_message_history[next_message_to_add_index]

                    tokens_to_add = count_message_tokens([message_to_add], self.model)
                    if current_tokens_used + tokens_to_add > send_token_limit:
                        break

                    # Add the most recent message to the start of the current context,
                    #  after the two system prompts.
                    current_context.insert(insertion_index, full_message_history[next_message_to_add_index])

                    # Count the currently used tokens
                    current_tokens_used += tokens_to_add

                    # Move to the next most recent message in the full message history
                    next_message_to_add_index -= 1

                # Append user input, the length of this is accounted for above
                current_context.extend([self.create_chat_message("user", user_input)])

                # Calculate remaining tokens
                tokens_remaining = token_limit - current_tokens_used
                # assert tokens_remaining >= 0, "Tokens remaining is negative.
                # This should never happen, please submit a bug report at
                #  https://www.github.com/Torantulino/Auto-GPT"

                # Debug print the current context
                logger.debug(f"Token limit: {token_limit}")
                logger.debug(f"Send Token Count: {current_tokens_used}")
                logger.debug(f"Tokens remaining for response: {tokens_remaining}")
                logger.debug("------------ CONTEXT SENT TO AI ---------------")
                for message in current_context:
                    # Skip printing the prompt
                    if message["role"] == "system" and message["content"] == prompt:
                        continue
                    logger.debug(f"{message['role'].capitalize()}: {message['content']}")
                    logger.debug("")
                logger.debug("----------- END OF CONTEXT ----------------")

                # TODO: use a model defined elsewhere, so that model can contain
                # temperature and other settings we care about
                assistant_reply = self.create_chat_completion(
                    model=self.model,
                    messages=current_context,
                    max_tokens=tokens_remaining,
                )

                # Update full message history
                full_message_history.append(self.create_chat_message("user", user_input))
                full_message_history.append(self.create_chat_message("assistant", assistant_reply))

                return assistant_reply
            except RateLimitError:
                # TODO: When we switch to langchain, this is built in
                print("Error: ", "API Rate Limit Reached. Waiting 10 seconds...")
                time.sleep(10)

    def create_chat_completion(
        self,
        messages: list,  # type: ignore
        model=None,
        temperature: float = 1,
        max_tokens=None,
    ) -> str:
        """Create a chat completion using the OpenAI API

        Args:
            messages (list[dict[str, str]]): The messages to send to the chat completion
            model (str, optional): The model to use. Defaults to None.
            temperature (float, optional): The temperature to use. Defaults to 0.9.
            max_tokens (int, optional): The max tokens to use. Defaults to None.

        Returns:
            str: The response from the chat completion
        """
        response = None
        num_retries = 10
        for attempt in range(num_retries):
            backoff = 2 ** (attempt + 2)
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                break
            except APIError as e:
                if e.http_status == 502:
                    pass
                else:
                    raise
                if attempt == num_retries - 1:
                    raise
            time.sleep(backoff)
        if response is None:
            raise RuntimeError(f"Failed to get response after {num_retries} retries")

        return response.choices[0].message["content"]


def count_message_tokens(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo-0301") -> int:
    """
    Returns the number of tokens used by a list of messages.

    Args:
        messages (list): A list of messages, each of which is a dictionary
            containing the role and content of the message.
        model (str): The name of the model to use for tokenization.
            Defaults to "gpt-3.5-turbo-0301".

    Returns:
        int: The number of tokens used by the list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        # !Note: gpt-3.5-turbo may change over time.
        # Returning num tokens assuming gpt-3.5-turbo-0301.")
        return count_message_tokens(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # !Note: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return count_message_tokens(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"num_tokens_from_messages() is not implemented for model {model}.\n"
            " See https://github.com/openai/openai-python/blob/main/chatml.md for"
            " information on how messages are converted to tokens."
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def count_string_tokens(string: str, model_name: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The text string.
        model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
        int: The number of tokens in the text string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(string))

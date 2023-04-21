"""
Author: phong.dao
"""
import logging
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from src.chat_gpt.chat_gpt import ChatGPT
from src.constants import ChatGPTConstants

logger = logging.getLogger(__name__)


class ActionAskChatGPT(Action):
    """
    Action ask Chatgpt.
    """

    def __init__(self):
        self.chatgpt = ChatGPT()

    def name(self) -> Text:
        return "action_ask_chatgpt"

    def get_conversation(
        self,
        tracker: Tracker,
    ):
        history = []
        for event in tracker.events:
            if event["event"] == "bot" and "text" in event and isinstance(event["text"], str):
                history.append({"role": "assistant", "content": event["text"]})
            elif event["event"] == "user" and "text" in event and isinstance(event["text"], str):
                history.append({"role": "user", "content": event["text"]})
        return history[:-1]

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        last_message = tracker.latest_message.get("text")
        try:
            history = self.get_conversation(tracker)
            response = self.chatgpt.chat_with_ai(ChatGPTConstants.BASE_PROMPT, last_message, history, 2000)
            dispatcher.utter_message(response)
        except Exception as e:
            logger.error(e)
            dispatcher.utter_message(template=f"utter_default")
        return []

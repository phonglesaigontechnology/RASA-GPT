"""
Author: phong.dao
"""
import logging
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from src.chat_gpt.chat_gpt import ChatGPT

logger = logging.getLogger(__name__)


class ActionAskChatGPT(Action):
    """
    Action ask Chatgpt.
    """

    def __init__(self):
        self.chatgpt = ChatGPT()

    def name(self) -> Text:
        return "action_ask_chatgpt"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        last_message = tracker.latest_message.get("text")
        try:
            response = self.chatgpt.ask(last_message)
            dispatcher.utter_message(response)
        except Exception as e:
            logger.error(e)
            dispatcher.utter_message(template=f"utter_default")
        return []

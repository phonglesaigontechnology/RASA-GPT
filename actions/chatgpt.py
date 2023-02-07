"""
Author: phong.dao
"""
from typing import Text, Dict, Any, List

import loguru
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from src.chat_gpt.chat_gpt import ChatGPT


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
        try:
            response = self.chatgpt.ask(tracker.latest_message.get("text"))
            dispatcher.utter_message(response)
        except Exception as e:
            loguru.logger.error(e)
            dispatcher.utter_message(template=f"utter_default")
        return []

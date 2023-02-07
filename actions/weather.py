"""
Author: phong.dao
"""
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from src.chat_gpt.chat_gpt import ChatGPT


class ActionAskWeather(Action):
    """
    Action ask Chatgpt.
    """

    def __init__(self):
        self.chatgpt = ChatGPT()

    def name(self) -> Text:
        return "action_ask_weather"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            location: Text = "DaNang",
    ) -> List[Dict]:

        dispatcher.utter_message(image=f"https://wttr.in/{location}.png")
        return []

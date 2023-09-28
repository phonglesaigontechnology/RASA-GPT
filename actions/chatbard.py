"""
Author: phong.dao
"""
import requests
import logging
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# from src.chat_gpt.chat_gpt import ChatGPT
from src.constants import ChatGPTConstants
from src.config import bard_configs
from bardapi import Bard

logger = logging.getLogger(__name__)
    

class ActionAskChatBard(Action):
    """
    Action ask Bard.
    """

    def __init__(self):
        timeout = int(bard_configs["TIMEOUT"])
        token = bard_configs["API_KEY"]
        # self.session = requests.Session()
        # self.session.headers = bard_configs["SESSION_HEADERS"]
        # self.session.cookies.set("__Secure-1PSID", token)
        # self.bard = Bard(token=token, session=self.session, timeout=timeout)
        try:
            self.bard = Bard(token=token, timeout=timeout)
        except Exception as e:
            logger.error("Please regenerate the API key on Bard")

    def name(self) -> Text:
        return "action_ask_chatbard"
    
    def chat_with_bard(self, message:str):
        """
        """
        try:
            response = self.bard.get_answer(message)
            logger.error(f"bard response: \n{response}")
            return response['content']
        except Exception as e:
            logger.error("Please regenerate the API key on Bard")
            return 0
            

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
        logger.error(f"chatbard message: {last_message}")
        try:
            history = self.get_conversation(tracker)
            logger.error(f"history message: {type(last_message)}")
            response = self.chat_with_bard(message=last_message)
            logger.error(f"response message: {response}")
            
            dispatcher.utter_message(response)
        except Exception as e:
            logger.error(e)
            dispatcher.utter_message(template=f"utter_default")
        return []

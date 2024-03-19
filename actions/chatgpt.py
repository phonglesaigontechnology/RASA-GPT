"""
Author: phong.dao
"""
from typing import Text, Dict, Any, List

import loguru
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import html
from src.chat_gpt.chat_gpt import ChatGPT


class ActionAskChatGPT(Action):
    """
    Action ask Chatgpt.
    """
    def __init__(self):
        self.chatgpt = ChatGPT()
        self.host = "experiment.saigontechnology.vn/ai-llm"
        self.uri = f"https://{self.host}/api/v1/chat"

    def name(self) -> Text:
        return "action_ask_chatbard"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        try:
            last_message = tracker.latest_message.get("text")
            inputs = {
                "input": last_message,
                "chat_history": []
            }
            response = requests.post("http://10.10.2.2:8013/chat", json=inputs)

            response = response.json().get("output")
            dispatcher.utter_message(response)
        except Exception as e:
            loguru.logger.error(e)
            dispatcher.utter_message(template=f"utter_default")
        return []
    
    def predict(self, user_input, history):
        request = {
            "user_input": user_input,
            "max_new_tokens": 250,
            "auto_max_new_tokens": False,
            "max_tokens_second": 0,
            "history": history,
            "mode": "chat",  # Valid options: 'chat', 'chat-instruct', 'instruct'
            "character": "Example",
            # "instruction_template": "Vicuna-v1.1",  # Will get autodetected if unset
            "your_name": "You",
            # 'name1': 'name of user', # Optional
            # 'name2': 'name of character', # Optional
            # 'context': 'character context', # Optional
            # 'greeting': 'greeting', # Optional
            # 'name1_instruct': 'You', # Optional
            # 'name2_instruct': 'Assistant', # Optional
            # 'context_instruct': 'context_instruct', # Optional
            # 'turn_template': 'turn_template', # Optional
            "regenerate": False,
            "_continue": False,
            "chat_instruct_command": 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',
            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            "preset": "None",
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.1,
            "typical_p": 1,
            "epsilon_cutoff": 0,  # In units of 1e-4
            "eta_cutoff": 0,  # In units of 1e-4
            "tfs": 1,
            "top_a": 0,
            "repetition_penalty": 1.18,
            "repetition_penalty_range": 0,
            "top_k": 40,
            "min_length": 0,
            "no_repeat_ngram_size": 0,
            "num_beams": 1,
            "penalty_alpha": 0,
            "length_penalty": 1,
            "early_stopping": False,
            "mirostat_mode": 0,
            "mirostat_tau": 5,
            "mirostat_eta": 0.1,
            "grammar_string": "",
            "guidance_scale": 1,
            "negative_prompt": "",
            "seed": -1,
            "add_bos_token": True,
            "truncation_length": 2048,
            "ban_eos_token": False,
            "custom_token_bans": "",
            "skip_special_tokens": True,
            "stopping_strings": [],
        }

        response = requests.post(self.uri, json=request, verify=False)

        if response.status_code == 200:
            result = response.json()["results"][0]["history"]
            print(json.dumps(result, indent=4))
            print()
            print(html.unescape(result["visible"][-1][1]))
            return result["visible"][-1][1]
        else:
            raise ValueError

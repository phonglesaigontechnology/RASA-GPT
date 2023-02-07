from typing import Dict, Text, Any, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
import random


class ActionAskEmail(Action):
    def name(self) -> Text:
        return "action_ask_email"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("previous_email"):
            dispatcher.utter_message(
                template=f"utter_ask_use_previous_email",
            )
        else:
            dispatcher.utter_message(template=f"utter_ask_email")
        return []


def _validate_email(
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
) -> Dict[Text, Any]:
    """Validate email is in system."""
    if not value:
        return {"email": None, "previous_email": None}
    elif isinstance(value, bool):
        value = tracker.get_slot("previous_email")

    return {"email": value}


class ValidateOpenIncidentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_open_incident_form"

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate email is in ticket system."""
        return _validate_email(value, dispatcher, tracker, domain)


class ActionOpenIncident(Action):
    def name(self) -> Text:
        return "action_open_incident"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Create an incident and return details or
        if local mode return incident details as if incident
        was created
        """

        priority = tracker.get_slot("priority")
        email = tracker.get_slot("email")
        problem_description = tracker.get_slot("problem_description")
        incident_title = tracker.get_slot("incident_title")
        confirm = tracker.get_slot("confirm")
        if not confirm:
            dispatcher.utter_message(template="utter_incident_creation_canceled")
            return [AllSlotsReset(), SlotSet("previous_email", email)]
        message = (
            f"An incident with the following details would be opened:"
            f"- email: {email}\n"
            f"- problem description: {problem_description}\n"
            f"- title: {incident_title}\n"
            f"- priority: {priority}"
        )
        dispatcher.utter_message(message)
        return [AllSlotsReset(), SlotSet("previous_email", email)]


class IncidentStatusForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_incident_status_form"

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate email is in ticket system."""
        return _validate_email(value, dispatcher, tracker, domain)


class ActionCheckIncidentStatus(Action):
    def name(self) -> Text:
        return "action_check_incident_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Look up all incidents associated with email address
        and return status of each"""

        email = tracker.get_slot("email")

        incident_states = {
            "New": "is currently awaiting triage",
            "In Progress": "is currently in progress",
            "On Hold": "has been put on hold",
            "Closed": "has been closed",
        }
        status = random.choice(list(incident_states.values()))
        message = (
            f"The most recent incident for {email} {status}"
        )
        dispatcher.utter_message(message)
        return [AllSlotsReset(), SlotSet("previous_email", email)]

"""
Author: phong.dao
"""
import os
from typing import Dict, Text, Any, List

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.types import DomainDict

from src.constants import BaseConstants
from src.employee_data.employee_searcher import EmployeeSearcher
from src.utils.get_configs import get_config

data_configs = get_config("data_configs")


class SearchEmployeeAction(Action):
    """
    Search employee
    """

    def __init__(self):
        super().__init__()
        self.employee_searcher = EmployeeSearcher(
            employee_data=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("employee_data", "employee_data.csv")),
            department=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("department", "department.csv")),
            department_employee=os.path.join(
                BaseConstants.ROOT_PATH, data_configs.get("department_employee", "department_employee.csv")
            ),
            department_manager=os.path.join(
                BaseConstants.ROOT_PATH, data_configs.get("department_manager", "department_manager.csv")
            ),
            title=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("title", "title.csv")),
        )

    def name(self) -> Text:
        return "action_search_employee"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        self.employee_searcher = EmployeeSearcher(
            employee_data=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("employee_data", "employee_data.csv")),
            department=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("department", "department.csv")),
            department_employee=os.path.join(
                BaseConstants.ROOT_PATH, data_configs.get("department_employee", "department_employee.csv")
            ),
            department_manager=os.path.join(
                BaseConstants.ROOT_PATH, data_configs.get("department_manager", "department_manager.csv")
            ),
            title=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("title", "title.csv")),
        )

        email = next(tracker.get_latest_entity_values("email"), None)
        name = next(tracker.get_latest_entity_values("employee_name"), None)
        if email:
            name = email.split("@")[0]
        if name:
            employee_info = self.employee_searcher.get_information_employee(name.lower())
            if employee_info is not None:
                dispatcher.utter_message(
                    f"Found {len(employee_info)} {name} in the company. Please see the details below: "
                )
                for index, row in employee_info.iterrows():
                    dispatcher.utter_message(
                        f"{row['fullname']} \n"
                        f"- Title: {row['title']} \n"
                        f"- Department: {row['department']} \n"
                        f"- Manager: {row['manager']} \n"
                        f"- Email: {row['email']} \n"
                    )
            else:
                dispatcher.utter_message(f"I can not find any employee has name {name}. Please try another.")
        else:
            dispatcher.utter_message(template=f"utter_ask_name")
        return []


class ShowEmployeeAction(Action):

    def __init__(self):
        self.employee_searcher = None

    def name(self) -> Text:
        return "action_show_list_of_employee"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        self.employee_searcher = EmployeeSearcher(
            employee_data=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("employee_data", "employee_data.csv")),
            department=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("department", "department.csv")),
            department_employee=os.path.join(
                BaseConstants.ROOT_PATH, data_configs.get("department_employee", "department_employee.csv")
            ),
            department_manager=os.path.join(
                BaseConstants.ROOT_PATH, data_configs.get("department_manager", "department_manager.csv")
            ),
            title=os.path.join(BaseConstants.ROOT_PATH, data_configs.get("title", "title.csv")),
        )
        preview_employees = self.employee_searcher.get_preview_of_list_employee(3)
        dispatcher.utter_message(f"We have total {len(self.employee_searcher.employee)} "
                                 f"employees. Here is some samples: ")

        dispatcher.utter_message(preview_employees.to_markdown(index=False))
        return []

"""
Author: phong.dao
"""
import os
from typing import Text, Tuple
import shutil
from htmlwebshot import WebShot
import pandas as pd
from loguru import logger

from src.constants import BaseConstants


class EmployeeSearcher:
    """
    Search employee infor
    """

    def __init__(
        self, employee_data: Text, department: Text, department_employee: Text, department_manager: Text, title: Text
    ):
        """

        Args:
            employee_data: Path to employee.csv
            department: Path to department.csv
            department_employee: Path to department_employee.csv
            department_manager: Path to department_manager.csv
            title: Path to title.csv
        """
        try:
            self.employee = pd.read_csv(employee_data)
            self.department = pd.read_csv(department)
            self.department_employee = pd.read_csv(department_employee)
            self.department_manager = pd.read_csv(department_manager)
            self.title = pd.read_csv(title)
        except Exception as e:
            logger.error(e)
        self.shot = WebShot()

    def _get_title(self, emp_id: int) -> Text:
        """

        Returns: the title of employee

        """
        title = self.title.loc[self.title["employee_id"] == emp_id, ["title"]]
        return title.values[0][0]

    def _get_department(self, emp_id: int) -> Tuple[Text, Text]:
        """

        Returns: the department that employee work in

        """
        department_id = (
            self.department_employee.loc[self.department_employee["employee_id"] == emp_id, ["department_id"]].values[0]
        )[0]
        department = self._get_department_name_from_id(department_id)[0]
        manager = self._get_manager(department_id)

        return department, manager

    def _get_department_name_from_id(self, depart_id) -> Text:
        """

        Args:
            depart_id:

        Returns:

        """
        department = self.department.loc[self.department["id"] == depart_id, ["dept_name"]].values
        return department[0]

    def _get_manager(self, depart_id: int) -> Text:
        """

        Returns: the department that employee work in

        """
        manager_id = self.department_manager.loc[
            self.department_manager["department_id"] == depart_id, ["employee_id"]
        ].values[0][0]

        manager_name = self._get_name_from_emp_id(manager_id)
        return manager_name

    def _get_name_from_emp_id(self, emp_id):
        """

        Args:
            emp_id:

        Returns:

        """

        name = self.employee.loc[self.employee["id"] == emp_id, ["first_name", "last_name"]]

        first_name, last_name = name[["first_name", "last_name"]].values[0]
        return f"{first_name} {last_name}"

    def get_preview_of_list_employee(self, n_employees: int) -> pd.DataFrame:
        """
        Returns: A head() of employee dataframe

        """
        employees = self.employee.sample(n_employees)
        employees["emp_code"] = employees.apply(lambda x: f"{x['first_name']}.{x['last_name']}", axis=1)
        return employees[["emp_code"]]

    def csv_to_image(self, df, name_file):
        """
        Convert dataframe to a image
        Args:
            df:
            name_file:

        Returns:

        """
        df_style = df.style.set_table_styles(
            [dict(selector="th", props=[("text-align", "center"), ("background-color", "#40466e"), ("color", "white")])]
        )
        df_style.set_properties(**{"text-align": "center"}).hide(axis="index")
        pd.set_option("colheader_justify", "center")

        html = df_style.to_html()
        output_path = self.shot.create_pic(
            html=html, size=(30*len(df), 300))
        shutil.move(output_path, os.path.join(BaseConstants.ROOT_PATH, f"static/{name_file}.jpg"))
        return f"{name_file}.jpg"

    def get_information_employee(self, first_name: Text = "", last_name: Text = ""):
        """

        Args:
            first_name:
            last_name:

        Returns: Information of employees.

        """
        assert first_name or last_name
        try:
            if first_name.count(" ") == 1 and not first_name.endswith(" ") and not first_name.startswith(" "):
                first_name, last_name = first_name.split()
            elif first_name.count(".") == 1 and not first_name.endswith(".") and not first_name.startswith("."):
                first_name, last_name = first_name.split(".")
            if first_name and last_name:
                employees = self.employee.loc[
                    (self.employee["first_name"] == first_name) & (self.employee["last_name"] == last_name),
                ]
            elif first_name:
                employees = self.employee.loc[self.employee["first_name"] == first_name]
            else:
                employees = self.employee.loc[self.employee["last_name"] == last_name]

            # Sort and get 10 employee
            employees = (
                employees.sort_values("hire_date", ascending=False).loc[:, employees.columns != "hire_date"].head(10)
            )
        except Exception as e:
            logger.error(e)
            return
        result = []
        if len(employees) == 0:
            return
        for employee_id, birth_date, first_name, last_name, gender, email in employees.values:
            try:
                employee_title = self._get_title(employee_id)
            except Exception as e:
                employee_title = ""
            try:
                employee_department, employee_manager = self._get_department(employee_id)
            except Exception as e:
                employee_department, employee_manager = "", ""

            result.append(
                {
                    "employee_id": employee_id,
                    "title": employee_title,
                    "department": employee_department,
                    "manager": employee_manager,
                    "fullname": f"{first_name} {last_name}",
                    "gender": gender,
                    "email": email,
                }
            )

        result = pd.DataFrame.from_records(result, index="employee_id")
        return result


if __name__ == "__main__":
    from src.utils.get_configs import get_config

    data_configs = get_config("data_configs")
    employee_searcher = EmployeeSearcher(
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
    df = employee_searcher.get_preview_of_list_employee(5)
    employee_searcher.csv_to_image(df, "asd")

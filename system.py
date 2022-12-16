"""
A very advanced employee management system

"""

import logging
from dataclasses import dataclass
from typing import List


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# noinspection PyTypeChecker
@dataclass
class Employee:
    """Basic employee representation"""

    first_name: str
    last_name: str
    role: str
    vacation_days: int = 25

    def __init__(self, first_name: str, last_name: str, role: str, vacation_days = 25):
        """

        :param first_name:
        :param last_name:
        :param role:
        :param vacation_days:
        Ініціалізація параметров та виклик функції, яка виконує валідацію значень.

        """

        if self.validate_str(first_name,last_name,role) and self.valadate_vacation_days(vacation_days):
            self.first_name= first_name.strip().capitalize()
            self.last_name=last_name.strip().capitalize()
            self.role=role.strip().capitalize()
            self.vacation_days = vacation_days

        else:
            raise (ValueError)

    @property
    def fullname(self):
        return self.first_name, self.last_name

    def __str__(self) -> str:
        """Return a string version of an instance"""

        return self.fullname

    def validate_str(self,*args) -> bool:
        """
        :param param: вхідний парамерт
        :return: True, якщо відповідає вимогам.

        Функція перевіряє вхідний параметр на відповідність типу та вимогам до написання імені особи.
        """
        res= True
        for arg in args:
            res = res and isinstance(arg, str) and arg.strip().isalpha()
        return res

    def valadate_vacation_days(self, days: int):
        """

        :param days:
        :return:
        Функція виконує валідацію кількості днів відпустки
        """
        return isinstance(days, int) and days> -1 and days < 32


    def take_holiday(self, payout: bool = False) -> None:
        """Take a single holiday or a payout vacation"""

        remaining = self.vacation_days
        if payout:
            if self.vacation_days < 5:
                msg = f"{self} have not enough vacation days. " \
                      f"Remaining days: %d. Requested: %d" % (remaining, 5)
                raise ValueError(msg)
            self.vacation_days -= 5
            msg = "Taking a holiday. Remaining vacation days: %d" % remaining
            logger.info(msg)
        else:
            if self.vacation_days < 1:
                remaining = self.vacation_days
                msg = f"{self} have not enough vacation days. " \
                      f"Remaining days: %d. Requested: %d" % (remaining, 1)
                raise ValueError(msg)
            self.vacation_days -= 1
            msg = "Taking a payout. Remaining vacation days: %d" % remaining
            logger.info(msg)


# noinspection PyTypeChecker
@dataclass
class HourlyEmployee(Employee):
    """Represents employees who are paid on worked hours base"""

    amount: int = 0
    hourly_rate: int = 50

    def log_work(self, hours: int) -> None:
        """Log working hours"""

        self.amount += hours


# noinspection PyTypeChecker
@dataclass
class SalariedEmployee(Employee):
    """Represents employees who are paid on a monthly salary base"""

    salary: int = 5000


# noinspection PyTypeChecker
class Company:
    """A company representation"""

    title: str
    employees: List[Employee] = []

    def get_ceos(self) -> List[Employee]:
        """Return employees list with role of CEO"""

        result = []
        for employee in self.employees:
            if employee.role == "CEO":
                result.append(employee)
        return result

    def get_managers(self) -> List[Employee]:
        """Return employees list with role of manager"""

        result = []
        for employee in self.employees:
            if employee.role == "manager":
                result.append(employee)
        return result

    def get_developers(self) -> List[Employee]:
        """Return employees list with role of developer"""

        result = []
        for employee in self.employees:
            if employee.role == "dev":
                result.append(employee)
        return result

    @staticmethod
    def pay(employee: Employee) -> None:
        """Pay to employee"""

        if isinstance(employee, SalariedEmployee):
            msg = (
                "Paying monthly salary of %.2f to %s"
            ) % (employee.salary, employee)
            logger.info(f"Paying monthly salary to {employee}")

        if isinstance(employee, HourlyEmployee):
            msg = (
                "Paying %s hourly rate of %.2f for %d hours"
            ) % (employee, employee.hourly_rate, employee.amount)
            logger.info(msg)

    def pay_all(self) -> None:
        """Pay all the employees in this company"""

        # TODO: implement this method

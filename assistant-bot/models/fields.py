import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Address(Field):
    """
    Represents a contact address stored as a single formatted string.
    """

    def __init__(self, value):
        # Normalize final address string before saving
        normalized_value = str(value).strip()

        # Prevent saving empty address
        if not normalized_value:
            raise ValueError("Address cannot be empty.")

        # Prevent saving unrealistically short address
        if len(normalized_value) < 5:
            raise ValueError("Address is too short.")

        super().__init__(normalized_value)


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Phone number must contain only digits and be 10 digits long.")
        self._value = new_value


class Email(Field):
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        normalized_value = str(new_value).strip()
        if not self.EMAIL_PATTERN.fullmatch(normalized_value):
            raise ValueError("Invalid email format.")
        self._value = normalized_value


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
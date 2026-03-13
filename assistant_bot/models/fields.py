import re
from datetime import datetime

class Field:
    def __init__(self, value):
        normalized = self.normalize(value)
        self.validate(normalized)
        self._value = normalized

    def __str__(self):
        return str(self._value)
    
    def normalize(self, value):
        return value
    
    def validate(self, value):
        return
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        normalized = self.normalize(new_value)
        self.validate(normalized)
        self._value = normalized

class Name(Field):
    def normalize(self, value):
        return value.strip()
    
    def validate(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")

class Address(Field):
    """
    Represents a contact address stored as a single formatted string.
    """

    def normalize(self, value):
        return super().normalize(value)
    
    def validate(self, value):
        if not value:
            raise ValueError("Address cannot be empty.")
        if len(value) < 5:
            raise ValueError("Address is too short.")

class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "Phone number must contain only digits and be 10 digits long.")

class Email(Field):
    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    
    def normalize(self, value):
        return value.strip().lower()
    
    def validate(self, value):
        if not self.EMAIL_PATTERN.fullmatch(value):
            raise ValueError("Invalid email format.")

class Birthday(Field):
    def normalize(self, value):
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            return None

    def validate(self, value):
        if not isinstance(value, datetime.date):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

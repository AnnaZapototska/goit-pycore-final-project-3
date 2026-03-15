import re
from datetime import datetime, date
from typing import Any, Optional


class Field:
    def __init__(self, value: Any) -> None:
        self._value: Optional[Any] = None
        self.value = value  # This will trigger normalization and validation

    def __str__(self) -> str:
        return str(self._value)

    def normalize(self, value: Any) -> Any:
        return value

    def validate(self, value: Any) -> None:
        return

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        normalized = self.normalize(new_value)
        self.validate(normalized)
        self._value = normalized


class Name(Field):
    def normalize(self, value: str) -> str:
        return value.strip()

    def validate(self, value: str) -> None:
        if not value:
            raise ValueError("Name cannot be empty.")


class Address(Field):
    """
    Represents a contact address stored as a single formatted string.
    """

    def normalize(self, value: str) -> str:
        return super().normalize(value)

    def validate(self, value: str) -> None:
        if not value:
            raise ValueError("Address cannot be empty.")
        if len(value) < 5:
            raise ValueError("Address is too short.")


class Phone(Field):
    def validate(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "Phone number must contain only digits and be 10 digits long."
            )


class Email(Field):
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def normalize(self, value: str) -> str:
        return value.strip().lower()

    def validate(self, value: str) -> None:
        if not self.EMAIL_PATTERN.fullmatch(value):
            raise ValueError("Invalid email format.")


class Birthday(Field):
    def normalize(self, value: str) -> Optional[date]:
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            return None

    def validate(self, value: Optional[date]) -> None:
        if value is None:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

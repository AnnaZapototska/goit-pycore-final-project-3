import re
from collections import UserDict
from datetime import datetime, timedelta
from .fields import *

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def remove_phone(self, phone: str):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                return
        raise ValueError(f"Phone number {phone} not found.")

    
    def edit_phone(self, old_phone: str, new_phone: str):
        for i, phone_obj in enumerate(self.phones):
            if phone_obj.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found.")
        

    def find_phone(self, phone: str):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj.value
        raise ValueError(f"Phone number {phone} not found.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"



class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find (self, name: str):
        return self.data.get(name)
    
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact with name {name} not found.")
        

    def get_upcoming_birthdays(self):

        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_this_year = record.birthday.value.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if 0 <= days_until_birthday <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append(
                    f"{record.name.value} -> {congratulation_date}"
                )

        if not upcoming_birthdays:
            return ["No upcoming birthdays within the next week."]

        return upcoming_birthdays
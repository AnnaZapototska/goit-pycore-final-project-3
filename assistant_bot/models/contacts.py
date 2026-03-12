from collections import UserDict
from datetime import datetime, timedelta
from .fields import *


class Record:
    def __init__(self, name, primary_phone):
        self.name = Name(name)
        self.phones = [Phone(primary_phone)]
        self.birthday = None
        self.email = None
        self.address = None

    @property
    def primary_phone(self):
        return self.phones[0]

    def set_name(self, name):
        self.name = Name(name)

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if any(p.value == phone_obj.value for p in self.phones):
            return
        self.phones.append(phone_obj)

    def set_primary_phone(self, phone):
        new_primary = Phone(phone)
        remaining = [p for p in self.phones if p.value != new_primary.value]
        self.phones = [new_primary, *remaining]

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, new_email):
        self.email = Email(new_email)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, new_address):
        self.address = Address(new_address)

    def remove_address(self):
        self.address = None

    def get_address(self):
        return self.address.value if self.address else "no address"

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
        additional_phones = "; ".join(p.value for p in self.phones[1:]) or "no additional phones"
        email_value = self.email.value if self.email else "no email"
        address_value = self.address.value if self.address else "no address"

        return (
            f"Contact name: {self.name.value}, primary phone: {self.primary_phone.value}, "
            f"additional phones: {additional_phones}, email: {email_value}, address: {address_value}"
        )


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.ensure_primary_phone_unique(record.primary_phone.value)
        self.data[record.primary_phone.value] = record

    def iter_records(self):
        return self.data.values()

    def find(self, primary_phone: str):
        try:
            normalized_phone = Phone(primary_phone).value
        except ValueError:
            return None
        return self.data.get(normalized_phone)

    def find_by_name(self, name: str):
        normalized_name = str(name).strip()
        return [r for r in self.iter_records() if r.name.value == normalized_name]

    def find_by_email(self, email: str):
        normalized_email = str(email).strip()
        for record in self.iter_records():
            if record.email and record.email.value == normalized_email:
                return record
        return None
    
    def find_by_phone(self, phone: str):
        normalized_phone = phone.strip()
        for record in self.data.values():
            for phone_obj in record.phones:
                if phone_obj.value == normalized_phone:
                    return record
        return None

    def find_by_selector(self, selector: str):
        record = self.find(selector)
        if record:
            return record
        return self.find_by_email(selector)

    def ensure_primary_phone_unique(self, phone: str, owner_phone: str | None = None):
        normalized_phone = Phone(phone).value
        existing_record = self.data.get(normalized_phone)

        if existing_record is None:
            return

        if owner_phone and existing_record.primary_phone.value == owner_phone:
            return

        raise ValueError("Primary phone must be unique.")

    def ensure_email_unique(self, email: str, owner_phone: str | None = None):
        existing_record = self.find_by_email(email)

        if existing_record is None:
            return

        if owner_phone and existing_record.primary_phone.value == owner_phone:
            return

        raise ValueError("Email must be unique.")

    def ensure_phone_unique(self, phone: str, owner_name: str | None = None):
        existing_record = self.find_by_phone(phone)
        if existing_record is None:
            return

        if owner_name is not None and existing_record.name.value == owner_name:
            return

        raise ValueError("Phone number must be unique.")
    
    def replace_primary_phone(self, old_phone: str, new_phone: str):
        record = self.find(old_phone)
        if record is None:
            raise ValueError("Contact does not exist.")

        normalized_old = record.primary_phone.value
        normalized_new = Phone(new_phone).value

        self.ensure_primary_phone_unique(normalized_new, owner_phone=normalized_old)

        record.set_primary_phone(normalized_new)

        del self.data[normalized_old]
        self.data[record.primary_phone.value] = record

    def search(self, query: str):
        normalized_query = query.strip().lower()
        results = []

        for record in self.iter_records():

            if normalized_query in record.name.value.lower():
                results.append(record)
                continue

            for phone in record.phones:
                if normalized_query == phone.value:
                    results.append(record)
                    break

            if record.email and normalized_query in record.email.value.lower():
                results.append(record)

        return results

    def delete(self, primary_phone: str):
        normalized_phone = Phone(primary_phone).value

        if normalized_phone in self.data:
            del self.data[normalized_phone]
        else:
            raise ValueError(f"Contact with primary phone {primary_phone} not found.")

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.iter_records():
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
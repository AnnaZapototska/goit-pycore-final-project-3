from collections import UserDict
from datetime import datetime, timedelta
from .fields import *


class Record:
    def __init__(self, name, primary_phone):
        self.name = Name(name)
        self.phones = [Phone(primary_phone)]
        self.birthday = None
        self.email = None

    @property
    def primary_phone(self):
        return self.phones[0]

    def set_name(self, name):
        self.name = Name(name)

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if any(existing_phone.value == phone_obj.value for existing_phone in self.phones):
            return
        self.phones.append(phone_obj)

    def set_primary_phone(self, phone):
        new_primary = Phone(phone)
        remaining_phones = [phone_obj for phone_obj in self.phones if phone_obj.value != new_primary.value]
        self.phones = [new_primary, *remaining_phones]

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, new_email):
        self.email = Email(new_email)

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
        additional_phones = "; ".join(p.value for p in self.phones[1:]) or "no additional phones"
        email = getattr(self, "email", None)
        email_value = email.value if email else "no email"
        return (
            f"Contact name: {self.name.value}, primary phone: {self.primary_phone.value}, "
            f"additional phones: {additional_phones}, email: {email_value}"
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
        return [record for record in self.iter_records() if record.name.value == normalized_name]

    def find_by_email(self, email: str):
        normalized_email = str(email).strip()
        for record in self.iter_records():
            record_email = getattr(record, "email", None)
            if record_email and record_email.value == normalized_email:
                return record
        return None

    def find_by_selector(self, selector: str):
        record = self.find(selector)
        if record is not None:
            return record
        return self.find_by_email(selector)

    def ensure_primary_phone_unique(self, phone: str, owner_phone: str | None = None):
        normalized_phone = Phone(phone).value
        existing_record = self.data.get(normalized_phone)
        if existing_record is None:
            return

        if owner_phone is not None and existing_record.primary_phone.value == owner_phone:
            return

        raise ValueError("Primary phone must be unique.")

    def ensure_email_unique(self, email: str, owner_phone: str | None = None):
        existing_record = self.find_by_email(email)
        if existing_record is None:
            return

        if owner_phone is not None and existing_record.primary_phone.value == owner_phone:
            return

        raise ValueError("Email must be unique.")

    def replace_primary_phone(self, old_phone: str, new_phone: str):
        record = self.find(old_phone)
        if record is None:
            raise ValueError("Contact does not exist.")

        normalized_old_phone = record.primary_phone.value
        normalized_new_phone = Phone(new_phone).value
        self.ensure_primary_phone_unique(normalized_new_phone, owner_phone=normalized_old_phone)

        record.set_primary_phone(normalized_new_phone)
        del self.data[normalized_old_phone]
        self.data[record.primary_phone.value] = record

    def delete(self, primary_phone: str):
        normalized_phone = Phone(primary_phone).value
        if normalized_phone in self.data:
            del self.data[normalized_phone]
        else:
            raise ValueError(f"Contact with primary phone {primary_phone} not found.")

    def migrate_legacy_records(self):
        migrated_records = {}

        for record in list(self.data.values()):
            if not hasattr(record, "email"):
                record.email = None

            if not getattr(record, "phones", None):
                raise ValueError(f"Contact {record.name.value} does not have a primary phone.")

            normalized_phones = []
            for phone_obj in record.phones:
                phone_value = phone_obj.value if hasattr(phone_obj, "value") else str(phone_obj)
                validated_phone = Phone(phone_value).value
                if validated_phone not in normalized_phones:
                    normalized_phones.append(validated_phone)

            if not normalized_phones:
                raise ValueError(f"Contact {record.name.value} does not have a primary phone.")

            record.phones = [Phone(phone_value) for phone_value in normalized_phones]
            primary_phone = record.primary_phone.value
            if primary_phone in migrated_records:
                raise ValueError("Primary phone must be unique.")

            record_email = getattr(record, "email", None)
            if record_email is not None:
                for existing_record in migrated_records.values():
                    existing_email = getattr(existing_record, "email", None)
                    if existing_email and existing_email.value == record_email.value:
                        raise ValueError("Email must be unique.")

            migrated_records[primary_phone] = record

        self.data = migrated_records

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

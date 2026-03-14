from collections import UserDict, UserList
from datetime import datetime, timedelta
from .fields import Name, Phone, Email, Address, Birthday
from tabulate import tabulate
from utils.colors import AnsiColor

class Record:
    def __init__(self, name, primary_phone, record_id=None):
        """
        name: string
        primary_phone: string
        record_id: string (optional) - assigned by AddressBook if None
        """
        self.id = record_id            # sequential ID assigned later
        self.name = Name(name)
        self.phones = [Phone(primary_phone)]
        self.email = None
        self.birthday = None
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
        additional_phones = "; ".join(
            p.value for p in self.phones[1:]) or "no additional phones"
        email_value = self.email.value if self.email else "no email"
        address_value = self.address.value if self.address else "no address"

        return (
            f"Contact name: {self.name.value}, "
            f"primary phone: {self.primary_phone.value}, "
            f"additional phones: {additional_phones}, "
            f"email: {email_value}, "
            f"address: {address_value}"
        )
    
    def to_colored_dict(self, text_color=AnsiColor.CYAN, border_color=AnsiColor.WHITE):
        """
        Convert the Record to a dict with ANSI color codes for terminal display.
        """
        def color_value(value):
            if value is None:
                return None
            return AnsiColor.RESET + text_color + ' ' + str(value) + AnsiColor.RESET + border_color
        
        result = {
            "id": color_value(self.id),
            "name": color_value(self.name.value),
            "phones": "\n".join([color_value(p.value) for p in self.phones]) if self.phones != [] else None,
            "email": color_value(self.email.value) if self.email else None,
            "birthday": color_value(self.birthday.value.strftime("%d.%m.%Y")) if self.birthday else None,
            "address": color_value(self.address.value) if self.address else None,
        }
        
        return result

    def to_table(self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN):
        """
        Convert the Record to a table with ANSI color codes for terminal display.
        """
        return AnsiColor.wrap(tabulate([self.to_colored_dict(text_color, border_color)], headers="keys", tablefmt="fancy_grid"), border_color)

class RecordList(UserList):
    def to_table(self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN):
        """
        Convert the list of records to a table with ANSI color codes for terminal display.
        """
        return AnsiColor.wrap(tabulate([record.to_colored_dict(text_color, border_color) for record in self.data], headers="keys", tablefmt="fancy_grid"), border_color)

class AddressBook(UserDict):

    def add_record(self, record: Record):
        """
        Adds a new contact to the AddressBook.
        Assigns a sequential ID if the record has no ID.
        Ensures primary phone is unique.
        """
        # Ensure the primary phone is unique
        self.ensure_primary_phone_unique(record.primary_phone.value)

        # Generate a sequential ID if record.id is None
        if record.id is None:
            if self.data:
                # Take the max existing ID and add 1
                next_id = str(max(int(rid) for rid in self.data.keys()) + 1)
            else:
                next_id = "1"
            record.id = next_id

        # Store the record using the ID as the key
        self.data[record.id] = record


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
        return [r for r in self.iter_records() if r.name.value ==
                normalized_name]

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
        """
        Find a contact by ID, primary phone, or email.
        """
        normalized_selector = str(selector).strip()

        if normalized_selector in self.data:
            return self.data[normalized_selector]

        for record in self.data.values():
            if record.primary_phone.value == normalized_selector:
                return record
            
        for record in self.data.values():
            if record.email and record.email.value == normalized_selector:
                return record

        # Not found
        return None

    def ensure_primary_phone_unique(
            self,
            phone: str,
            owner_phone: str | None = None):
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


    def replace_primary_phone(self, record_id: str, new_phone: str):
        """
        Change the primary phone of a contact.
        Requires the contact's ID.
        Ensures the new phone is unique.
        """

        record = self.data.get(record_id)
        if record is None:
            raise ValueError("Contact ID not found.")

        normalized_new = Phone(new_phone).value

        self.ensure_primary_phone_unique(
            normalized_new,
            owner_phone=record.primary_phone.value
        )
        record.set_primary_phone(normalized_new)

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

        return RecordList(results)

    def delete(self, record_id: str):
        normalized_id = str(record_id).strip()

        if normalized_id in self.data:
            del self.data[normalized_id]
        else:
            raise ValueError("Contact ID not found.")



    def get_upcoming_birthdays(self, days_ahead=7):
        """
        Returns a list of contacts whose birthday is within the next `days_ahead` days.
        """
        today = datetime.today().date()
        upcoming = []

        for record in self.iter_records():
            if record.birthday is None:
                continue

            # Birthday in the current year
            bday_this_year = record.birthday.value.replace(year=today.year)

            # If birthday already passed this year, consider next year
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            days_until_bday = (bday_this_year - today).days

            if 0 <= days_until_bday <= days_ahead:
                # Adjust for weekend
                congr_date = bday_this_year
                if congr_date.weekday() == 5:  # Saturday
                    congr_date += timedelta(days=2)
                elif congr_date.weekday() == 6:  # Sunday
                    congr_date += timedelta(days=1)

                upcoming.append((congr_date, record))

        upcoming.sort(key=lambda x: x[0])
        return [f"{rec.name.value} -> {date.strftime('%d.%m.%Y')}" for date, rec in upcoming]
    
    
    def to_colored_dict(self, text_color=AnsiColor.BRIGHT_CYAN, border_color=AnsiColor.BRIGHT_WHITE):
        return [record.to_colored_dict(text_color, border_color) for record in self.data.values()]
    
    def to_table(self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN):
        return AnsiColor.wrap(tabulate(self.to_colored_dict(text_color, border_color), headers="keys", tablefmt="fancy_grid"), border_color)

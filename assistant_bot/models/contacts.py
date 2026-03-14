from collections import UserDict, UserList
from datetime import datetime, timedelta
from tabulate import tabulate
from .fields import Name, Phone, Email, Address, Birthday
from utils.colors import AnsiColor, table_cell_colored_value


class Record:
    MAX_PHONES = 3  # Max phones per contact

    def __init__(self, name, primary_phone, record_id=None):
        """
        name: string
        primary_phone: string
        record_id: string (optional) - assigned by AddressBook if None
        """
        self.id = record_id  # sequential ID assigned later
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

    def get_phones_list(self):
        return [phone.value for phone in self.phones]

    def get_phones_display(self):
        return "; ".join(self.get_phones_list())

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if any(existing_phone.value == phone_obj.value for existing_phone in self.phones):
            raise ValueError("This phone already exists for the contact.")
        if len(self.phones) >= self.MAX_PHONES:
            raise ValueError("A contact can have maximum 3 phone numbers.")
        self.phones.append(phone_obj)

    def set_primary_phone(self, phone):
        new_primary = Phone(phone)
        if not any(p.value == new_primary.value for p in self.phones):
            raise ValueError("New primary phone must already exist in the contact phones list.")
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
        normalized_phone = Phone(phone).value
        if len(self.phones) == 1 and self.phones[0].value == normalized_phone:
            raise ValueError("A contact must have at least one phone number.")
        for phone_obj in self.phones:
            if phone_obj.value == normalized_phone:
                self.phones.remove(phone_obj)
                return
        raise ValueError(f"Phone number {phone} not found.")

    def edit_phone(self, old_phone: str, new_phone: str):
        normalized_old = Phone(old_phone).value
        new_phone_obj = Phone(new_phone)
        if any(p.value == new_phone_obj.value for p in self.phones if p.value != normalized_old):
            raise ValueError("This phone already exists for the contact.")
        for i, p in enumerate(self.phones):
            if p.value == normalized_old:
                self.phones[i] = new_phone_obj
                return
        raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone: str):
        normalized_phone = Phone(phone).value
        for p in self.phones:
            if p.value == normalized_phone:
                return p.value
        raise ValueError(f"Phone number {phone} not found.")

    def __str__(self):
        email_value = self.email.value if self.email else "no email"
        address_value = self.address.value if self.address else "no address"
        birthday_value = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "no birthday"
        return (
            f"ID: {self.id}, "
            f"Contact name: {self.name.value}, "
            f"phones: {self.get_phones_display()}, "
            f"email: {email_value}, "
            f"birthday: {birthday_value}, "
            f"address: {address_value}"
        )

    def to_colored_dict(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """
        Convert the Record to a dict with ANSI color codes for terminal display.
        """

        return {
            "id": table_cell_colored_value(self.id, text_color, border_color),
            "name": table_cell_colored_value(self.name.value, text_color, border_color),
            "phones": "\n".join(
                [
                    table_cell_colored_value(p.value, text_color, border_color)
                    for p in self.phones
                ]
            )
            if self.phones != []
            else None,
            "email": table_cell_colored_value(
                self.email.value, text_color, border_color
            )
            if self.email
            else None,
            "birthday": table_cell_colored_value(
                self.birthday.value.strftime("%d.%m.%Y"), text_color, border_color
            )
            if self.birthday
            else None,
            "address": table_cell_colored_value(
                self.address.value, text_color, border_color
            )
            if self.address
            else None,
        }

    def to_table(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """
        Convert the Record to a table with ANSI color codes for terminal display.
        """
        return AnsiColor.wrap(
            tabulate(
                [self.to_colored_dict(text_color, border_color)],
                headers="keys",
                tablefmt="fancy_grid",
            ),
            border_color,
        )



class RecordList(UserList):
    def to_table(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """
        Convert the list of records to a table with ANSI color codes for terminal display.
        """

        if not self.data:
            return AnsiColor.wrap("No contacts found.", text_color)

        return AnsiColor.wrap(
            tabulate(
                [
                    record.to_colored_dict(text_color, border_color)
                    for record in self.data
                ],
                headers="keys",
                tablefmt="fancy_grid",
            ),
            border_color,
        )


class AddressBook(UserDict):
    def add_record(self, record: Record):
        for phone_obj in record.phones:
            self.ensure_phone_unique(phone_obj.value)
        if record.id is None:
            next_id = str(max([int(rid) for rid in self.data.keys()] + [0]) + 1)
            record.id = next_id
        self.data[record.id] = record

    def iter_records(self):
        return self.data.values()

    def find(self, primary_phone: str):
        return self.find_by_phone(primary_phone)

    def find_by_id(self, record_id: str):
        return self.data.get(str(record_id).strip())

    def find_by_name(self, name: str):
        normalized_name = str(name).strip()
        return [r for r in self.iter_records() if r.name.value == normalized_name]

    def find_by_email(self, email: str):
        normalized_email = str(email).strip()
        for r in self.iter_records():
            if r.email and r.email.value == normalized_email:
                return r
        return None

    def find_by_phone(self, phone: str):
        try:
            normalized = Phone(phone).value
        except ValueError:
            return None
        for r in self.data.values():
            for p in r.phones:
                if p.value == normalized:
                    return r
        return None

    def find_by_selector(self, selector: str):
        r = self.find_by_id(selector) or self.find_by_phone(selector) or self.find_by_email(selector)
        return r

    def ensure_primary_phone_unique(self, phone: str, owner_record_id: str | None = None):
        self.ensure_phone_unique(phone, owner_record_id)

    def ensure_email_unique(self, email: str, owner_record_id: str | None = None):
        r = self.find_by_email(email)
        if r is None or (owner_record_id is not None and r.id == owner_record_id):
            return
        raise ValueError("Email must be unique.")

    def ensure_phone_unique(self, phone: str, owner_record_id: str | None = None):
        r = self.find_by_phone(phone)
        if r is None or (owner_record_id is not None and r.id == owner_record_id):
            return
        raise ValueError("Phone number must be unique.")

    def replace_primary_phone(self, record_id: str, new_phone: str):
        record = self.data.get(str(record_id).strip())
        if record is None:
            raise ValueError("Contact ID not found.")
        normalized_new = Phone(new_phone).value
        self.ensure_phone_unique(normalized_new, owner_record_id=record.id)
        if any(p.value == normalized_new for p in record.phones):
            record.set_primary_phone(normalized_new)
            return
        record.phones[0] = Phone(normalized_new)

    def search(self, query: str):
        q = query.strip().lower()
        results = []
        for r in self.iter_records():
            if q in r.name.value.lower() or (r.email and q in r.email.value.lower()) or any(q in p.value.lower() for p in r.phones):
                results.append(r)
        return RecordList(results)

    def delete(self, record_id: str):
        rid = str(record_id).strip()
        if rid in self.data:
            del self.data[rid]
        else:
            raise ValueError("Contact ID not found.")

    def get_upcoming_birthdays(self, days_ahead=7):
        """
        Returns a list of tuples (record, birthday_date) for contacts whose
        birthday is within the next `days_ahead` days.
        Adjusts birthdays falling on weekends to Monday.
        Sorted by upcoming date (soonest first).
        """
        today = datetime.today().date()
        upcoming = []

        for record in self.iter_records():
            if record.birthday is None:
                continue

            # Birthday in current year
            bday_this_year = record.birthday.value.replace(year=today.year)

            # If birthday already passed, consider next year
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

                upcoming.append((record, congr_date))

        # Sort by upcoming date
        upcoming.sort(key=lambda x: x[1])

        return upcoming  


    def to_colored_dict(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        return [
            record.to_colored_dict(text_color, border_color)
            for record in self.data.values()
        ]

    def to_table(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        return AnsiColor.wrap(
            tabulate(
                self.to_colored_dict(text_color, border_color),
                headers="keys",
                tablefmt="fancy_grid",
            ),
            border_color,
        )

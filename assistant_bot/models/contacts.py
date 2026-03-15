from collections import UserDict, UserList
from datetime import datetime, timedelta, date
from tabulate import tabulate
from assistant_bot.models.fields import Name, Phone, Email, Address, Birthday
from assistant_bot.utils.colors import AnsiColor, table_cell_colored_value
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


class Record:
    MAX_PHONES = 3  # Max phones per contact

    def __init__(
        self, name: str, primary_phone: str, record_id: Optional[str] = None
    ) -> None:
        """
        name: string
        primary_phone: string
        record_id: string (optional) - assigned by AddressBook if None
        """
        self.id: Optional[str] = record_id  # sequential ID assigned later
        self.name: Name = Name(name)
        self.phones: List[Phone] = [Phone(primary_phone)]
        self.email: Optional[Email] = None
        self.birthday: Optional[Birthday] = None
        self.address: Optional[Address] = None
        self.groups: Set[str] = set()

    @property
    def primary_phone(self) -> Phone:
        return self.phones[0]

    def set_name(self, name: str) -> None:
        self.name = Name(name)

    def get_phones_list(self) -> List[str]:
        return [phone.value for phone in self.phones]

    def get_phones_display(self) -> str:
        return "; ".join(self.get_phones_list())

    def add_phone(self, phone: str) -> None:
        phone_obj = Phone(phone)
        if any(
            existing_phone.value == phone_obj.value for existing_phone in self.phones
        ):
            raise ValueError("This phone already exists for the contact.")
        if len(self.phones) >= self.MAX_PHONES:
            raise ValueError("A contact can have maximum 3 phone numbers.")
        self.phones.append(phone_obj)

    def set_primary_phone(self, phone: str) -> None:
        new_primary = Phone(phone)
        if not any(p.value == new_primary.value for p in self.phones):
            raise ValueError(
                "New primary phone must already exist in the contact phones list."
            )
        remaining = [p for p in self.phones if p.value != new_primary.value]
        self.phones = [new_primary, *remaining]

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def edit_email(self, new_email: str) -> None:
        self.email = Email(new_email)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def edit_address(self, new_address: str) -> None:
        self.address = Address(new_address)

    def remove_address(self) -> None:
        self.address = None

    def get_address(self) -> str:
        return self.address.value if self.address else "no address"

    def remove_phone(self, phone: str) -> None:
        normalized_phone = Phone(phone).value
        if len(self.phones) == 1 and self.phones[0].value == normalized_phone:
            raise ValueError("A contact must have at least one phone number.")
        for phone_obj in self.phones:
            if phone_obj.value == normalized_phone:
                self.phones.remove(phone_obj)
                return
        raise ValueError(f"Phone number {phone} not found.")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        normalized_old = Phone(old_phone).value
        new_phone_obj = Phone(new_phone)
        if any(
            p.value == new_phone_obj.value
            for p in self.phones
            if p.value != normalized_old
        ):
            raise ValueError("This phone already exists for the contact.")
        for i, p in enumerate(self.phones):
            if p.value == normalized_old:
                self.phones[i] = new_phone_obj
                return
        raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone: str) -> str:
        normalized_phone = Phone(phone).value
        for p in self.phones:
            if p.value == normalized_phone:
                return p.value
        raise ValueError(f"Phone number {phone} not found.")

    def __str__(self) -> str:
        email_value = self.email.value if self.email else "no email"
        address_value = self.address.value if self.address else "no address"
        birthday_value = (
            self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "no birthday"
        )
        return (
            f"ID: {self.id}, "
            f"Contact name: {self.name.value}, "
            f"phones: {self.get_phones_display()}, "
            f"email: {email_value}, "
            f"birthday: {birthday_value}, "
            f"address: {address_value}"
            f"groups: {self.get_groups_display()}"
        )

    def to_colored_dict(
        self,
        text_color: AnsiColor = AnsiColor.BRIGHT_GREEN,
        border_color: AnsiColor = AnsiColor.BRIGHT_CYAN,
    ) -> Dict[str, Any]:
        """
        Convert the Record to a dict with ANSI color codes for terminal display.
        """

        return {
            "id": table_cell_colored_value(self.id, text_color, border_color),
            "name": table_cell_colored_value(self.name.value, text_color, border_color),
            "groups": table_cell_colored_value(
                self.get_groups_display(), text_color, border_color
            ),
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
        self,
        text_color: AnsiColor = AnsiColor.BRIGHT_GREEN,
        border_color: AnsiColor = AnsiColor.BRIGHT_CYAN,
    ) -> str:
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

    def ensure_groups_initialized(self) -> None:
        if not hasattr(self, "groups") or self.groups is None:
            self.groups = set()
        elif not isinstance(self.groups, set):
            self.groups = set(self.groups)

    def add_group(self, group: str) -> None:
        self.ensure_groups_initialized()
        normalized_group = str(group).strip().lower()
        if not normalized_group:
            raise ValueError("Group name cannot be empty.")
        self.groups.add(normalized_group)

    def remove_group(self, group: str) -> None:
        self.ensure_groups_initialized()
        normalized_group = str(group).strip().lower()
        if normalized_group not in self.groups:
            raise ValueError(f"Contact is not in group '{normalized_group}'.")
        self.groups.remove(normalized_group)

    def clear_groups(self) -> None:
        self.ensure_groups_initialized()
        self.groups.clear()

    def has_group(self, group: str) -> bool:
        self.ensure_groups_initialized()
        normalized_group = str(group).strip().lower()
        return normalized_group in self.groups

    def get_groups_list(self) -> List[str]:
        self.ensure_groups_initialized()
        return sorted(self.groups)

    def get_groups_display(self) -> str:
        self.ensure_groups_initialized()
        return ", ".join(self.get_groups_list()) if self.groups else "no groups"


class RecordList(UserList):
    def to_table(
        self,
        text_color: AnsiColor = AnsiColor.BRIGHT_GREEN,
        border_color: AnsiColor = AnsiColor.BRIGHT_CYAN,
    ) -> str:
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
    DEFAULT_GROUPS: Set[str] = {"family", "work", "friends"}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ensure_groups_storage()

    def ensure_groups_storage(self) -> None:
        if not hasattr(self, "available_groups") or self.available_groups is None:
            self.available_groups = set(self.DEFAULT_GROUPS)
        elif not isinstance(self.available_groups, set):
            self.available_groups = set(self.available_groups)

        if not self.available_groups:
            self.available_groups = set(self.DEFAULT_GROUPS)

        for record in self.data.values():
            if hasattr(record, "ensure_groups_initialized"):
                record.ensure_groups_initialized()
            elif not hasattr(record, "groups") or record.groups is None:
                record.groups = set()

    def normalize_group_name(self, group: str) -> str:
        normalized_group = str(group).strip().lower()
        if not normalized_group:
            raise ValueError("Group name cannot be empty.")
        return normalized_group

    def add_group(self, group: str) -> None:
        self.ensure_groups_storage()
        normalized_group = self.normalize_group_name(group)
        if normalized_group in self.available_groups:
            raise ValueError(f"Group '{normalized_group}' already exists.")
        self.available_groups.add(normalized_group)

    def get_all_groups(self) -> List[str]:
        self.ensure_groups_storage()
        return sorted(self.available_groups)

    def ensure_group_exists(self, group: str) -> str:
        self.ensure_groups_storage()
        normalized_group = self.normalize_group_name(group)
        if normalized_group not in self.available_groups:
            raise ValueError(f"Group '{normalized_group}' does not exist.")
        return normalized_group

    def delete_group(self, group: str) -> None:
        self.ensure_groups_storage()
        normalized_group = self.ensure_group_exists(group)
        self.available_groups.remove(normalized_group)

        for record in self.iter_records():
            record.ensure_groups_initialized()
            if normalized_group in record.groups:
                record.groups.remove(normalized_group)

    def add_contact_to_group(self, record_id: str, group: str) -> None:
        self.ensure_groups_storage()
        record = self.find_by_id(record_id)
        if record is None:
            raise ValueError(f"Contact ID {record_id} not found.")
        normalized_group = self.ensure_group_exists(group)
        if normalized_group in record.groups:
            raise ValueError(f"Contact already belongs to group '{normalized_group}'.")
        record.add_group(normalized_group)

    def add_contacts_to_group(
        self, group: str, record_ids: List[str]
    ) -> Dict[str, List[str]]:
        self.ensure_groups_storage()
        normalized_group = self.ensure_group_exists(group)
        added: List[str] = []
        skipped: List[str] = []

        for record_id in record_ids:
            record = self.find_by_id(record_id)
            if record is None:
                skipped.append(f"{record_id} (not found)")
                continue
            if normalized_group in record.groups:
                skipped.append(f"{record_id} (already in group)")
                continue
            record.add_group(normalized_group)
            added.append(record_id)

        return {"group": normalized_group, "added": added, "skipped": skipped}

    def delete_contact_group(self, record_id: str, group: str) -> None:
        self.ensure_groups_storage()
        record = self.find_by_id(record_id)
        if record is None:
            raise ValueError(f"Contact ID {record_id} not found.")
        normalized_group = self.normalize_group_name(group)
        record.remove_group(normalized_group)

    def delete_contact_groups(self, record_id: str) -> None:
        self.ensure_groups_storage()
        record = self.find_by_id(record_id)
        if record is None:
            raise ValueError(f"Contact ID {record_id} not found.")
        record.clear_groups()

    def find_contacts_by_group(self, group: str) -> RecordList:
        self.ensure_groups_storage()
        normalized_group = self.ensure_group_exists(group)
        results = [
            record
            for record in self.iter_records()
            if normalized_group in record.groups
        ]
        return RecordList(results)

    def add_record(self, record: Record) -> None:
        for phone_obj in record.phones:
            self.ensure_phone_unique(phone_obj.value)
        if record.id is None:
            next_id = str(max([int(rid) for rid in self.data.keys()] + [0]) + 1)
            record.id = next_id
        self.data[record.id] = record

    def iter_records(self) -> Iterable[Record]:
        return self.data.values()

    def find(self, primary_phone: str) -> Optional[Record]:
        return self.find_by_phone(primary_phone)

    def find_by_id(self, record_id: str) -> Optional[Record]:
        return self.data.get(str(record_id).strip())

    def find_by_name(self, name: str) -> List[Record]:
        normalized_name = str(name).strip()
        return [r for r in self.iter_records() if r.name.value == normalized_name]

    def find_by_email(self, email: str) -> Optional[Record]:
        normalized_email = str(email).strip()
        for r in self.iter_records():
            if r.email and r.email.value == normalized_email:
                return r
        return None

    def find_by_phone(self, phone: str) -> Optional[Record]:
        try:
            normalized = Phone(phone).value
        except ValueError:
            return None
        for r in self.data.values():
            for p in r.phones:
                if p.value == normalized:
                    return r
        return None

    def find_by_selector(self, selector: str) -> Optional[Record]:
        r = (
            self.find_by_id(selector)
            or self.find_by_phone(selector)
            or self.find_by_email(selector)
        )
        return r

    def ensure_primary_phone_unique(
        self, phone: str, owner_record_id: Optional[str] = None
    ) -> None:
        self.ensure_phone_unique(phone, owner_record_id)

    def ensure_email_unique(
        self, email: str, owner_record_id: Optional[str] = None
    ) -> None:
        r = self.find_by_email(email)
        if r is None or (owner_record_id is not None and r.id == owner_record_id):
            return
        raise ValueError("Email must be unique.")

    def ensure_phone_unique(
        self, phone: str, owner_record_id: Optional[str] = None
    ) -> None:
        r = self.find_by_phone(phone)
        if r is None or (owner_record_id is not None and r.id == owner_record_id):
            return
        raise ValueError("Phone number must be unique.")

    def replace_primary_phone(self, record_id: str, new_phone: str) -> None:
        record = self.data.get(str(record_id).strip())
        if record is None:
            raise ValueError("Contact ID not found.")
        normalized_new = Phone(new_phone).value
        self.ensure_phone_unique(normalized_new, owner_record_id=record.id)
        if any(p.value == normalized_new for p in record.phones):
            record.set_primary_phone(normalized_new)
            return
        record.phones[0] = Phone(normalized_new)

    def search(self, query: str) -> RecordList:
        q = query.strip().lower()
        results: List[Record] = []
        for r in self.iter_records():
            if (
                q in r.name.value.lower()
                or (r.email and q in r.email.value.lower())
                or any(q in p.value.lower() for p in r.phones)
            ):
                results.append(r)
        return RecordList(results)

    def delete(self, record_id: str) -> None:
        rid = str(record_id).strip()
        if rid in self.data:
            del self.data[rid]
        else:
            raise ValueError("Contact ID not found.")

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> List[Tuple[Record, date]]:
        """
        Returns a list of tuples (record, birthday_date) for contacts whose
        birthday is within the next `days_ahead` days.
        Adjusts birthdays falling on weekends to Monday.
        Sorted by upcoming date (soonest first).
        """
        today = datetime.today().date()
        upcoming: List[Tuple[Record, date]] = []

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
        self,
        text_color: AnsiColor = AnsiColor.BRIGHT_GREEN,
        border_color: AnsiColor = AnsiColor.BRIGHT_CYAN,
    ) -> List[Dict[str, Any]]:
        return [
            record.to_colored_dict(text_color, border_color)
            for record in self.data.values()
        ]

    def to_table(
        self,
        text_color: AnsiColor = AnsiColor.BRIGHT_GREEN,
        border_color: AnsiColor = AnsiColor.BRIGHT_CYAN,
    ) -> str:
        return AnsiColor.wrap(
            tabulate(
                self.to_colored_dict(text_color, border_color),
                headers="keys",
                tablefmt="fancy_grid",
            ),
            border_color,
        )

"""Module that contains classes for working with address book."""

import re

from collections import UserDict

class Field:
    """
    Represents a base field object.

    Args:
        value (any): The value.

    Attributes:
        value (any): The value of the field.
    """
    def __init__(self, value: any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Field):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class Name(Field):
    """
    Represents a name field.

    Args:
        name (str): The name field.

    Attributes:
        name (str): The name field.
    """
    def __init__(self, name: str) -> None:
        super().__init__(name)


class Phone(Field):
    """Represents a phone number field.

    Args:
        value (str): The phone number value.

    Attributes:
        value (str): The normalized phone number value.

    Raises:
        PhoneFormatError: If the phone number format is not valid.
    """
    pattern = r"[+\d]"
    country_code = "38"

    def __init__(self, raw_phone: str) -> None:

        phone = "".join(re.findall(self.pattern, raw_phone))

        if not phone.startswith("+"):
            phone = re.sub(fr"^({self.country_code})?", f"+{self.country_code}", phone)

        if len(phone) != 13:
            raise PhoneFormatError("Invalid phone number.")

        super().__init__(phone)

class Record:
    """
    Represents a contact record with a name and a list of phone numbers.

    Args:
        name (str): The name of the contact.

    Attributes:
        name (Name): The name of the contact.
        phones (list): A list of phone numbers associated with the contact.
    """

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str):
        """
        Adds a phone number to the contact's list of phone numbers.

        Args:
            phone (Phone): The phone number to add.

        Raises:
            ContactError: If the phone number already exists in the contact's list of phone numbers.
        """
        if self.find_phone(phone):
            raise ContactError("Phone number already exists.")

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """
        Removes a phone number from the contact's list of phone numbers.
        Won't raise error if phone number not exist.

        Args:
            phone (str): The phone number to remove.
        """
        existing_phone = self.find_phone(phone)
        if existing_phone:
            self.phones.remove(existing_phone)

    def edit_phone(self, phone: str, new_phone: str):
        """
        Edits a phone number in the contact's list of phone numbers.

        Args:
            phone (str): The phone number to edit.
            new_phone (str): The new phone number.

        Raises:
            ContactError: If the phone number to edit does not exist in the contact's phones list,
                        or if the new phone number already exists in the contact's phones list.
        """
        existing_phone = self.find_phone(phone)
        if not existing_phone:
            raise ContactError("No such phone number.")

        if self.find_phone(new_phone):
            raise ContactError("New phone number already exists.")

        self.phones[self.phones.index(existing_phone)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """
        Finds a phone number in the contact's list of phone numbers.

        Args:
            phone (str): The phone number to check.

        Returns:
            Phone: The phone number if found, None otherwise.
        """
        target_phone = Phone(phone)
        return next((p for p in self.phones if p == target_phone), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    """
    A class representing an address book.

    This class extends the UserDict class to provide functionality for managing contacts in an address book.

    Attributes:
        data (dict): A dictionary to store the contacts in the address book.

    Methods:
        add_record(record: Record): Adds a record to the address book.
        find(name: Name) -> Record: Finds a record in the address book by name.
        delete(name: Name): Deletes a record from the address book by name.
    """

    def add_record(self, record: Record) -> None:
        """
        Adds a record to the data dictionary.

        Args:
            record (Record): The record to be added.

        Raises:
            ContactError: If the contact already exists in the data dictionary.
        """
        if record.name in self.data:
            raise ContactError("Contact already exists.")

        self.data[record.name] = record

    def find(self, name: str, raise_error: bool = True) -> Record | None:
        """
        Find a contact by name.

        Args:
            name (str): The name of the contact to find.
            raise_error (bool): Whether to raise an error if the contact is not found.

        Returns:
            Record: The contact record associated with the given name.
            None if not found if raise_error is False.

        Raises:
            ContactError: If no contact with the given name is found. Only if raise_error is True.
        """
        name = Name(name)

        if name not in self.data:
            if raise_error:
                raise ContactError("No such contact.")
            return None

        return self.data[name]

    def delete(self, name: str):
        """
        Deletes the specified name from the data dictionary.
        Won't raise error if phone number not exist.

        Args:
            name (str): The name to be deleted.
        """
        name = Name(name)

        if name in self.data:
            del self.data[name]

class ContactError(Exception):
    """Custom exception for contact errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class PhoneFormatError(Exception):
    """Custom exception for phone number format errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

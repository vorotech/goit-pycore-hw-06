"""Module for handling commands."""

from decorators import input_error
from models import Record, AddressBook

book = AddressBook()

@input_error(strerror="Invalid command. Usage: add [ім'я] [номер телефону]")
def add_contact_number(*args) -> str:
    """Adds a contact to the phonebook or adds a new phone number to contact."""
    name, phone = args

    record = book.find(name, raise_error=False)
    if not record:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)

    return "Contact number added."

@input_error(strerror="Invalid command. Usage: change [ім'я] [номер телефону] [новий номер телефону]")
def change_contact_number(*args) -> str:
    """Change a contact."""
    name, phone, new_phone = args
    record = book.find(name)
    record.edit_phone(phone, new_phone)

    return "Contact number updated."

@input_error(strerror="Invalid command. Usage: delete [ім'я]")
def delete_contact(*args) -> str:
    """Deletes a contact."""
    (name,) = args
    book.delete(name)

    return "Contact deleted."


@input_error(strerror="Invalid command. Usage: contact [ім'я]")
def get_contact(*args) -> Record:
    """Gets a contact."""
    (name,) = args
    record = book.find(name)
    return record

def get_all_contacts() -> list:
    """Gets all contacts."""
    return [str(record) for record in book.data.values()]

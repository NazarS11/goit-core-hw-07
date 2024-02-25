from collections import UserDict
import re
from datetime import datetime as dtdt
from datetime import timedelta as td


class Field:                                                                                                    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):                                                                                     
    def __init__(self, value):
        self.value = value


class Phone(Field):                                                                                     

    def __init__(self, value):
       self.value = value

    @property
    def value(self):
        return self._value

    @value.setter                                                                                             
    def value(self, new_value):
        if re.fullmatch(r'\d{10}', new_value):
            self._value = new_value
        else:
            raise ValueError(f"Phone number {new_value} should consist of 10 digits")


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter                                                                                             
    def value(self, new_value):
        if re.fullmatch(r'(\d{2}\.){2}\d{4}', new_value):
            self._value = dtdt.strptime(new_value, "%d.%m.%Y").date()
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:                                                                                          
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):                                                                                         
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def add_birthday(self, birthday:str):                                                                           
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else: raise ValueError(f"Contact {self.name} has already added birthday {self.birthday}")
        
    def find_phone(self, phone: str): 
        for existing_phone in self.phones:
            if phone == existing_phone.value:
                return existing_phone
        return None
        
    def add_phone(self, phone:str):                                                                           
        if not self.find_phone(phone):
            self.phones.append(Phone(phone))
            
    def remove_phone(self, phone:str):  
        phone_for_remove = self.find_phone(phone)                                                                              
        if phone_for_remove:
            self.phones.remove(phone_for_remove)

    def edit_phone(self, old:str, new:str):
        phone_for_edit = self.find_phone(old)     
        if phone_for_edit:
            phone_for_edit.value = new
        else: raise ValueError(f"Contact {self.name} has no phone number: {old}")


class AddressBook(UserDict):

    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        for key in self.data.keys():
            if key == name:
                return self.data[key]

    def delete(self, name: str):
        for key in self.data.keys():
            if key == name:
                del self.data[key]
                break

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
           return "Enter the argument for the command."
        except KeyError:
            return "No such contact in the list."        
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(address_book, name, phone):
    existing_contact = address_book.find(name)
    if existing_contact:
        existing_contact.add_phone(phone)
        for name, record in address_book.data.items():
            print(f"key: {name}: value {record}")
    else:
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        for name, record in address_book.data.items():
            print(f"key: {name}: value {record}")

@input_error
def change_phone(address_book, name, old_phone, new_phone):
    existing_contact = address_book.find(name)
    if existing_contact:
        existing_contact.edit_phone(old_phone, new_phone)
    else:
        print(f"{name} contact is not in the address book")

@input_error
def add_birthday(address_book, name, birthday):
    existing_contact = address_book.find(name)
    if existing_contact:
        existing_contact.add_birthday(birthday)
    else:
        print(f"{name} contact is not in the address book")

@input_error
def show_birthday(address_book, name):
    existing_contact = address_book.find(name)
    if existing_contact:
        print(f"Name: { existing_contact.name.value}, Birthday: {existing_contact.birthday}")
    else:
        print (f"{name} contact is not in the address book")

@input_error
def show_phone(address_book, name):
    existing_contact = address_book.find(name)
    if existing_contact:
        for phone in existing_contact.phones:
            print(f"Name: {existing_contact.name.value}, contact data: {phone.value}")
    else:
        print (f"{name} contact is not in the address book")

@input_error
def display_contacts(address_book):
    for name, record in address_book.data.items():
        print(f"Name: {name}, contact data: {record}")

@input_error
def show_birthdays(address_book):
    today = dtdt.now().date()
    congrat_list = []
    for name, record in address_book.data.items():
        if record.birthday:
            birthday = record.birthday.value
            latest_birth_date = dtdt(today.year, birthday.month, birthday.day).date()
            if today < latest_birth_date and (latest_birth_date - today).days < 8:
                if latest_birth_date.weekday() == 6:
                    congrat_list.append({'name':name,'congratulation_date':(latest_birth_date + td(days=1)).strftime("%Y.%m.%d")})
                elif latest_birth_date.weekday() == 5:
                    congrat_list.append({'name':name,'congratulation_date':(latest_birth_date + td(days=2)).strftime("%Y.%m.%d")})
                else:
                    congrat_list.append({'name':name,'congratulation_date':latest_birth_date.strftime("%Y.%m.%d")})
        else: continue
    for record in congrat_list:
        print(f"{record['name']} should be congratulated at {record['congratulation_date']}")


@input_error
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            add_contact(book, *args)
        elif command == "change":
            change_phone(book, *args)
        elif command == "adb":
            add_birthday(book, *args)
        elif command == "show-birthday":
            show_birthday(book, *args)
        elif command == "phone":
            show_phone(book, *args)
        elif command == "birthdays":
            show_birthdays(book)        
        elif command == "all":
            display_contacts(book)
        else:
            print("Invalid command.")



if __name__ == '__main__':
    main()
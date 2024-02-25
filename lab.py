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
def add_contact(args, contacts):
    name, phone = args
    #check if contact already in the list
    if any(name in item for item in contacts):
        return f"{name} is already added in the list"
    else:
        #add new contact
        contacts[name] = phone
        return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    name = args[0]
    #Search for an entity in the list with a key equal to name
    for key in contacts:
        if key == name:
            #Change value for entity with key = name
            contacts[name] = phone
        return "Contact is successfully changed."
    #Return error message in case if name is not found
    return ("No such contact")

@input_error
def show_phone(args, contacts):
    name = args[0]
    #return value from the contacts where key = argument arg[0]
    return (contacts[name])

@input_error        
def show_all(contacts):
    #if contacts list is not empty create string (s) with names and numbers
    if contacts:
        s=''
        for key in contacts:
            s+=(f"{key:10} - {contacts[key]}\n")
        return s
    else:
        #Return error in case if list is empty
        return ("No contacts in the list")

def main():
    contacts = {}
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
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
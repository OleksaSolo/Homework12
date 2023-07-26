from ab_classes import AddressBook, Name, Phone, Birthday, Record, error_except
import pickle

address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError as e:
            return "You are entering an invalid command."
    return wrapper


@input_error
@error_except
def add_command(*args):
    name = Name(args[0])
    phone = Phone(args[1]) if len(args) > 1 else None
    birthday = Birthday(args[2]) if len(args) > 2 else None
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone, birthday)
    return address_book.add_record(rec)

@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"

@input_error
def delete_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.del_phone(phone)
    return f"No contact {name} in address book"

@input_error
def find_command(*args):
    search = args[0]
    result = address_book.find_records(search)
    #return result
    if result != []:
        return f"In address book {search} find in record(s): {result}"
    else:
        return f"In address book not find record(s) containing: {search}"
    

def hello_command(*args):
    return f"How can I help you?"


def exit_command(*args):
    return "Bye"


def unknown_command(*args):
    return "Unknown command. I don't understand. Please, input rigth command."


def show_all_command(*args):
    return address_book


COMMANDS = {
    add_command: ("add", "+"),
    change_command: ("change", "зміни"),
    delete_command: ("del", "видалити"),
    find_command: ("find", "знайти"),
    exit_command: ("bye", "exit", "end"),
    hello_command: ("hello", "hi"),
    show_all_command: ("show all", )
}


def parser(text:str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                # print(cmd)
                data = text[len(kwd):].strip().split()
                # print(data)
                return cmd, data 
    return unknown_command, []


def main():
    address_book.read_book()
    print(address_book)
    while True:
        user_input = input("Input command: hello, add name phone birthday, change name phone_old phone_new, del name phone, find name, show all, bye/end/exit\n>>>")
        
        cmd, data = parser(user_input)
        
        result = cmd(*data)
        
        print(result)
        
        if cmd == exit_command:
            print(address_book.save_book())
            break

if __name__ == "__main__":
    main()
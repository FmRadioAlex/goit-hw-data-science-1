import os
from collections import UserDict
from datetime import datetime as dt
import datetime
import pickle
os.system("clear")
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return"Помилка 😭"
        except IndexError:
            return"Enter the argument for the command"
        except Exception as eror:
            print(f"Error: {eror}")
    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
        

class Name(Field):
    def __init__(self, name):
        self.name=name

    def __str__(self):
        return str(self.name)
    

class Phone(Field):
    def __init__(self, phone):
        fail="1234567890"
        if len(phone)==10:
            self.phone=phone
        else:
            self.phone=fail
            print ("No range number phone and added number:1234567890")
        
    def __str__(self):
        return str(self.phone)    

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self,number):
        self.phones.append(Phone(number))

    def add_birthday(self,date):
        self.birthday=date
   
    def print_day(self):
       return self.birthday
           
    def delete_phone(self,phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self,old_num,new_num):
        
        enum=0
        for count in self.phones:
            if old_num == count.phone:
                self.phones[enum] = Phone(new_num)
            enum+=1
    
    def find_phone(self,phone):
        if phone in self.phones:
            return phone
    
    


    def __str__(self):
        return f"Contact name: {self.name.name}, phones: {'; '.join(p.phone for p in self.phones)} Birthday:{self.birthday}"

class AddressBook(UserDict,Phone):
    
    def add_record(self,class_person):
        
        self.data[class_person.name.name] = class_person
        
       
    def find(self,name):
        return self.get(name)
    
    def delete(self,name):
        for nick, other in self.data.items():
            if nick==name:
                del self.data[nick]
                return other
            

    def __str__(self) -> str:
        return self.class_person
    



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

def change_phone_number(args,book: AddressBook):
    name, old_phone, new_phone, *_=args
    record = book.find(name)
    record.edit_phone(old_phone,new_phone)
    
    return f"Change"

def show_phone(args, book: AddressBook):
    name, *_=args
    return book.get(name)
    

def show_all(book: AddressBook):
    for name, record in book.data.items():
        print(record)

def add_birthday(args, book: AddressBook):
    name,*_=args
    for record, other in book.items():
   
        if name == record:
            try:
                find_record=book.find(name)
                date_birtday=dt(year=int(input("Year= ")),month=int(input("Month= ")),day=int(input("Day= ")))
                find_record.add_birthday(date_birtday)
                return"Add"
            except Exception as eror:
                    os.system('clear')
                    print(f"Error: {eror}")
                    add_birthday(name,book)    
    return f"No found Name: {name}"

def s_birthday(args, book: AddressBook):
    name, *_=args
    record=book.get(name)
    return record.print_day()
    
    
def get_upcoming_birthdays(book:AddressBook):

    
    one_person=[]
    for name, other in book.items():
        
        day_birthday=other.print_day()
        if day_birthday!=None:
            day_now=(dt.now())
            day_happy=dt(day_now.year, day_birthday.month, day_birthday.day).date()

            
            if(day_happy-day_now.date()).days < 0:
                day_happy=dt(day_now.year+1, day_birthday.month, day_birthday.day).date()
            elif(day_happy - day_now.date()).days < 7:
                if(day_happy-day_now.date()).days == 6:
                    day_happy=day_happy+datetime.timedelta(days=1)
                elif(day_happy-day_now.date()).days == 5:
                    day_happy=day_happy+datetime.timedelta(days=2)
                one_person.append(name)
                one_person.append(str(day_happy))
        
    return one_person
    


def help_command():
    print(f"\n\nadd [ім'я]\nhello-виведе привіт \nclose|exit- закриє программу \nchange [Ім'я] [Старий телефон] [Новий]- Міняє номер телефона\nphone [Номер телефона]-шукає по телефону\nadd-birthday [ім'я]-додає день народженя до контакту\nshow-birthday [ім'я]-показує коли день народження у контакта\nall-вивести увесь список\ncls-почитсити вікно")

def main():

    

    os.system('cls')
    book = load_data()
    print(f"\nWelcome to the assistant bot! You can use command 'help'\n")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        

        if command in ["close", "exit"]:
            save_data(book)  # Викликати перед виходом з програми
            print("Good bye!")
            break


        elif command == "hello":
            print("How can I help you?")


        elif command == "add":
            print(add_contact(args, book))

        

        elif command=="change":     
            print(change_phone_number(args, book))
                    

        elif command=="phone":
            print(show_phone(args,book))


        elif command=="all":
            show_all(book)

        elif command=='help':
            help_command()
        elif command in ["add-birthday","ab"]:
            
            print(add_birthday(args, book))

        elif command in ["show-birthday","sb"]:
            
            print(s_birthday(args, book))
        elif command in ["birthdays","bd"]:
                    
            print(get_upcoming_birthdays(book))

        elif command=="fm":
            print(f"А що ми тут робимо я тут слідкую  \n┬┴┬┴┤(･_├┬┴┬┴")


        elif command in ["cls","clear"]:
            os.system('clear')
        

        else:
            print("Invalid command.")


            


if __name__ == "__main__":
    main()


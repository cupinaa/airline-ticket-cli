import csv
from . import validation as iu
from .paths import data_path
from .state import users, current_user

def login():
    print('\nSign in\n')
    while True:
        found = False
        username = input('Enter username: ').strip()
        password = input('Enter password: ').strip()
        for k in users:
            if k[1] == username:
                found = True
                if k[2] == password:
                    print('\nSigned in successfully')
                    current_user.clear()
                    current_user.append(k)
                    return True
                else:
                    print('Incorrect password')
                    break
        if not found:
            print('Incorrect username')

def username_exists(username):
    for x in users:
        if x[1] == username:
            return True
    return False

def register_customer():
    username = iu.username()
    password = iu.password()
    phone = iu.phone()
    email = iu.email()
    first_name = iu.first_name()
    last_name = iu.last_name()
    record = ['customer', username, password, phone, email, first_name, last_name, None, None, None]
    users.append(record)
    current_user.append(record)
    with open(data_path('users.csv'), 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(record)
    return True

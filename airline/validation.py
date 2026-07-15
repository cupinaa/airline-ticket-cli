from .state import airports, flights, aircraft_models, users

def username():
    while True:
        first_name = input('Enter username: ').strip()
        if len(first_name) < 5:
            print('Username must contain at least 5 characters.')
            continue
        if ' ' in first_name:
            print('Username cannot contain spaces.')
            continue
        if '@' in first_name:
            print("Username cannot contain '@'.")
            continue
        if any((user[1] == first_name for user in users)):
            print('That username is already taken. Choose another.')
            continue
        break
    return first_name

def password():
    while True:
        password = input('Enter password: ').strip()
        if not any((char.isdigit() for char in password)):
            print('Password must contain at least one digit.')
            continue
        if not any((char.isupper() for char in password)):
            print('Password must contain at least one uppercase letter.')
            continue
        if len(password) < 7:
            print('Password must contain at least 7 characters.')
            continue
        break
    return password

def phone():
    while True:
        phone = input('Enter phone number: ').strip()
        if not phone.isdigit():
            print('Phone numbers must contain digits only.')
            continue
        if len(phone) < 9:
            print('The phone number is too short.')
            continue
        break
    return phone

def email():
    while True:
        email = input('Enter email: ').strip()
        if '@' not in email or '.' not in email:
            print('Enter a valid email address.')
            continue
        parts = email.split('@')
        if len(parts) != 2:
            print('Enter a valid email address.')
            continue
        if len(parts[0]) < 2 or len(parts[1]) < 6:
            print('Enter a valid email address.')
            continue
        break
    return email

def first_name():
    while True:
        user_input = input('Enter first name: ').strip()
        if not user_input.isalpha() or not user_input.istitle():
            print('Enter a valid first name.')
            continue
        break
    return user_input

def last_name():
    while True:
        user_input = input('Enter last name: ').strip()
        if not user_input.isalpha() or not user_input.istitle():
            print('Enter a valid last name.')
            continue
        break
    return user_input

def passport_number():
    while True:
        user_input = input('Enter passport number: ').strip()
        if not user_input.isdigit() or not 6 <= len(user_input) <= 9:
            print('Enter a valid passport number.')
            continue
        break
    return user_input

def nationality():
    while True:
        user_input = input('Enter nationality code: ').strip()
        if not (user_input.isalpha() and len(user_input) == 3 and user_input.isupper()):
            print('Enter a valid three-letter nationality code.')
            continue
        break
    return user_input

def gender():
    while True:
        user_input = input('Gender (male/female): ').lower().strip()
        if user_input != 'male' and user_input != 'female':
            print('Invalid option.')
            continue
        break
    return user_input

def flight_number():
    while True:
        found = False
        user_input = input('Enter flight number: ').strip().upper()
        if len(user_input) != 4 or not (user_input[:2].isalpha() and user_input[2:].isdigit()):
            print('Flight numbers must contain two letters followed by two digits (for example, JU12).')
            continue
        for l in flights:
            if l[0] == user_input:
                print('That flight already exists.')
                found = True
                break
        if found:
            continue
        if not found:
            return user_input

def origin():
    while True:
        found = False
        user_input = input('Enter origin: ').strip().upper()
        if len(user_input) != 3 or not user_input.isalpha():
            print('Enter a valid three-letter origin airport code.')
            continue
        for a in airports:
            if a[0] == user_input:
                found = True
                break
        if found:
            return user_input
        if not found:
            print('The origin airport was not found.')

def destination():
    while True:
        found = False
        user_input = input('Enter destination: ').strip().upper()
        if len(user_input) != 3 or not user_input.isalpha():
            print('Enter a valid three-letter destination airport code.')
            continue
        for a in airports:
            if a[0] == user_input:
                found = True
                break
        if found:
            return user_input
        if not found:
            print('The destination airport was not found.')

def departure_time():
    while True:
        user_input = input('Enter departure time (HH:MM): ').strip()
        if len(user_input) != 5 or user_input[2] != ':':
            print('Time must use HH:MM format (for example, 07:30)')
            continue
        hours_value = user_input[:2]
        minutes_value = user_input[3:]
        if not (hours_value.isdigit() and minutes_value.isdigit()):
            print('Time must contain digits only (for example, 07:30)')
            continue
        hours_value = int(hours_value)
        minutes_value = int(minutes_value)
        if not (23 >= hours_value >= 0 and 59 >= minutes_value >= 0):
            print('Invalid time')
            continue
        return user_input

def arrival_time():
    while True:
        user_input = input('Enter arrival time (HH:MM): ').strip()
        if len(user_input) != 5 or user_input[2] != ':':
            print('Time must use HH:MM format (for example, 07:30)')
            continue
        hours_value = user_input[:2]
        minutes_value = user_input[3:]
        if not (hours_value.isdigit() and minutes_value.isdigit()):
            print('Time must contain digits only (for example, 07:30)')
            continue
        hours_value = int(hours_value)
        minutes_value = int(minutes_value)
        if not (23 >= hours_value >= 0 and 59 >= minutes_value >= 0):
            print('Invalid time')
            continue
        return user_input

def crosses_midnight(departure_time, arrival_time):
    from datetime import datetime
    departure = datetime.strptime(departure_time, '%H:%M')
    arrival = datetime.strptime(arrival_time, '%H:%M')
    difference = arrival - departure
    if difference.total_seconds() > 0:
        return 'no'
    else:
        return 'yes'

def airline_name():
    while True:
        user_input = input('Enter airline name: ').strip()
        if len(user_input) == 0:
            print('Enter a valid airline name.')
            continue
        return user_input

def flight_days():
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        user_input = input('Enter comma-separated flight days: ').strip().lower()
        if len(user_input) == 0:
            print('Enter at least one day.')
            continue
        days_list = []
        for d in user_input.split(','):
            d = d.strip()
            days_list.append(d)
        invalid = False
        for d in days_list:
            if d not in valid_days:
                print('Invalid input')
                invalid = True
                break
        if invalid:
            continue
        return days_list

def aircraft_model():
    while True:
        found = False
        user_input = input('Enter aircraft model: ').strip().upper()
        for m in aircraft_models:
            if m[0] == user_input:
                found = True
                break
        if found:
            return user_input
        if not found:
            print('The aircraft model was not found.')

def price():
    while True:
        user_input = input('Enter flight price: ').strip()
        if not user_input.isdigit():
            print('Price must be numeric.')
            continue
        return user_input

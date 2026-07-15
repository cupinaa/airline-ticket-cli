from datetime import datetime, timedelta
import csv
from . import validation as iu
from .paths import data_path
from .state import tickets, scheduled_flights, flights, users, current_user

def register_seller():
    username = iu.username()
    password = iu.password()
    phone = iu.phone()
    email = iu.email()
    first_name = iu.first_name()
    last_name = iu.last_name()
    record = ['seller', username, password, phone, email, first_name, last_name, None, None, None]
    users.append(record)
    current_user.append(record)
    with open(data_path('users.csv'), 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(record)
    return True

def create_flight():
    flight_number = iu.flight_number()
    origin = iu.origin()
    destination = iu.destination()
    departure_time = iu.departure_time()
    arrival_time = iu.arrival_time()
    crosses_midnight = iu.crosses_midnight(departure_time, arrival_time)
    airline_name = iu.airline_name()
    days_list = iu.flight_days()
    flight_days = ','.join(days_list)
    aircraft_model = iu.aircraft_model()
    price = iu.price()
    record = [flight_number, origin, destination, departure_time, arrival_time, crosses_midnight, airline_name, flight_days, aircraft_model, price]
    flights.append(record)
    with open(data_path('flights.csv'), 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(record)

def edit_flight():
    input_value = input('Enter flight number: ').strip().upper()
    flight_to_edit = None
    for l in flights:
        if l[0] == input_value:
            flight_to_edit = l
            break
    if flight_to_edit is None:
        print('No flight has that number')
        return
    print('Change flight')
    print('1. Change origin')
    print('2. Change destination')
    print('3. Change departure time')
    print('4. Change arrival time')
    print('5. Change airline')
    print('6. Change flight days')
    print('7. Change aircraft model')
    print('8. Change price')
    input_value = input('>> ')
    if input_value == '1':
        flight_to_edit[1] = iu.origin()
    elif input_value == '2':
        flight_to_edit[2] = iu.destination()
    elif input_value == '3':
        flight_to_edit[3] = iu.departure_time()
    elif input_value == '4':
        flight_to_edit[4] = iu.arrival_time()
    elif input_value == '5':
        flight_to_edit[6] = iu.airline_name()
    elif input_value == '6':
        days_list = iu.flight_days()
        flight_to_edit[7] = ','.join(days_list)
    elif input_value == '7':
        flight_to_edit[8] = iu.aircraft_model()
    elif input_value == '8':
        flight_to_edit[9] = iu.price()
    else:
        print('Invalid option')
    with open(data_path('flights.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['flight_number', 'origin', 'destination', 'departure_time', 'arrival_time', 'crosses_midnight', 'airline', 'flight_days', 'aircraft_model', 'price'])
        writer.writerows(flights)

def manage_ticket_deletions():
    print('Ticket deletion')
    deletion = []
    copies = tickets.copy()
    for k in tickets:
        if k[7] == '1':
            print(f'|{k[0]}|{k[1]}|{k[2]:^11}|{k[3]:^11}|{k[4]:^5}|{k[5]:^16}|{k[6]}|')
            deletion.append(k[0])
    if not deletion:
        print('No tickets are available for deletion.')
        return
    print('\n1. Delete all')
    print('2. Select a ticket to delete')
    print('3. Select a ticket to restore')
    user_input = input('>> ').strip()
    if user_input == '1':
        for k in copies:
            if k[0] in deletion:
                tickets.remove(k)
    elif user_input == '2':
        input_value = input('Enter ticket number to delete: ').strip()
        if input_value in deletion:
            for k in copies:
                if k[0] == input_value:
                    tickets.remove(k)
                    break
        else:
            print('The ticket number is not available for deletion')
    elif user_input == '3':
        input_value = input('Enter ticket number to restore: ').strip()
        if input_value in deletion:
            for k in tickets:
                if k[0] == input_value:
                    k[7] = '0'
                    break
        else:
            print('The ticket number is not available for deletion')
    else:
        print('Invalid option')
    with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
        writer.writerows(tickets)

def reporting():
    print('1. Sold tickets for a selected sale date')
    print('2. Sold tickets for a selected departure date')
    print('3. Sold tickets for a selected sale date and seller')
    print('4. Total ticket count and value for the selected sale date')
    print('5. Total ticket count and value for the selected departure date')
    print('6. Total ticket count and value for the selected sale date and seller ')
    print('7. Total ticket count and value in the last 30 days for each seller')
    user_input = input('>> ').strip()
    if user_input == '1':
        sale_day = input('Enter sale date: ').strip()
        for k in tickets:
            if k[8] == sale_day:
                print(f'|{k[0]}|{k[1]}|{k[2]:^11}|{k[3]:^11}|{k[4]:^5}|{k[5]:^16}|')
    elif user_input == '2':
        ids = []
        departure_day = input('Enter departure date: ').strip()
        for k in scheduled_flights:
            if k[2] == departure_day:
                ids.append(k[0])
        for kr in tickets:
            if kr[1] in ids:
                print(f'Tickets for {departure_day}')
                print(f'|{kr[0]}|{kr[1]}|{kr[2]:^11}|{kr[3]:^11}|{kr[4]:^5}|{kr[5]:^26}|')
    elif user_input == '3':
        sale_day = input('Enter sale date: ').strip()
        seller_username = input('Enter seller username: ').strip()
        for k in tickets:
            if k[8] == sale_day and k[9] == seller_username:
                print(f'Tickets for {k[8]} sold by {k[9]} ')
                print(f'|{k[0]}|{k[1]}|{k[2]:^11}|{k[3]:^11}|{k[4]:^5}|{k[5]:^16}|')
    elif user_input == '4':
        sale_day = input('Enter sale date: ').strip()
        found = False
        counter = 0
        price = 0
        for k in tickets:
            for kl in scheduled_flights:
                for l in flights:
                    if k[8] == sale_day and k[1] == kl[0] and (kl[1] == l[0]):
                        counter += 1
                        price += int(l[9])
                        found = True
        if found:
            print(f'Total tickets sold:{counter}\nTotal price:{price}')
        if not found:
            print('No tickets were found for the selected date')
    elif user_input == '5':
        ids = []
        found = False
        counter = 0
        price = 0
        departure_day = input('Enter departure date: ').strip()
        for k in scheduled_flights:
            if k[2] == departure_day:
                ids.append(k[0])
        for k in tickets:
            for kl in scheduled_flights:
                for l in flights:
                    if k[1] in ids and k[1] == kl[0] and (kl[1] == l[0]):
                        counter += 1
                        price += int(l[9])
                        found = True
        if found:
            print(f'Total tickets sold:{counter}\nTotal price:{price}')
        if not found:
            print('No tickets were found for the selected date')
    elif user_input == '6':
        seller = input('Enter seller username: ').strip()
        sale_day = input('Enter sale date: ').strip()
        found = False
        counter = 0
        price = 0
        for k in tickets:
            for kl in scheduled_flights:
                for l in flights:
                    if k[8] == sale_day and k[1] == kl[0] and (kl[1] == l[0]) and (k[9] == seller):
                        counter += 1
                        price += int(l[9])
                        found = True
        if found:
            print(f'For {seller}:\nTotal tickets sold:{counter}\nTotal price:{price}')
        if not found:
            print('No tickets were found for the selected date and seller')
    elif user_input == '7':
        today = datetime.today()
        cutoff = today - timedelta(days=30)
        statistics = {}
        for k in tickets:
            sale_date = datetime.strptime(k[8], '%Y-%m-%d')
            seller = k[9]
            if sale_date >= cutoff:
                for k in tickets:
                    for kl in scheduled_flights:
                        for l in flights:
                            if k[1] == kl[0] and kl[1] == l[0] and (k[9] == seller):
                                price = int(l[9])
                if seller not in statistics:
                    statistics[seller] = [0, 0]
                statistics[seller][0] += 1
                statistics[seller][1] += price
        print('\nReport for the last 30 days\n')
        for p in statistics:
            number = statistics[p][0]
            total = statistics[p][1]
            print(f'{p}')
            print(f'  Tickets sold: {number}')
            print(f'  Total price: {total} \n')

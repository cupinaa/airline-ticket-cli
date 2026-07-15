from datetime import datetime, timedelta
import csv
from . import validation as iu
from .paths import data_path
from .state import tickets, scheduled_flights, flights, seat_inventory, current_user

def ticket_purchase_menu():
    flight = []
    found = False
    print('1. Search for a flight')
    print('2. Scheduled flight ID')
    user_input = input('>> ')
    if user_input == '1':
        origin = input('Enter origin: ').upper()
        destination = input('Enter destination: ').upper()
        departure = input('Enter departure time: ')
        carrier = input('Enter carrier: ')
        date_value = input('Enter departure date (YYYY-MM-DD): ')
        for n in flights:
            if n[1] == origin and n[2] == destination and (n[3] == departure) and (n[6] == carrier):
                for x in scheduled_flights:
                    if n[0] == x[1] and x[2] == date_value:
                        flight.append(x[0])
                        found = True
        purchase_ticket(flight, found)
    elif user_input == '2':
        flight_number = input('Enter scheduled flight ID: ')
        for n in scheduled_flights:
            if n[0] == flight_number:
                flight.append(n[0])
                found = True
        purchase_ticket(flight, found)
    else:
        print('Invalid option')

def purchase_ticket(flight, found):
    if not found:
        print('No flight matches the provided details')
    if found:
        for y in seat_inventory:
            if y[0] == flight[0]:
                if int(y[3]) > 0:
                    print(f'Seats remaining: {y[3]}')
                    with open(data_path('seat_inventory.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter='|')
                        writer.writerow(['scheduled_flight_id', 'aircraft_model', 'capacity', 'available_seats'])
                        writer.writerows(seat_inventory)
                    ticket_purchase_options(flight)
                else:
                    print(f'Flight {flight[0]} has no available seats')

def ticket_purchase_options(flight):
    print('1. Purchase for yourself')
    print('2. Purchase for another passenger')
    user_input = input('>> ')
    today = datetime.today().date()
    if user_input == '1':
        print('Do you want to complete the purchase \n(yes/no)')
        crosses_midnight = input('>> ').lower().strip()
        if crosses_midnight == 'yes':
            for n in current_user:
                number = next_ticket_number()
                record = [number, flight[0], n[5], n[6], n[3], n[4], None, None, today, 'online']
                tickets.append(record)
            for y in seat_inventory:
                if y[0] == flight[0]:
                    if int(y[3]) > 0:
                        y[3] = str(int(y[3]) - 1)
                        print(f'Ticket purchased for flight {flight[0]}. Seats remaining: {y[3]}\n')
                        with open(data_path('seat_inventory.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile, delimiter='|')
                            writer.writerow(['scheduled_flight_id', 'aircraft_model', 'capacity', 'available_seats'])
                            writer.writerows(seat_inventory)
            purchase = True
            with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter='|')
                writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
                writer.writerows(tickets)
                continue_purchase(purchase, flight)
        if crosses_midnight == 'no':
            purchase = False
            continue_purchase(purchase, flight)
    if user_input == '2':
        first_name = iu.first_name()
        last_name = iu.last_name()
        number = next_ticket_number()
        print('Do you want to complete the purchase?\n(yes/no)')
        crosses_midnight = input('>> ').lower().strip()
        if crosses_midnight == 'yes':
            for n in current_user:
                record = [number, flight[0], first_name, last_name, n[3], n[4], None, None, today, 'online']
                tickets.append(record)
            for y in seat_inventory:
                if y[0] == flight[0]:
                    if int(y[3]) > 0:
                        y[3] = str(int(y[3]) - 1)
                        print(f'Ticket purchased for flight {flight[0]}. Seats remaining: {y[3]}\n')
                        with open(data_path('seat_inventory.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile, delimiter='|')
                            writer.writerow(['scheduled_flight_id', 'aircraft_model', 'capacity', 'available_seats'])
                            writer.writerows(seat_inventory)
            purchase = True
            with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter='|')
                writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
                writer.writerows(tickets)
                continue_purchase(purchase, flight)
        if crosses_midnight == 'no':
            purchase = False
            continue_purchase(purchase, flight)

def continue_purchase(purchase, flight):
    from datetime import timedelta, datetime
    found = False
    has_seats = False
    extended_flight = []
    today = datetime.today().date()
    if purchase:
        print('Continue with the next flight')
        print('1. Buy a ticket for the next flight')
        print('2. Buy a ticket for a travel companion')
        print('X. Exit')
        user_input = input('>> ')
        if user_input == '1':
            destination = input('Enter destination: ').upper()
            departure = input('Enter departure time: ')
            for n in scheduled_flights:
                if flight[0] == n[0]:
                    for x in flights:
                        if n[1] == x[0]:
                            origin = x[2]
                            time_value = x[4]
                            found = True
            if found:
                for y in flights:
                    if y[1] == origin and y[2] == destination:
                        for z in scheduled_flights:
                            if z[1] == y[0]:
                                extended_flight.append(z[0])
            if extended_flight:
                time_object = datetime.strptime(time_value, '%H:%M')
                departure_time = datetime.strptime(departure, '%H:%M')
                difference = departure_time - time_object
                if timedelta(minutes=1) <= difference <= timedelta(minutes=120):
                    for y in seat_inventory:
                        if y[0] == extended_flight[0] and int(y[3]) > 0:
                            has_seats = True
                            break
                    if not has_seats:
                        print(f'No seats are available for flight {extended_flight[0]}.')
                        return
                    for n in current_user:
                        number = next_ticket_number()
                        record = [number, extended_flight[0], n[5], n[6], n[3], n[4], None, None, today, 'online']
                        tickets.append(record)
                        for y in seat_inventory:
                            if y[0] == extended_flight[0]:
                                y[3] = str(int(y[3]) - 1)
                                print(f'Ticket purchased for flight {extended_flight[0]}. Seats remaining: {y[3]}')
                                break
            else:
                print('No connecting flight is available within 120 minutes of the previous flight')
            if not found or not extended_flight:
                print('No matching flight was found.')
                return
        elif user_input == '2':
            first_name = iu.first_name()
            last_name = iu.last_name()
            number = next_ticket_number()
            for y in seat_inventory:
                if y[0] == flight[0] and int(y[3]) > 0:
                    has_seats = True
                    break
            if not has_seats:
                print(f'No seats are available for flight {flight[0]}.')
                return
            for n in current_user:
                record = [number, flight[0], first_name, last_name, n[3], n[4], None, None, today, 'online']
                tickets.append(record)
                for y in seat_inventory:
                    if y[0] == flight[0]:
                        y[3] = str(int(y[3]) - 1)
                        print(f'Ticket purchased for flight {flight[0]}. Seats remaining: {y[3]}')
                        break
        else:
            print('Leaving ticket purchase...')
            return
    with open(data_path('seat_inventory.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['scheduled_flight_id', 'aircraft_model', 'capacity', 'available_seats'])
        writer.writerows(seat_inventory)
    with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
        writer.writerows(tickets)

def next_ticket_number():
    with open(data_path('ticket_counter.txt'), 'r', encoding='utf-8') as f:
        number = int(f.read())
    number += 1
    with open(data_path('ticket_counter.txt'), 'w', encoding='utf-8') as f:
        f.write(str(number))
    return number

def list_upcoming_tickets():
    today = datetime.today().date()
    user = current_user[0]
    phone_number = user[3]
    first_name = user[5]
    for m in tickets:
        if m[4] == phone_number and m[2] == first_name:
            for l in scheduled_flights:
                if l[0] == m[1]:
                    flight_date = datetime.strptime(l[2], '%Y-%m-%d').date()
                    if flight_date > today:
                        print(f'{m[0]}|{m[1]}|{m[2]}|{m[3]}|{m[4]}|{m[5]}|')
                        print('-' * 53)
                        break

from datetime import datetime, timedelta
import csv
from . import validation as iu
from .paths import data_path
from .checkin import select_seat
from .booking import next_ticket_number
from .state import tickets, scheduled_flights, flights, aircraft_models, guest_passengers, users, seat_inventory, current_user

def sell_ticket():
    print('\nSell tickets\n')
    print('1. Find a flight by search')
    print('2. Find a flight by ID')
    has_seats = False
    found = False
    today = datetime.today().date()
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
                        flight = x[0]
    elif user_input == '2':
        flight = input('Enter scheduled flight ID: ')
    else:
        print('Invalid option')
        return
    for y in seat_inventory:
        if y[0] == flight:
            if int(y[3]) > 0:
                print(f'\nSeats remaining: {y[3]}')
                has_seats = True
                with open(data_path('seat_inventory.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='|')
                    writer.writerow(['scheduled_flight_id', 'aircraft_model', 'capacity', 'available_seats'])
                    writer.writerows(seat_inventory)
            else:
                print('\nNo seats available')
                return
    if has_seats:
        first_name = iu.first_name()
        last_name = iu.last_name()
        for n in users:
            if n[5] == first_name and n[6] == last_name:
                email = n[4]
                phone = n[3]
                found = True
                break
        if not found:
            email = iu.email()
            phone = iu.phone()
        print('Do you want to complete the purchase?\n(yes/no)')
        crosses_midnight = input('>> ').lower().strip()
        if crosses_midnight == 'yes':
            number = next_ticket_number()
            record = [number, flight, first_name, last_name, phone, email, None, 0, today, current_user[0][1]]
            tickets.append(record)
            for y in seat_inventory:
                if y[0] == flight:
                    if int(y[3]) > 0:
                        y[3] = str(int(y[3]) - 1)
                        print(f'Ticket purchased for flight {flight}. Seats remaining: {y[3]}')
                        with open(data_path('seat_inventory.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile, delimiter='|')
                            writer.writerow(['scheduled_flight_id', 'aircraft_model', 'capacity', 'available_seats'])
                            writer.writerows(seat_inventory)
            with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter='|')
                writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
                writer.writerows(tickets)
        if crosses_midnight == 'no':
            print('Returning to the start...')

def seller_check_in():
    today = datetime.today()
    flight_found = False
    date_found = False
    found = False
    scheduled_flight_ids = []
    user = None
    ticket_number = None
    first_name = iu.first_name()
    last_name = iu.last_name()
    for n in users:
        if n[5] == first_name and n[6] == last_name:
            email = n[4]
            found = True
            user = n
            break
    if not found:
        email = iu.email()
    for m in tickets:
        if m[2] == first_name and m[3] == last_name and (m[5] == email):
            ticket_number = m[0]
            scheduled_flight_ids.append(m[1])
    for l in scheduled_flights:
        if l[0] in scheduled_flight_ids:
            date_value = datetime.strptime(l[2], '%Y-%m-%d')
            date_found = True
    if date_found:
        difference = date_value - today
        if difference <= timedelta(days=2):
            flight_found = True
        else:
            print('Check-in is not available yet. Check-in opens 48 hours before departure.')
    if flight_found:
        if found:
            for k in user:
                if n[7] == '':
                    passport = iu.passport_number()
                    nationality = iu.nationality()
                    gender = iu.gender()
                    for x in users:
                        if k[1] == x[1]:
                            k[7] = passport
                            x[7] = passport
                            k[8] = nationality
                            x[8] = nationality
                            k[9] = gender
                            x[9] = gender
                            with open(data_path('users.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                                writer = csv.writer(csvfile, delimiter='|')
                                writer.writerow(['role', 'username', 'password', 'phone', 'email', 'first_name', 'last_name', 'passport_number', 'nationality', 'gender'])
                                writer.writerows(users)
                                select_seat(scheduled_flight_ids, ticket_number)
            else:
                select_seat(scheduled_flight_ids, ticket_number)
        else:
            passport = iu.passport_number()
            nationality = iu.nationality()
            gender = iu.gender()
            record = [first_name, last_name, passport, nationality, gender]
            guest_passengers.append(record)
            with open(data_path('guest_passengers.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter='|')
                writer.writerow(['first_name', 'last_name', 'passport_number', 'nationality', 'gender'])
                writer.writerows(guest_passengers)
                select_seat(scheduled_flight_ids, ticket_number)

def edit_ticket():
    ticket_number = input('Enter the ticket number to edit: ').strip()
    ticket = None
    for k in tickets:
        if k[0] == ticket_number:
            ticket = k
            break
    if ticket is None:
        print('No ticket has that number.')
        return
    print('\nWhat do you want to change?')
    print('1. Change seat')
    print('2. Change flight')
    choice = input('>> ')
    if choice == '1':
        select_replacement_seat(ticket_number)
    elif choice == '2':
        new_value = input('Enter new scheduled flight ID: ').strip()
        exists = False
        for k in scheduled_flights:
            if k[0] == new_value:
                exists = True
                break
        if not exists:
            print('No flight has that ID.')
            return
        has_seats = False
        for s in seat_inventory:
            if s[0] == new_value:
                if int(s[3]) > 0:
                    has_seats = True
                break
        if not has_seats:
            print('No seats are available on that flight.')
            return
        for b in tickets:
            if b[0] == ticket_number:
                b[1] = new_value
                b[6] = ''
                print('Flight changed successfully; the seat assignment was reset.')
                break
        with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
            writer.writerows(tickets)
    else:
        print('Invalid option.')
        return

def select_replacement_seat(ticket_number, occupied_seats_file=data_path('occupied_seats.csv'), tickets_file=data_path('tickets.csv')):
    ticket = None
    for k in tickets:
        if k[0] == ticket_number:
            ticket = k
            break
    if ticket is None:
        print('Ticket not found.')
        return
    scheduled_flight_id = ticket[1]
    old_seat = ticket[6]
    aircraft = None
    for s in seat_inventory:
        if s[0] == scheduled_flight_id:
            aircraft = s
            break
    if aircraft is None:
        print('Aircraft data is unavailable.')
        return
    aircraft_model = aircraft[1]
    row_count = 0
    seats_per_row = []
    for m in aircraft_models:
        if m[0] == aircraft_model:
            row_count = int(m[1])
            seats_per_row = m[2].strip('"').split(',')
            break
    occupied = []
    try:
        with open(occupied_seats_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == scheduled_flight_id:
                    occupied = row[1:]
                    break
    except FileNotFoundError:
        pass
    if old_seat in occupied:
        occupied.remove(old_seat)
    print(f'\nSeat map for flight {scheduled_flight_id} (X = occupied):')
    for r in range(1, row_count + 1):
        display_row = []
        for letter in seats_per_row:
            label = f'{r}{letter}'
            if label in occupied:
                display_row.append('X')
            else:
                display_row.append(letter)
        print(f'Row {r}: ', ' '.join(display_row))
    while True:
        new_seat = input('\nEnter new seat (for example, 28A): ').strip().upper()
        if new_seat in occupied:
            print('That seat is occupied.')
            continue
        ticket[6] = new_seat
        occupied.append(new_seat)
        print('Seat changed successfully!')
        break
    with open(tickets_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
        writer.writerows(tickets)
    print('Ticket data updated successfully.')
    all_rows = []
    try:
        with open(occupied_seats_file, newline='', encoding='utf-8') as f:
            all_rows = list(csv.reader(f))
    except FileNotFoundError:
        all_rows = []
    updated_file = []
    found = False
    for row in all_rows:
        if row and row[0] == scheduled_flight_id:
            updated_file.append([scheduled_flight_id] + occupied)
            found = True
        else:
            updated_file.append(row)
    if not found:
        updated_file.append([scheduled_flight_id] + occupied)
    with open(occupied_seats_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(updated_file)
    print('Occupied seats updated.')

def delete_ticket():
    number = input('Enter the ticket number to delete: ').strip()
    found_ticket = False
    for k in tickets:
        if k[0] == number:
            k[7] = '1'
            found_ticket = True
            print('Ticket deleted successfully!')
            break
    if found_ticket:
        print('Ticket deleted successfully!')
        with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
            writer.writerows(tickets)
    if not found_ticket:
        print('No ticket has that number.')
        return

def search_sold_tickets():
    print('Search tickets')
    print('1. By origin')
    print('2. By destination')
    print('3. By departure date')
    print('4. By arrival date')
    print('5. By passenger name')
    user_input = input('>> ')
    flight_numbers = []
    flight_ids = []
    found_ticket = False
    if user_input == '1':
        origin = input('Enter origin: ')
        for l in flights:
            if l[1] == origin:
                flight_numbers.append(l[0])
        for k in scheduled_flights:
            if k[1] in flight_numbers:
                flight_ids.append(k[0])
        for kr in tickets:
            if kr[1] in flight_ids:
                found_ticket = True
                print(f'|{kr[0]}|{kr[1]}|{kr[2]:^11}|{kr[3]:^11}|{kr[4]:^5}|{kr[5]:^16}|{kr[6]}|')
    elif user_input == '2':
        destination = input('Enter destination: ')
        for l in flights:
            if l[2] == destination:
                flight_numbers.append(l[0])
        for k in scheduled_flights:
            if k[1] in flight_numbers:
                flight_ids.append(k[0])
        for kr in tickets:
            if kr[1] in flight_ids:
                found_ticket = True
                print(f'|{kr[0]}|{kr[1]}|{kr[2]:^11}|{kr[3]:^11}|{kr[4]:^5}|{kr[5]:^16}|{kr[6]}|')
    elif user_input == '3':
        departure_date_input = input('Enter departure date: ')
        for k in scheduled_flights:
            if k[2] in departure_date_input:
                flight_ids.append(k[0])
        for kr in tickets:
            if kr[1] in flight_ids:
                found_ticket = True
                print(f'|{kr[0]}|{kr[1]}|{kr[2]:^11}|{kr[3]:^11}|{kr[4]:^5}|{kr[5]:^16}|{kr[6]}|')
    elif user_input == '4':
        arrival_date_input = input('Enter arrival date: ')
        for k in scheduled_flights:
            if k[3] in arrival_date_input:
                flight_ids.append(k[0])
        for kr in tickets:
            if kr[1] in flight_ids:
                found_ticket = True
                print(f'|{kr[0]}|{kr[1]}|{kr[2]:^11}|{kr[3]:^11}|{kr[4]:^5}|{kr[5]:^16}|{kr[6]}|')
    elif user_input == '5':
        first_name = iu.first_name()
        last_name = iu.last_name()
        for kr in tickets:
            if kr[2] == first_name and kr[3] == last_name:
                found_ticket = True
                print(f'|{kr[0]}|{kr[1]}|{kr[2]:^11}|{kr[3]:^11}|{kr[4]:^5}|{kr[5]:^16}|{kr[6]}|')
    else:
        print('Invalid option')
    if not found_ticket:
        print('No ticket matches the provided information')

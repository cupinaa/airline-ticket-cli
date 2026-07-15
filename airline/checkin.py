from datetime import datetime, timedelta
import csv
from . import validation as iu
from .paths import data_path
from .state import tickets, scheduled_flights, aircraft_models, users, seat_inventory, current_user

def customer_check_in():
    today = datetime.today()
    flight_found = False
    date_found = False
    for n in current_user:
        if n[7] == '':
            passport = iu.passport_number()
            nationality = iu.nationality()
            gender = iu.gender()
            for x in users:
                if n[1] == x[1]:
                    n[7] = passport
                    x[7] = passport
                    n[8] = nationality
                    x[8] = nationality
                    n[9] = gender
                    x[9] = gender
            with open(data_path('users.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter='|')
                writer.writerow(['role', 'username', 'password', 'phone', 'email', 'first_name', 'last_name', 'passport_number', 'nationality', 'gender'])
                writer.writerows(users)
        for m in tickets:
            if m[2] == n[5] and m[3] == n[6]:
                ticket_number = m[0]
                scheduled_flight_ids = [m[1]]
                flight_info = next((l for l in scheduled_flights if l[0] == m[1]), None)
                if flight_info:
                    flight_date = datetime.strptime(flight_info[2], '%Y-%m-%d')
                    if timedelta(days=0) <= flight_date - today <= timedelta(days=2):
                        select_seat(scheduled_flight_ids, ticket_number)
                        flight_found = True
                    else:
                        print(f'Check-in for {m[1]} is not available yet. Check-in opens 48 hours before departure.')
    if flight_found:
        print('\nCheck-in completed for all eligible flights.')

def select_seat(scheduled_flight_ids, ticket_number, occupied_seats_file=data_path('occupied_seats.csv')):
    for scheduled_flight_id in scheduled_flight_ids:
        if isinstance(scheduled_flight_id, list):
            scheduled_flight_id = scheduled_flight_id[0]
        aircraft = next((s for s in seat_inventory if s[0] == scheduled_flight_id), None)
        if aircraft is None:
            print(f'No aircraft data exists for scheduled flight {scheduled_flight_id}.')
            continue
        aircraft_model = aircraft[1]
        model_info = next((m for m in aircraft_models if m[0] == aircraft_model), None)
        if model_info:
            row_count = int(model_info[1])
            seats_per_row = model_info[2].strip('"').split(',')
        else:
            row_count = 0
            seats_per_row = []
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
        seat_map = []
        for r in range(1, row_count + 1):
            row = []
            for s in seats_per_row:
                label = f'{r}{s}'
                if label in occupied:
                    row.append('X')
                else:
                    row.append(s)
            seat_map.append(row)
        print(f'\nSeat map for flight {scheduled_flight_id} (X = occupied):')
        for i, row in enumerate(seat_map, start=1):
            print(f'Row {i}: ', '  '.join(row))
        while True:
            choice = input('\nEnter seat (for example, 1B): ').strip().upper()
            if len(choice) < 2:
                print('Invalid input. Try again.')
                continue
            row_number = int(choice[:-1])
            letter = choice[-1]
            if row_number < 1 or row_number > row_count or letter not in seats_per_row:
                print('That seat does not exist. Try again.')
                continue
            if choice in occupied:
                print('That seat is occupied. Choose another.')
                continue
            occupied.append(choice)
            seat_map[row_number - 1][seats_per_row.index(letter)] = 'X'
            print(f'Seat reserved successfully: {choice}')
            for k in tickets:
                if k[0] == ticket_number:
                    k[6] = choice
            with open(data_path('tickets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter='|')
                writer.writerow(['ticket_number', 'scheduled_flight_id', 'first_name', 'last_name', 'phone', 'email', 'seat', 'deleted', 'sale_date', 'seller'])
                writer.writerows(tickets)
            all_occupied = []
            try:
                with open(occupied_seats_file, newline='', encoding='utf-8') as f:
                    all_occupied = list(csv.reader(f))
            except FileNotFoundError:
                all_occupied = []
            updated_all = []
            found = False
            for row in all_occupied:
                if row and row[0] == scheduled_flight_id:
                    updated_all.append([scheduled_flight_id] + occupied)
                    found = True
                else:
                    updated_all.append(row)
            if not found:
                updated_all.append([scheduled_flight_id] + occupied)
            with open(occupied_seats_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(updated_all)
            break

from datetime import datetime, timedelta
from . import validation as iu
from .state import scheduled_flights, flights

def list_upcoming_flights():
    seen_flights = []
    for n in scheduled_flights:
        today = datetime.today()
        date_value = datetime.strptime(n[2], '%Y-%m-%d')
        if date_value > today:
            for x in flights:
                if x[0] == n[1] and n[0] not in seen_flights:
                    seen_flights.append(n[0])
                    print(f'|{n[2]:^12}|{n[3]:^5}|{x[0]:^6}|{x[1]:^10}|{x[2]:^10}|{x[3]:^8}|{x[4]:^8}|{x[5]:^8}|{x[6]:^22}|{x[7]:^45}|{x[8]:^6}|{x[9]:^5}|')
                    print('-' * 165)

def search_flights():
    print('====== Search flights ======')
    print(' 1. Search by origin')
    print(' 2. Search by destination')
    print(' 3. Search by departure date')
    print(' 4. Search by arrival date')
    print(' 5. Search by departure time')
    print(' 6. Search by arrival time')
    print(' 7. Search by carrier')
    user_input = input('>> ')
    if user_input == '1':
        input_value = input('Enter origin: ').strip().upper()
        found = False
        for n in flights:
            if n[1] == input_value:
                print(f'|{n[0]}|{n[1]}|{n[2]}|{n[3]}|{n[4]}|{n[5]}|{n[6]:^22}|{n[7]:^45}|{n[8]}|{n[9]:^3}|')
                print('-' * 108)
                found = True
        if not found:
            print('No flight matches that origin')
    elif user_input == '2':
        input_value = input('Enter destination: ').strip().upper()
        found = False
        for n in flights:
            if n[2] == input_value:
                print(f'|{n[0]}|{n[1]}|{n[2]}|{n[3]}|{n[4]}|{n[5]}|{n[6]:^22}|{n[7]:^45}|{n[8]}|{n[9]:^3}|')
                print('-' * 108)
                found = True
        if not found:
            print('No flight matches that destination')
    elif user_input == '3':
        input_value = input('Enter departure date: ')
        found = False
        for n in scheduled_flights:
            if n[2] == input_value:
                for x in flights:
                    if n[1] == x[0]:
                        print(f'|{n[2]}|{n[3]}|{x[0]}|{x[1]}|{x[2]}|{x[3]}|{x[4]}|{x[5]}|{x[6]:^22}|{x[7]:^45}|{x[8]}|{x[9]:^3}|')
                        print('-' * 130)
                        found = True
        if not found:
            print('No flight matches that departure date')
    elif user_input == '4':
        input_value = input('Enter arrival date: ')
        found = False
        for n in scheduled_flights:
            if n[3] == input_value:
                for x in flights:
                    if n[1] == x[0]:
                        print(f'|{n[2]}|{n[3]}|{x[0]}|{x[1]}|{x[2]}|{x[3]}|{x[4]}|{x[5]}|{x[6]:^22}|{x[7]:^45}|{x[8]}|{x[9]:^3}|')
                        print('-' * 130)
                        found = True
        if not found:
            print('No flight matches that arrival date')
    elif user_input == '5':
        input_value = input('Enter departure time: ')
        found = False
        for n in flights:
            if n[3] == input_value:
                print(f'|{n[0]}|{n[1]}|{n[2]}|{n[3]}|{n[4]}|{n[5]}|{n[6]:^22}|{n[7]:^45}|{n[8]}|{n[9]:^3}|')
                print('-' * 108)
                found = True
        if not found:
            print('No flight matches that departure time')
    elif user_input == '6':
        input_value = input('Enter arrival time: ')
        found = False
        for n in flights:
            if n[4] == input_value:
                print(f'|{n[0]}|{n[1]}|{n[2]}|{n[3]}|{n[4]}|{n[5]}|{n[6]:^22}|{n[7]:^45}|{n[8]}|{n[9]:^3}|')
                print('-' * 108)
                found = True
        if not found:
            print('No flight matches that arrival time')
    elif user_input == '7':
        input_value = input('Enter carrier name: ')
        found = False
        for n in flights:
            if n[6] == input_value:
                print(f'|{n[0]}|{n[1]}|{n[2]}|{n[3]}|{n[4]}|{n[5]}|{n[6]:^22}|{n[7]:^45}|{n[8]}|{n[9]:^3}|')
                print('-' * 108)
                found = True
        if not found:
            print('No flight matches that carrier')
    else:
        print('Invalid option.')

def multi_criteria_search():
    filtered = scheduled_flights.copy()
    while True:
        print('\n====== Search flights ======')
        print(' 1. Search by origin')
        print(' 2. Search by destination')
        print(' 3. Search by departure date')
        print(' 4. Search by arrival date')
        print(' 5. Search by departure time')
        print(' 6. Search by arrival time')
        print(' 7. Search by carrier')
        print(' 0. Show results')
        user_input = input('>> ')
        if user_input == '0':
            break
        ids = []
        new_filtered = []
        if user_input == '1':
            origin = input('Enter origin: ').upper()
            for l in flights:
                if l[1] == origin:
                    ids.append(l[0])
            for i in filtered:
                if i[1] in ids:
                    new_filtered.append(i)
        elif user_input == '2':
            destination = input('Enter destination: ').upper()
            for l in flights:
                if l[2] == destination:
                    ids.append(l[0])
            for i in filtered:
                if i[1] in ids:
                    new_filtered.append(i)
        elif user_input == '3':
            date_value = input('Enter departure date: ')
            for i in filtered:
                if i[2] == date_value:
                    new_filtered.append(i)
        elif user_input == '4':
            date_value = input('Enter arrival date: ')
            for i in filtered:
                if i[3] == date_value:
                    new_filtered.append(i)
        elif user_input == '5':
            time_value = input('Enter departure time: ')
            for l in flights:
                if l[3] == time_value:
                    ids.append(l[0])
            for i in filtered:
                if i[1] in ids:
                    new_filtered.append(i)
        elif user_input == '6':
            time_value = input('Enter arrival time: ')
            for l in flights:
                if l[4] == time_value:
                    ids.append(l[0])
            for i in filtered:
                if i[1] in ids:
                    new_filtered.append(i)
        elif user_input == '7':
            carrier = input('Enter carrier name: ')
            for l in flights:
                if l[6] == carrier:
                    ids.append(l[0])
            for i in filtered:
                if i[1] in ids:
                    new_filtered.append(i)
        else:
            print('Invalid option')
            continue
        filtered = new_filtered
    seen = set()
    unique = []
    for k in filtered:
        if k[0] not in seen:
            unique.append(k)
            seen.add(k[0])
    filtered = unique
    if not filtered:
        print('\nNo flights match all criteria.')
        return []
    for k in filtered:
        l = None
        for flight in flights:
            if flight[0] == k[1]:
                l = flight
                break
        if l is None:
            continue
        print(f'| {k[0]} | {k[2]} | {k[3]} | {k[1]} | {l[1]} | {l[2]} | {l[3]} | {l[4]} | {l[6]:^16} | {l[8]} | {l[9]}')
        print('-' * 100)
    return k[0]

def show_cheapest_flights():
    prices = []
    for flight in flights:
        prices.append(int(flight[9]))
    counter = 10
    flight_copy = flights.copy()
    ten_cheapest = []
    while True:
        if counter == 0:
            break
        else:
            minimum_price = min(prices)
            index_value = prices.index(minimum_price)
            n = flight_copy[index_value]
            ten_cheapest.append(n)
            del prices[index_value]
            del flight_copy[index_value]
            counter -= 1
            continue
    ten_cheapest.reverse()
    for n in ten_cheapest:
        print(f'|{n[0]:^6}|{n[1]:^6}|{n[2]:^6}|{n[3]:^6}|{n[4]:^6}|{n[5]:^4}|{n[6]:^22}|{n[7]:^40}|{n[8]:^6}|{n[9]:^4}|')
        print('-' * 118)

def flexible_departures():
    origin = iu.origin()
    destination = iu.destination()
    try:
        date_input = input('Enter departure date (YYYY-MM-DD): ').strip()
        flexible_days = int(input('Enter flexible-day range: ').strip())
        date_value = datetime.strptime(date_input, '%Y-%m-%d')
        start_date = date_value - timedelta(days=flexible_days)
        end_date = date_value + timedelta(days=flexible_days)
        arrival_date_input = input('Enter arrival date (YYYY-MM-DD): ').strip()
        arrival_flexible_days = int(input('Enter arrival flexible-day range: ').strip())
        arrival_date = datetime.strptime(arrival_date_input, '%Y-%m-%d')
        arrival_start_date = arrival_date - timedelta(days=arrival_flexible_days)
        arrival_end_date = arrival_date + timedelta(days=arrival_flexible_days)
    except ValueError:
        print('\nError: dates must use YYYY-MM-DD and the day range must be an integer.')
        return
    matching_flights = []
    for n in scheduled_flights:
        for x in flights:
            if n[1] == x[0]:
                flight_date = datetime.strptime(n[2], '%Y-%m-%d')
                flight_arrival_date = datetime.strptime(n[3], '%Y-%m-%d')
                if start_date <= flight_date <= end_date and arrival_start_date <= flight_arrival_date <= arrival_end_date and (origin == x[1]) and (destination == x[2]):
                    matching_flights.append(x)
    matching_flights.sort(key=lambda l: int(l[9]), reverse=True)
    if matching_flights:
        for x in matching_flights:
            print(f'|{x[0]:^6}|{x[1]:^6}|{x[2]:^6}|{x[3]:^6}|{x[4]:^6}|{x[5]:^4}|{x[6]:^22}|{x[7]:^40}|{x[8]:^6}|{x[9]:^6}|')
            print('-' * 120)
    else:
        print('No flight matches the provided details')

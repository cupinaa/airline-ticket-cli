import csv
from .paths import data_path
from .state import (
    aircraft_models,
    airports,
    flights,
    guest_passengers,
    scheduled_flights,
    seat_inventory,
    tickets,
    users,
)

def load_all():
    load_flights()
    load_users()
    load_guest_passengers()
    load_scheduled_flights()
    load_aircraft_models()
    load_airports()
    load_seat_inventory()
    load_tickets()

def load_scheduled_flights():
    scheduled_flights.clear()
    with open(data_path('scheduled_flights.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            scheduled_flights.append(row)

def load_flights():
    flights.clear()
    with open(data_path('flights.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            flights.append(row)

def load_users():
    users.clear()
    with open(data_path('users.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            users.append(row)

def load_guest_passengers():
    guest_passengers.clear()
    with open(data_path('guest_passengers.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            guest_passengers.append(row)

def load_aircraft_models():
    aircraft_models.clear()
    with open(data_path('aircraft_models.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            aircraft_models.append(row)

def load_airports():
    airports.clear()
    with open(data_path('airports.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            airports.append(row)

def load_seat_inventory():
    seat_inventory.clear()
    with open(data_path('seat_inventory.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            seat_inventory.append(row)

def load_tickets():
    tickets.clear()
    with open(data_path('tickets.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)
        for row in reader:
            tickets.append(row)

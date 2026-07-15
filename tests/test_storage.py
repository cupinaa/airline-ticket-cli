import unittest

from airline import state, storage
from airline.paths import DATA_DIR, data_path


class StorageTests(unittest.TestCase):
    def setUp(self):
        storage.load_all()

    def test_all_required_data_files_exist(self):
        expected = {
            "aircraft_models.csv",
            "airports.csv",
            "flights.csv",
            "guest_passengers.csv",
            "occupied_seats.csv",
            "scheduled_flights.csv",
            "seat_inventory.csv",
            "ticket_counter.txt",
            "tickets.csv",
            "users.csv",
        }
        self.assertTrue(DATA_DIR.is_dir())
        self.assertTrue(expected.issubset({path.name for path in DATA_DIR.iterdir()}))

    def test_data_paths_are_absolute(self):
        self.assertTrue(data_path("flights.csv").is_absolute())

    def test_loading_twice_does_not_duplicate_records(self):
        counts = (
            len(state.flights),
            len(state.scheduled_flights),
            len(state.users),
            len(state.tickets),
        )

        storage.load_all()

        self.assertEqual(
            counts,
            (
                len(state.flights),
                len(state.scheduled_flights),
                len(state.users),
                len(state.tickets),
            ),
        )


if __name__ == "__main__":
    unittest.main()

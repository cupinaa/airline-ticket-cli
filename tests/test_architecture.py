import importlib
import unittest


class ArchitectureTests(unittest.TestCase):
    def test_feature_modules_import_without_starting_cli(self):
        modules = (
            "airline.auth",
            "airline.booking",
            "airline.checkin",
            "airline.flights",
            "airline.management",
            "airline.sales",
            "airline.storage",
            "airline.validation",
        )

        for module in modules:
            with self.subTest(module=module):
                importlib.import_module(module)

if __name__ == "__main__":
    unittest.main()

# Contributing

Thank you for considering an improvement to Airline Ticket CLI.

## Development setup

1. Use Python 3.10 or newer.
2. Install the project in editable mode with `python -m pip install -e .` if you want the `airline-tickets` command.
3. Keep runtime dependencies limited to the Python standard library unless a new dependency provides a clear, documented benefit.

## Verification

Run the complete test suite before submitting a change:

```bash
python -m unittest discover -s tests -v
```

Also start the CLI with `python main.py` and verify the workflow affected by your change.

## Data changes

Only commit synthetic demonstration data. Do not add real names, personal email addresses, telephone numbers, passport numbers, credentials, or travel records.


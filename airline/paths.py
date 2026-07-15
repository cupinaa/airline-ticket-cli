"""Project paths shared by persistence and application services."""
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / 'data'

def data_path(filename: str) -> Path:
    """Return an absolute path to a runtime data file."""
    return DATA_DIR / filename

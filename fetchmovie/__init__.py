from pathlib import Path

__all__ = [
    'HOME_DIR',
    'VERSION',
]

app_root = str(Path(__file__).parents[1])

HOME_DIR = Path(app_root)
VERSION = '0.0.1.2'

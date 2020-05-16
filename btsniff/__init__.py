from pathlib import Path

__all__ = [
    'HOME_DIR',
    'VERSION',
]

VERSION = '0.0.2'
HOME_DIR = Path(__file__).parents[1]

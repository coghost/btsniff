from pathlib import Path

__all__ = [
    'HOME_DIR',
    'VERSION',
]

VERSION = '0.0.1'
HOME_DIR = Path(__file__).parents[1]

from dataclasses import dataclass
from pathlib import Path
from iparse import IParser

app_root = Path(__file__).parents[1]
MOVIE_HOME_DIR = app_root / 'data'


@dataclass
class CNChar:
    COLON = '：'


class MovieParser(IParser):
    def __init__(self, raw_data='', file_name='', is_test_mode=True, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', MOVIE_HOME_DIR)
        kwargs['log_level'] = 20
        if raw_data:
            kwargs['raw_data'] = raw_data
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)

    def _refine_post_date(self, info):
        return self.last_non_empty_info(info, CNChar.COLON)

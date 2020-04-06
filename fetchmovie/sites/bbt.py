__description__ = '''
url: bbt.tv
'''

import time
from dataclasses import dataclass
from pathlib import Path

from icraw import AsyncCrawler
from iparse import IParser
import sgr_ansi as echo
from vto.core import num_choice

app_root = Path(__file__).parents[1]

from fetchmovie.sites._chrome import get_page_by_chrome

BBT_HOME_DIR = app_root / 'data'


@dataclass
class BbtUrl:
    home: str = 'http://www.bbt.tv/'
    search: str = 'http://www.bbt.tv/index.php?s=vod-search'


class BbtParser(IParser):
    def __init__(self, raw_data='', file_name='', is_test_mode=True, **kwargs):
        kwargs['startup_dir'] = kwargs.get('startup_dir', BBT_HOME_DIR)
        kwargs['log_level'] = 20
        if raw_data:
            kwargs['raw_data'] = raw_data
        super().__init__(file_name, is_test_mode=is_test_mode, **kwargs)

    def _refine_torrent_name(self, info):
        return self.last_non_empty_info(info, index=0)


class Bbt(AsyncCrawler):
    def __init__(self, **kwargs):
        kwargs['site_init_url'] = BbtUrl.home
        super().__init__(**kwargs)

    def search_name(self, name):
        cnt = self.bs4post(BbtUrl.search, data={'wd': name}, ret='html')
        parser = BbtParser(raw_data=cnt)
        parser.do_parse()
        return parser.data['movies']

    def get_torrents(self, url):
        url = url.replace('https://', 'http://')
        cnt = self.bs4get(url, is_json=False)
        parser = BbtParser(raw_data=cnt)
        parser.do_parse()
        return parser.data['torrents']

    def get_thunder_link(self, url):
        st = time.time()

        url = url.replace('https://', 'http://')
        echo.BIg(f'>>> start to get thunder link:', end=' ')
        echo.BIU(url)
        dat = get_page_by_chrome(url)
        parser = BbtParser(raw_data=dat)
        parser.do_parse()
        cost_time = round(time.time() - st, 2)

        echo.BIg(f'    total cost {cost_time}s <<<')
        return parser.data['thunder']


def run_bbt(name, display_img=False):
    bbt = Bbt()

    dat = bbt.search_name(name)
    movies = [f'{m["movie"]["name"]}-{m["resolution"]}' for m in dat]
    movie_images = []
    if display_img:
        movie_images = [f"{m['image']}" for m in dat]
    c = num_choice(movies, img_list=movie_images)

    dat = dat[c]
    dat = bbt.get_torrents(dat['movie']['link'])
    torrents = [f"{t['name']}" for t in dat]
    c = num_choice(torrents)

    link = bbt.get_thunder_link(dat[c]['link'])
    return link

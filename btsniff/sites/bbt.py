__description__ = '''
url: bbt.tv
'''

import time
from dataclasses import dataclass
from pathlib import Path

from icraw import AsyncCrawler
import sgr_ansi as echo
from vto.core import num_choice
from vto import dec

app_root = Path(__file__).parents[1]

from btsniff.core import get_page_by_chrome, PageParser


@dataclass
class SiteURL:
    home: str = 'http://www.btbttv.cc/'
    # !WARN: UA Redirect ERROR
    search: str = 'http://www.btbttv.cc/index.php?s=vod-search'
    intro: str = f'bt电影天堂: {home}'


class BbtParser(PageParser):
    def _refine_torrent_name(self, info):
        return self.last_non_empty_info(info, index=0)


class Bbt(AsyncCrawler):
    def __init__(self, **kwargs):
        kwargs['site_init_url'] = SiteURL.home
        super().__init__(**kwargs)

    def search_name(self, name):
        cnt = self.bs4post(SiteURL.search, data={'wd': name}, ret='html')
        parser = BbtParser(raw_data=cnt)
        parser.do_parse()
        return parser.data['movies']

    def get_detail_page(self, url):
        url = url.replace('https://', 'http://')
        cnt = self.bs4get(url, is_json=False)
        parser = BbtParser(raw_data=cnt)
        parser.do_parse()
        return parser.data['torrents']

    @dec.prt(True)
    def get_final_link(self, url):
        url = url.replace('https://', 'http://')
        echo.BIg(f'>>> start to get thunder link:', end=' ')
        echo.BIU(url)
        dat = get_page_by_chrome(url)
        parser = BbtParser(raw_data=dat)
        parser.do_parse()
        return parser.data['thunder']


def run(name, display_img=False, overwrite=False):
    bbt = Bbt(overwrite=overwrite)

    dat = bbt.search_name(name)
    movies = [f'{m["movie"]["name"]}-{m["resolution"]}' for m in dat]
    movie_images = []
    if display_img:
        movie_images = [f"{m['image']}" for m in dat]
    c = num_choice(movies, img_list=movie_images, img_cache_dir=bbt.cache['site_media'])

    dat = dat[c]
    dat = bbt.get_detail_page(dat['movie']['link'])
    torrents = [f"{t['name']}" for t in dat]
    c = num_choice(torrents)

    link = bbt.get_final_link(dat[c]['link'])
    return link

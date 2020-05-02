__description__ = '''url: https://www.btdx8.com'''

from dataclasses import dataclass
import sgr_ansi
from icraw import AsyncCrawler
from vto.core import num_choice

from ._chrome import get_page_by_chrome
from ._parser import MovieParser


@dataclass
class Btdx8Url:
    home: str = 'https://www.btdx8.com/'
    search: str = 'https://www.btdx8.com/?s={}'
    more: str = 'https://www.btdx8.com/down.php'


class Btdx8Parser(MovieParser):
    def _refine_torrent_name(self, info):
        return self.last_non_empty_info(info, index=0)


class Btdx8(AsyncCrawler):
    def __init__(self, **kwargs):
        kwargs['site_init_url'] = Btdx8Url.home
        super().__init__(**kwargs)

    def search_name(self, name):
        cnt = self.bs4get(Btdx8Url.search.format(name))
        parser = Btdx8Parser(raw_data=cnt)
        parser.do_parse()
        return parser.data['movies']

    def get_detail_page(self, url):
        cnt = self.bs4get(url)
        parser = Btdx8Parser(raw_data=cnt)
        parser.do_parse()
        dat = parser.data['torrents']
        return dat.get('direct', []) + dat.get('more', [])

    def load_more(self, url):
        cnt = self.bs4get(url)
        parser = Btdx8Parser(raw_data=cnt)
        parser.do_parse()
        print(parser.data)
        return parser.data


def run(name, display_img=False, overwrite=False):
    bt = Btdx8(overwrite=overwrite)

    dat = bt.search_name(name)
    movies = [f'{m["movie"]["name"]}' for m in dat]
    images = []
    if display_img:
        images = [f"{m['image']}" for m in dat]
    c = num_choice(movies, img_list=images, img_cache_dir=bt.cache['site_media'])

    dat = dat[c]
    details = bt.get_detail_page(dat['movie']['url'])
    torrents = [f"{t['name']}" for t in details]
    c = num_choice(torrents, depth=2)
    url = details[c]['url']
    if Btdx8Url.more not in url:
        return url
    else:
        sgr_ansi.BIy('    >>>url is not supported download, please visit it manually!')
        return url

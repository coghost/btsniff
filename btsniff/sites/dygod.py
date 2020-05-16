__description__ = '''url: https://www.dy2018.com/'''

from dataclasses import dataclass
import sgr_ansi
from icraw import AsyncCrawler, ParseHeaderFromFile
from vto.core import num_choice
from vto.dec import prt
from ihelp import helper
from logzero import logger as zlog

from btsniff.core import PageParser, search_by_chrome


@dataclass
class SiteURL:
    home: str = 'https://www.dy2018.com/'
    search: str = 'https://www.dy2018.com/result'
    intro: str = f'电影天堂: {home}'


class DygodParser(PageParser):
    def _refine_torrent_name(self, info):
        return self.last_non_empty_info(info, index=0)

    def _refine_name(self, info):
        return self.last_non_empty_info(info, sep='=', index=-1)

    def _refine_url_href(self, info):
        if 'jianpian://pathtype=url' in info:
            return self.last_non_empty_info(info, sep='=', index=-1)
        return info


class Dygod(AsyncCrawler):
    def __init__(self, **kwargs):
        kwargs['site_init_url'] = SiteURL.home
        super().__init__(**kwargs)

    @prt(True)
    def search_name(self, name):
        pth, raw = self.load_cache(SiteURL.search, data={'keywords': name}, use_str=True)
        if not raw or self.overwrite:
            raw = search_by_chrome(SiteURL.home, ('input.formhue', name))
            helper.write_file(raw, pth)

        parser = DygodParser(raw_data=raw)
        parser.do_parse()
        return parser.data['movies']

    def get_detail_page(self, url: str) -> dict:
        """get movie candidates links

        Args:
            url (str): url

        Returns:
            dict: movies links
        """
        cnt = self.bs4get(url)
        parser = DygodParser(raw_data=cnt, encoding='gb2312')
        parser.do_parse()
        dat = parser.data['downloads']
        return dat


def run(name, display_img=False, overwrite=False):
    bt = Dygod(overwrite=overwrite)

    dat = bt.search_name(name)
    movies = [f'{m["name"]}' for m in dat]
    images = []
    if display_img:
        images = [f"{m['image']}" for m in dat]
    c = num_choice(movies, img_list=images, img_cache_dir=bt.cache['site_media'])

    dat = dat[c]
    details = bt.get_detail_page(dat['url'])
    candidates = [f"{t['name']}" for t in details]
    c = num_choice(candidates, depth=2)

    return details[c]['url']

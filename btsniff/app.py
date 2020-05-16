# -*- coding: utf-8 -*-
__date__ = '04/05 21:46'
__description__ = '''
'''

import urllib3
import sys
from pathlib import Path
from sgr_ansi import Chain
import sgr_ansi as echo
import click
from vto.core import copy_to_clipboard
from vto.dec import fmt_help

app_root = str(Path(__file__).parents[1])
sys.path.append(app_root)
urllib3.disable_warnings()

from btsniff.sites import SITES


@click.command(context_settings=dict(help_option_names=['-h', '--help'], terminal_width=200))
@click.option('--name', '-n', help=fmt_help('movie/actor name', '-n <name>'))
@click.option('--site', '-s', default='bbt', help=fmt_help('site name', '-s <site_name>'))
@click.option('--list_sites', '-l', is_flag=True, help=fmt_help('list supported sites', '-l'))
@click.option('--overwrite', '-w', is_flag=True, help=fmt_help('overwrite local cache', '-w'))
@click.option('--display_img', '-img', is_flag=True, help=fmt_help('display with image', '-img'))
def run(name, site, display_img, overwrite=False, list_sites=False):
    if list_sites:
        echo.BIy("Available sites:")
        for i, _site in enumerate(SITES.keys()):
            print(echo.BIm_(f'{_site:>8}'), echo.BIg_(f'[{SITES.get(_site).SiteURL.intro}]'))
        return
    chain = Chain()
    chain.BIUg(f'[SEARCH] site').BIUr(f'{site}').BIUg(f'for').BIUb(f'"{name}"').show()

    sniffer = SITES.get(site)
    link = sniffer.run(name, display_img, overwrite=overwrite)
    echo.IUb(link)
    copy_to_clipboard(link)


def debug_site(site, name, overwrite=False):
    """ local only """
    sniffer = SITES[site]
    sniffer.run(name, overwrite=overwrite)


if __name__ == '__main__':
    run()

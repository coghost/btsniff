# -*- coding: utf-8 -*-
__date__ = '04/05 21:46'
__description__ = '''
'''

import urllib3
import sys
from pathlib import Path
import sgr_ansi as echo
import click
from vto.core import copy_to_clipboard

app_root = str(Path(__file__).parents[1])
sys.path.append(app_root)
urllib3.disable_warnings()

from fetchmovie.sites import bbt


def fmt_help(*args, show_more=True, opt_hint='[OPT] '):
    desc = echo.g(args[0], show=False)
    if show_more:
        if len(args) > 1:
            args = list(args[1:])
            args.insert(0, opt_hint)
            usage = ''.join([echo.b(x, show=False) for x in args])
            desc = '{}\n{}'.format(desc, usage)
    return desc


@click.command(context_settings=dict(help_option_names=['-h', '--help'], terminal_width=200))
@click.option('--name', '-n', help=fmt_help('movie name', '-n <name>'))
@click.option('--site', '-s', default='BBT', help=fmt_help('site name', '-s <site_name>'))
@click.option('--display_img', '-img', is_flag=True,
              help=fmt_help('display with image', '-img'))
def run(name, site, display_img):
    echo.BIg(f'[SEARCH] {site} for {name}')
    link = bbt.run_bbt(name, display_img)
    echo.Ib(link)
    copy_to_clipboard(link)


if __name__ == '__main__':
    run()

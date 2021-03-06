# -*- coding: utf-8 -*-

import json
import argparse
import feedparser
from typing import (
    Final,
    Dict
)
from .color import *
from .util import *

def print_news(entry):
    print(magenta('▸ ') + white(str(entry.title)))
    print(green(entry.summary))
    print(yellow(entry.link))

def _real_main():
    datapath: str = inves_app_path() + "/urldata.json"
    with open(datapath, 'r') as data_file:
        URL_DATA: Final[Dict[str, str]] = json.load(data_file)

    parser = argparse.ArgumentParser(
            description="If you use this app, \
            you can know easily social situation on command line!!"
    )

    parser.add_argument('-t', '--type', default="main",
                        help="You can choose the news type which you want.\
                        can choose 'main', 'society', 'chemotherapy', \
                        'politics', 'economy', 'international', \
                        'sports', 'culture', 'live'.",
                        type=str)
    parser.add_argument('-n', "--number", default=7,
                        help="You can set the number of news \
                        that you want know.",
                        type=int)
    parser.add_argument('-a', "--all", action="store_true",
                        help="Show you the all news",
                        )
    parser.add_argument('-s', "--search", default='',
                        help="You can search article including specific word.",
                        type=str)

    args = parser.parse_args()

    parse_data = feedparser.parse(URL_DATA[args.type])
    feed = parse_data["feed"]
    entries = parse_data["entries"]
    entry_num = len(entries)

    if args.all or args.search != '':
        args.number = entry_num

    news_num: str = str(args.number) \
        if args.number <= entry_num else str(entry_num)

    print(blue("-*- " + feed["title"]) + ' ' + \
        cyan(feed["updated"][:-6]) + ' ' + \
        cyan('[' + str(news_num) + '/' + \
        str(entry_num) + ']') + blue(" -*-"))

    if args.search == '':
        i: int = 0
        for entry in entries:
            print_news(entry)
            i += 1
            if args.number > i:
                print()
            else:
                break
    else:
        i: int = 0
        print_yet: bool = False
        for entry in entries:
            if args.search in entry.summary + entry.link:
                if print_yet:
                    print()
                print_news(entry)
                print_yet = True

def main():
    _real_main()

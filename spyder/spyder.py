import re
import argparse
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def get_links(page=None, numlinks=None, curent_num=0, rec_l=None):

    if rec_l+1 <= curent_num:
        return True

    page = requests.get(page)
    soup = BeautifulSoup(page.content, features="html.parser")
    all_links = soup.findAll('a', attrs={'href': re.compile("^https://")})
    num_of_links = len(all_links)
    links_clean = [link.get('href') for link in all_links]
    # clamp number of links if there is not enough on this page
    clampped_numlinks = min(numlinks, num_of_links)

    pprint(f'level {curent_num} links \n{links_clean[:clampped_numlinks]}')

    for i in range(clampped_numlinks):
        get_links(page=links_clean[i],
                  numlinks=numlinks,
                  curent_num=curent_num+1,
                  rec_l=rec_l)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('rootpage', type=str, help='root page')
    parser.add_argument('numlinks', type=int, help='number of links')
    parser.add_argument('-rl', '--recur_level', type=int,
                        dest='recursive_level')
    parser.set_defaults(recursive_level=0)

    args = parser.parse_args()
    rootpage = args.rootpage
    numlinks = args.numlinks
    recursive_level = args.recursive_level

    if numlinks < 1:
        print('provide more then 0 number of links')
        raise Exception('Not enough links provided')

    get_links(page=rootpage, numlinks=numlinks, rec_l=recursive_level)

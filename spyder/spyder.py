import re
import argparse

import requests
from bs4 import BeautifulSoup


class NumLinksExceeded(Exception):
    pass


def get_links(page=None, numlinks=None, curent_num=1, rec_l=None):

    try:
        page = requests.get(page)

    except requests.exceptions.MissingSchema:
        print('Invalid URL')
        raise

    except Exception as e:
        raise(e)

    soup = BeautifulSoup(page.content, features="html.parser")

    for num, link in enumerate(soup.findAll('a',
                               attrs={'href': re.compile("^https://")}),
                               start=curent_num):

        if num > numlinks:
            raise NumLinksExceeded()

        a_link = link.get('href')
        print(f'{num} : {a_link} ')

        if rec_l > 0:
            get_links(page=a_link, numlinks=numlinks,
                      curent_num=num+1, rec_l=rec_l-1)

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('rootpage', type=str, help='root page')
    parser.add_argument('numlinks', type=int, help='number of links')
    parser.add_argument('-rl', '--recur_level', type=int, dest='recursive_level')
    parser.set_defaults(recursive_level=0)

    args = parser.parse_args()
    rootpage = args.rootpage
    numlinks = args.numlinks
    recursive_level = args.recursive_level

    if numlinks < 1:
        print('provide more then 0 number of links')
        raise Exception('Not enough links provided')

    try:
        get_links(page=rootpage, numlinks=numlinks, rec_l=recursive_level)
    except NumLinksExceeded:
        print('We are done !')

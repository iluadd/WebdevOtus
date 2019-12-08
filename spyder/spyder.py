import re
import argparse

import requests
from bs4 import BeautifulSoup


def get_links(page=None, numlinks=None, curent_num=1, rec=None):
    page = requests.get(page)
    soup = BeautifulSoup(page.content, features="html.parser")

    print(f'numlinks {numlinks}\n curent_num {curent_num}')
    for num, link in enumerate(soup.findAll('a',
                               attrs={'href': re.compile("^https://")}),
                               start=curent_num):

        if num > numlinks:
            raise(Exception('End of recursive search'))

        a_link = link.get('href')
        print(f'{num} : {a_link}')

        if rec:
            get_links(page=a_link, numlinks=numlinks,
                      curent_num=num+1, rec=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('rootpage', type=str, nargs=1, help='root page')
    parser.add_argument('numlinks', type=int, nargs=1, help='number of links')

    args = parser.parse_args()
    rootpage = args.rootpage[0]
    numlinks = args.numlinks[0]

    get_links(page=rootpage, numlinks=numlinks, rec=True)

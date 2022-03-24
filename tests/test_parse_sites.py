import pytest
from bs4 import BeautifulSoup

from vlcars.query_online import (parse_autocasion_page,
                                 get_n_pages_autocasion)


def test_parse_autocasion_page():

    # -------------------
    # set expected output
    file = "tests/files/autocasion_parsed.txt"
    expected = [line.strip().split("\t") for line in open(file, "r").readlines()]
    # replace by int type when necessary
    for line in expected:
        for i in range(3, 7):
            if line[i] != "":
                line[i] = int(line[i])


    # ------------------------------------------
    # test parser function parse_autocasion_page
    # read static html from "files/" directory
    with open('tests/files/test_page.html', 'r') as fin:
        content = fin.read()
        # parse html with bs4
        soup = BeautifulSoup(content, 'html.parser')
        # parse soup
        timestamp = "2022-03-24"
        parsed_page = sorted(parse_autocasion_page(soup, timestamp))

        for entry in parsed_page:
            print(entry)

        assert parsed_page == expected

def test_get_n_pages_autocasion():
    # read static html from "files/" directory
    with open('tests/files/test_page.html', 'r') as fin:
        content = fin.read()
        # parse html with bs4
        soup = BeautifulSoup(content, 'html.parser')
        n_pages = get_n_pages_autocasion(soup)
        assert n_pages == 732
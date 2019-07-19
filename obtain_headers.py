"""
This file contains the code necessary to get headers to rotate.

"""

import requests
import bs4
import constants



def format(header):
    return {'User-Agent' : header}

def obtain_headers(URL):
    answer = []

    source = requests.get(URL)
    source = bs4.BeautifulSoup(source.content,features='html.parser')
    source = source.find('tbody')
    source = source.find_all('tr')

    for header in source:
        # haluttu means 'wanted' in finnish
        haluttu = header.find('td')
        haluttu = haluttu.find('a')
        haluttu = haluttu.text
        answer.append(haluttu)

    # formatting answer. We want a list of dictionaries.
    answer = list(map(format,answer))
    return answer


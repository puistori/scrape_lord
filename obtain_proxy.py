
import requests
import bs4
import random
import constants

"""" 
    Obtains a list of proxies, just fyi. 
    The output isn't quite ready to be actually
    entered into the requests.get() function.
"""
# This takes a proxy string and turns it into a dictionary so that it could be
# used as an argument in requests.get()
def format(answer):
    return {'https' : answer}

def obtain_proxy(URL):
    answers = []

    source = requests.get(URL)
    source = bs4.BeautifulSoup(source.content,features='html.parser')
    source = source.find('tbody')
    source = source.find_all('tr')
    for proxy in source:
        proxy_info = proxy.find_all('td')
        IP = proxy_info[0].text
        PORT = proxy_info[1].text
        ANONYMITY = proxy_info[4].text
        HTTPS = proxy_info[6].text
        # checking conditions
        if ANONYMITY in ['anonymous','elite proxy']:
            # I assume we want HTTPS
            if HTTPS == 'yes':
                outcome = IP + ":" + PORT
                answers.append(outcome)


    endly_outcome = list(map(format,answers))
    return endly_outcome
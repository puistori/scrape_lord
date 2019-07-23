"""
This code will use the obtain_proxy function until it can confirm that the proxy is good.
"""

import requests
import bs4
import constants
import obtain_proxy
import traceback
import time
import random
import sys

URL = random.choice(constants.TEST_URLS)

def winnow_proxies(timeout=5):
    while(1):
        sys.stdout.write("Getting a new one!")
        sys.stdout.write("\n")
        sys.stdout.flush()
        proxy_candidates = obtain_proxy.obtain_proxy(constants.PROXY_NET)
        count = 0
        while len(proxy_candidates) > 0 and count < 15:
            print(len(proxy_candidates))
            try:
                count += 1
                index = random.randint(0,len(proxy_candidates))
                proxy = proxy_candidates.pop(index)
                r = requests.get(URL,proxies=proxy,timeout=timeout)
                return proxy
            except Exception as e:
                sys.stdout.write("fail")
                sys.stdout.write("\n")
                sys.stdout.flush()
        sys.stdout.write("refreshing. . . ")
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(0.5)






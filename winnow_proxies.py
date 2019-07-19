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

URL = random.choice(constants.TEST_URLS)

def winnow_proxies(timeout=5):
    while(1):
        print("gettin a new one!")
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
                #traceback.print_exc()
                print("fail")
        print("refreshing")
        time.sleep(0.5)






"""
Using the code I've written in the rest of the library, this
script will create a safe request to whatever URL.

It's two main fields are times, and timeout.

Times is how many times a request will be made with the same header and proxy before switching.
timeout is how long you wait fore a connection timeout when testing the different proxies.
"""

import requests
import constants
import random
import traceback

import obtain_headers
import winnow_proxies
import constants
import time

class Safe_Requester:

    def __init__(self,times,timeout=5,error_log_name="Safe_request_error_log"):

        self.count = 0
        self.header = None
        self.proxy = None
        self.timeout = timeout
        self.error_log_name = error_log_name

        if times < 1:
            self.times = 1

        else:
            self.times = times



    # exception handling


    def reset_header(self):
        #self.header = random.choice(obtain_headers.obtain_headers(random.choice(constants.HEADERS)))
        self.header = {'User-Agent' : random.choice(constants.MANUALLY_SELECTED_USER_AGENTS)}
    def reset_proxy(self):
        self.proxy = winnow_proxies.winnow_proxies(timeout=self.timeout)


    def SR(self,URL,verify=True):
        # in case it's the first request.
        if self.proxy == None:
            self.reset_proxy()
        if self.header == None:
            self.reset_header()

        keep_going = True
        try_count =0
        while keep_going:
            time.sleep(2)
            try:
                print("all right, trying it again")
                with requests.Session() as s:
                    answer = s.get(URL,proxies=self.proxy,headers=self.header,verify=verify)
                self.count += 1
                # after a while, you should switch IP's and Headers.
                if self.count >= self.times:
                    self.count = 0
                    self.reset_header()
                    self.reset_proxy()
                keep_going = False
                print("Success! You got a request finally!")
            except Exception as e:
                print("Problem with request. Resetting proxy")
                traceback.print_exc()
                print("Problem reported. Moving on.")
                self.count = 0
                self.reset_header()
                self.reset_proxy()
                print("Now we're trying this as our proxy : %s"%self.proxy)

                if try_count == 5:
                    keep_going = False
                    print("I GIVE UP ON THIS URL : %s"%URL)
                    file = open("%s"%self.error_log_name, "a")
                    file.write("%s\n"%URL)
                    file.close()

                try_count +=1
                print("This url, %s has been tried %s times"%(URL,try_count))

        return answer
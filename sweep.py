"""
This file contains code used to scrape all the data from a list of URLS.

You must give it the following:
 1. the scraping function that you are using. You'll have to design this yourself, of course.
    !!!The scraping function must have two parameters (unless you want to change the source code here).
    !! The two parameters must be named URL (for the URL you're trying to scrape from) and requester (in
    order to reference the requester object)
    ## fix with kwargs?
 2. The name of the file containing the scraping assignment.
    The scraping assignment must be a pickled list.
 3. Options and parametrs for the Safe_Request object
    This means 'times' and 'timeout'  which respectively manage how many iterations are used
    with the same proxy and how long you'll wait on a proxy to respond before
    skipping to another one.
4. outputname. this will govern the name of your output, as well as your error logs.
    The output name should NOT have any file extensions in it (don't say .txt, we'll take care of that)
5. writing options; choose whether the output will be text or bites (pickling), and
   whether you are overwriting or appending to that file or object. write "wt" or "wb" for
   writing text or writing bytes ( and then pickling ) respectively. By default, write_type
   is set to "wt" and append is set to True.
   !!! If you are appending to a pickled object, the pickled object must be a string, list or dictionary.


"""

import Safe_Request
import pickle
import time
import os.path
import warnings
import signal

#update number at three places.

def sweep(scrape_function,scraping_assignment,output_name,times=50,timeout=5,
          write_type="wt",append=True,delim="\n",sleep_time=1,verify=True):

    print("Starting sweep up!")
    print(scrape_function)
    print(scraping_assignment)
    print(output_name)
    # Dealing with overwrite/append issues.
    if append == True:
        if os.path.exists(output_name) and os.path.isfile(output_name):
            test = open("%s"%output_name,'rb')
            testP = pickle.load(test)
            test.close()
            if type(testP) != str and type(testP) != list:
                warnings.warn("Invalid append type. The script will instead REPLACE any file with the name %s."%output_name)
                append = False

        else:
            warnings.warn("Sorry, the file you wanted to overwrite could not be found. Creating one from scratch.")
            append = False


    # opening error log
    error_log_name = output_name +"_error_log.txt"
    log = open('%s'%error_log_name,'a')
    log.write("This file contains the error messages\nfor a new scraping session.\n")
    log.close()

    # opening a success_log
    success_log_name = output_name+"_success_log.txt"
    success_log = open("%s"%success_log_name, 'a')
    success_log.write("This file contains the successfully scraped scraping assignments for a new scraping session.")
    # I don't have the same motivation to close this log, so I'll keep it open.


    # Creating Safe_Requester object
    requester = Safe_Request.Safe_Requester(times=times,timeout=timeout,error_log_name=error_log_name,verify=verify)

    #Loading in scraping assignment
    pickle_in = open('%s'%scraping_assignment, 'rb')
    scraping_assignment = pickle.load(pickle_in)
    pickle_in.close()

    # Everything gets stored in a big list.
    Sweep_results = []

    # We want these to be saved in case we have to interrupt our program for whatever reason.

    def keyboardInterruptHandler(signal, frame):
        emergency_save = open("%s_emergency_save"%output_name, 'wb')
        pickle.dump(Sweep_results,emergency_save)
        emergency_save.close()
        success_log.close()
        exit(-1)

    signal.signal(signal.SIGINT, keyboardInterruptHandler)



    # We're all set! Now the actual scraping begins.
    for assignment in scraping_assignment:
        time.sleep(sleep_time)
        try:
            data = scrape_function(URL=assignment,requester=requester)
            Sweep_results.append(data)
            success_log.write(str(assignment)+"\n")

        except Exception as e:
            # This may be inefficient, but I'm concerned because the subfunction sameuses the log :/
            log = open('%s' % error_log_name, 'a')
            Error = ("Error with href %s" % scraping_assignment) + " : " + str(e) + "\n"
            log.write(Error)
            log.close()


    # saving our data! This will depend on our saving options.
    success_log.close()
    if write_type =="wt":
        appendingOrWriting = "a"
        if append == False:
            appendingOrWriting = "wt"
        results = open("%s.txt"%output_name,appendingOrWriting)
        for datapoint in Sweep_results:
            results.write(str(datapoint)+delim)
        results.close()
    elif write_type == "wb":

        if append == True:
            pickle_in = open("%s"%output_name,'rb')
            old_data = pickle.load(pickle_in)

            if type(old_data == str):
                for datapoint in Sweep_results:
                    old_data += datapoint
                    old_data += delim
            if type(old_data == list):
                for datapoint in Sweep_results:
                    old_data.append(datapoint)
            pickle_in.close()

            pickle_out = open("%s"%output_name,'wb')
            pickle.dump(old_data,pickle_out)
            pickle_out.close()

        elif append == False:
            pickle_out = open('%s'%output_name,'wb')
            pickle.dump(Sweep_results,pickle_out)
            pickle_out.close()

